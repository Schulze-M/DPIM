import argparse
import os
import random
from itertools import product

import numpy as np
import pm4py
from pm4py.algo.discovery.inductive.util import tree_consistency
from pm4py.algo.discovery.inductive.variants.im_clean import utils as pm4py_utils
from pm4py.algo.discovery.inductive.variants.im_clean.cuts import loop, sequence
from pm4py.algo.simulation.playout.process_tree import algorithm as tree_playout
from pm4py.objects.dfg.utils import dfg_utils
from pm4py.objects.process_tree import obj as pt
from pm4py.objects.process_tree.utils import generic
from pm4py.visualization.process_tree import visualizer as pt_visualizer

from utils import cut_detection, eventLog_parsing, start_end_iterators, utils


class DPIM():
    def __init__(self) -> None:
        self.epsilon: float = 1.0
        self.fit_trehsold: float = 0.95
        self.lower_bound: int = 0
        self.upper_bound: int = 0
        self.DP: bool = True
    
    
    def initialization(self) -> None:
        # initialize the parser
        parser = argparse.ArgumentParser(description='Differential private Inductive Miner for process discovery. Generates a PST, that preserves DP, from an event log.',
                                            formatter_class=argparse.RawTextHelpFormatter, 
                                            epilog='Example usage:\npython3 main.py "path/to/eventlog.xes" -e 1.0 -l 5 -u 32')
        
        # arguments
        parser.add_argument('eventlog', type=str, help='Path to the input event log file.')
        parser.add_argument('-e', '--epsilon', type=float, default=1.0, help='Epsilon parameter for differential privacy. Default is 1.0.')
        parser.add_argument('-l', '--lower', type=int, default=0, help='Lower bound for the uniformly random choice for the number of DFRs.')
        parser.add_argument('-u', '--upper', type=int, default=0, help='Upper bound for the uniformly random choice for the number of DFRs.')
        parser.add_argument('-t,', '--threshold', type=float, default=0.95, help='Set the threshold for the rejection sampler. Default is 0.95.')
        parser.add_argument('--no-dp', action='store_true', default=False, help='Use epsilon to infinity.')

        # Customizing the help message
        parser._positionals.title = "Required Arguments"
        parser._optionals.title = "Optional Arguments"
        parser._positionals.description = "It is required to give an event log, to be able to generate a PST."
        parser._optionals.description = "All values have defaults. However, it is recommended to give a value for epsilon, as the default is 1.0. \nThe lower and upper bounds are used to determine the number of DFRs, so the default may be too excessive. \n"

        # parse the arguments
        args = parser.parse_args()

        # set the arguments
        if args.no_dp:
            self.DP = False
            self.epsilon = 100000

        # get the file path
        file_path = args.eventlog
        file_path = file_path.replace('"', '')
        name, extension = os.path.splitext(file_path)

        # set the epsilon to which the operations shouls sum up to
        self.epsilon = args.epsilon
        # set the threshold for the rejection sampler
        self.fit_trehsold = args.threshold

        # check type of file and go to the correct function
        if  extension.lower() == '.csv':
            import csv

            import pandas as pd

            # detect the delimiter of the.csv file
            with open(self.file_path, "r") as csvfile:
                dialect = csv.Sniffer().sniff(csvfile.readline())
            # read .csv file
            event_log = pd.read_csv(file_path, sep=dialect.delimiter)
            # define dataframe of the EventLog
            event_log = pm4py.format_dataframe(event_log, case_id='TraceID', activity_key='ActivityName', timestamp_key='TimeStamp')
            # do the necessary preprocessing
            permutations, traceList, num_acts = eventLog_parsing.csvFile().main_csv(event_log=event_log)

        elif extension.lower() == '.xes':
            from pm4py.objects.log.importer.xes import importer as xes_importer

            # read .xes file and do the necessary preprocessing
            event_log = xes_importer.apply(file_path)
            permutations, traceList, num_acts = eventLog_parsing.xesFile().createPermutations_XES(event_log=event_log)

        # set the lower and upper bounds
        if args.lower < num_acts or args.lower >= args.upper or args.lower > (num_acts**2) -1:
            self.lower_bound = num_acts
        else:
            self.lower_bound = args.lower

        if args.upper > (num_acts**2) -1 or args.upper <= args.lower or args.upper < num_acts:
            self.upper_bound = (num_acts**2) -1
        else:
            self.upper_bound = args.upper

        # create the process tree
        tree = self.create_tree(permutations=permutations, traceList=traceList, epsilon=self.epsilon, event_log=event_log)
        
        if tree is not False:
            gviz = pt_visualizer.apply(tree, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"})
            pt_visualizer.view(gviz)
        
        return


    def create_tree(self, permutations: list[tuple], traceList: list, epsilon: float, event_log: pm4py.objects.log.obj.EventLog) -> pt.ProcessTree or False:
        """
        Selects permutations which are used to build a process tree. 
        A rejection sampling algorithm is used to evaluate whether the created tree is accepted or not.

        Parameters:
            permutations (list[tuple]): List of permutations to consider.
            traceList (list): List of traces.
            epsilon (float): Privacy parameter for adding Laplace noise.
            event_log: Event log.

        Returns:
            Process tree if a tree with fitness score above the threshold is found, False otherwise.
        """

        gamma: float = 0.01
        e_0: float = 0.01
        T: int = int(max(1/gamma * np.log(2/e_0), 1/(np.e*gamma)))

        # subtract 0.01 (=e_0) from epsilon to get the correct value for the laplace noise
        # ensures that the overall epsilon is equal to the input epsilon
        epsilon: float = (epsilon -e_0)/2

        # get all permutations to count, only once per trace
        permutations_to_count: list[str] = [str(elem) for sublist in traceList for elem in set(sublist)]

        # get the score for each permutation, based on the occurens in the traces
        arr_traces: np.array() = np.array(permutations_to_count)
        unique_elements, counts = np.unique(arr_traces, return_counts=True)
        str_to_tuple: list[tuple] = [eval(elem) for elem in unique_elements]

        # create a dictionary with the permutations and their scores
        scoreDict: dict[tuple: float] = dict(zip(str_to_tuple, counts))

        # include remaining permutations with a score of 0
        for permutation in permutations:
            if permutation not in scoreDict:
                scoreDict[permutation] = 0

        for _ in range(0, T):
            coin_flip = random.random()
            selected_edges = dict()

            tmp_scoreDict: dict[tuple: float] = scoreDict.copy()

            if self.DP:
                # the lower and upper bound must be changed based on the complexety of the data
                n_cuts: int = np.random.randint(self.lower_bound, self.upper_bound)

                # get the edges
                edges: list = list(tmp_scoreDict.keys())

                # get the noisy scores
                noisy_scores: list = list(tmp_scoreDict.values())

                try:
                    # get the index of the  n_cuts highest scores
                    selected_permus_index: list[int] = np.argsort(noisy_scores)[-n_cuts:]
                except ValueError:
                    print("\nYour lower or upper bound is too high, please choose lower values. \nThe bounds are located in the n_cuts variable.")
                    print("Exiting...")
                    exit()

                for permutation_index in selected_permus_index:
                    selected_edges.update({edges[permutation_index]: utils.add_laplace_noise(scoreDict[edges[permutation_index]], 1, (epsilon/n_cuts)/2 *0.65)})


            else:
                # get all elemts with the highest score as long as their is a score > 0
                while max(tmp_scoreDict.values()) > 0.0 and len(list(tmp_scoreDict.keys())) > 0:
                    # get the edges
                    edges: list = list(tmp_scoreDict.keys())

                    # get the noisy scores
                    noisy_scores: list = list(tmp_scoreDict.values())

                    # choose the index of the permutation with the max noisy score
                    permutation_index = np.argmax(noisy_scores)

                    # update the selected edges
                    selected_edges.update({edges[permutation_index]: scoreDict[edges[permutation_index]]})

                    # remove the permutation on the selcted index from the dictionary
                    tmp_scoreDict.pop(edges[permutation_index])

                n_cuts = len(selected_edges)

            # build the process tree
            if self.DP:
                tree = PostProcessing(epsilon_std=(epsilon*0.65)/(2*n_cuts), epsilon=epsilon*0.25, DP=True).recursive_tree_build(selected_edges=selected_edges, traceList=traceList)
            else:
                tree = PostProcessing(epsilon_std=(epsilon)/(2*n_cuts), epsilon=100000, DP=False).recursive_tree_build(selected_edges=selected_edges, traceList=traceList)

            if tree is not None:
                net, initial_marking, final_marking = pm4py.convert_to_petri_net(tree)
                if self.DP:
                    fitness_score: float = utils.add_laplace_noise(pm4py.fitness_token_based_replay(event_log, net, initial_marking, final_marking)['log_fitness'], 
                                                                    1/len(traceList), epsilon*0.1)
                else:
                    fitness_score: float = utils.add_laplace_noise(pm4py.fitness_token_based_replay(event_log, net, initial_marking, final_marking)['log_fitness'], 
                                                                    1/len(traceList), 1000000)
            else:
                fitness_score = 0.0

            # cap the score at 1.0
            if fitness_score > 1.0:
                fitness_score: float = 1.0

            if fitness_score >= self.fit_trehsold:
                return tree

            # probability to stop and return nothing
            elif coin_flip <= gamma:
                return False

        # no tree was found
        return False


class PostProcessing:

    def __init__(self, epsilon: float, epsilon_std: float, DP: bool) -> None:
        self.incoming = 0.0
        self.start = set()
        self.end = set()
        self.cutSet_to_start_end = dict()
        self.trace_occurences = dict()
        self.predecessor = dict()
        self.successor = dict()
        self.traceList = list()
        self.epsilon = epsilon
        self.epsilon_std = epsilon_std

        self.DP = DP


    def recursive_tree_build(self, selected_edges: dict[tuple: float], traceList: list[list[tuple]]) -> pt.ProcessTree or None:
        """
        Builds a process tree recursively based on the selected edges. 
        Computes the initial alphabet and the direct predecessors and successors of each activities.

        Parameters:
            selected_edges (dict[tuple: float]): A dictionary containing the selected edges and their weights.
            traceList (list[list[tuple]]): A list of traces, where each trace is a list of tuples representing activities.

        Returns:
            pt.ProcessTree: The constructed process tree.
        """

        # set the direct predecessors and successors of the activities based on the selected edges
        self.predecessor, self.successor = utils.get_pred_succ(selected_edges)

        self.traceList = traceList.copy()

        alphabet = {act for edge in selected_edges for act in edge}
        
        # build the process tree, as the selected edges privacy preserving and non-deterministic
        # the recursive function can exceed the recursion limit, so build a flower model to catch the exception
        try:
            tree = self.relations(selected_edges, alphabet, None)

            # tree normalization
            tree_consistency.fix_parent_pointers(tree)
            tree = generic.fold(tree)
            generic.tree_sort(tree)
        except RecursionError:
            tree = None

        return tree
        

    # build the tree
    def relations(self, selected_edges: dict[tuple: float], alphabet: set, root: None) -> pt.ProcessTree:
        """
        This method calculates the relations between activities based on the selected edges and alphabet.
        It returns a ProcessTree object representing the process flow.

        Parameters:
            selected_edges (dict[tuple: float]): A dictionary containing the selected edges and their number of traces occuring.
            alphabet (set): A set of activities.
            root (None): The root node of the process tree.

        Returns:
            pt.ProcessTree: The process tree representing the process flow.
        """

        # get the occurences of the activities in the traces
        if len(self.trace_occurences) == 0:
            tmp_selected_edges = selected_edges.copy()
            # Calculate trace occurrences
            for permutation, score in tmp_selected_edges.items():
                self.trace_occurences[permutation[0]] = self.trace_occurences.get(permutation[0], 0) + score

            # error handling to ensure that all activities are in the trace_occurences and no exception is thrown
            for permutation in tmp_selected_edges:
                if permutation[1] not in self.trace_occurences:
                    self.trace_occurences[permutation[1]] = self.trace_occurences.get(permutation[0], 0)
        

        # if start and end activities are present save them accordingly and remove them from the selected edges and alphabet
        if '0xb2e-start-0x31c' in alphabet or '0x31c-end-0x1021' in alphabet:
            # Calculate start and end activities
            self.start = {a[1] for a, s in selected_edges.items() if a[0] == '0xb2e-start-0x31c'}
            self.end = {a[0] for a, s in selected_edges.items() if a[1] == '0x31c-end-0x1021'}

            # Calculate incoming score
            self.incoming = float(sum(score for permu, score in selected_edges.items() if permu[1] in self.start and permu[0] == '0xb2e-start-0x31c'))

            # Remove start and end activities from selected_edges and alphabet
            tmp_selected_edges: dict[tuple: float] = selected_edges.copy()
            selected_edges = {permutation: weight for permutation, weight in selected_edges.items() 
                                if permutation[0] != '0xb2e-start-0x31c' and permutation[1] != '0x31c-end-0x1021'}
            alphabet = {act for edge in selected_edges for act in edge if act != '0xb2e-start-0x31c' and act != '0x31c-end-0x1021'}

            # error handling to ensure the building of a process tree
            if len(selected_edges) == 0 and len(alphabet) == 0:
                selected_edges = tmp_selected_edges
                alphabet = {act for edge in selected_edges for act in edge}

            # Calculate pre and post relations
            pre, post = dfg_utils.get_transitive_relations(dfg=selected_edges, alphabet=alphabet)

            # create a copy of the start and end activities
            tmp_start: set = self.start.copy()
            tmp_end: set = self.end.copy()

        else:
            # Calculate pre and post relations
            pre, post = dfg_utils.get_transitive_relations(dfg=selected_edges, alphabet=alphabet)

            # create a copy of the start activities
            tmp_start: set = self.start.copy()
            
            # remove start activities not in alphabet
            tmp_start.intersection_update(alphabet)

            # create a copy of the end activities
            tmp_end: set = self.end.copy()
            
            # remove end activities not in alphabet
            tmp_end.intersection_update(alphabet)


        # Calculate sequence set
        sequence_set: list[set] = sequence.detect(alphabet, pre, post)
        if sequence_set is not None:
            return self.build_tree(pt.ProcessTree(pt.Operator.SEQUENCE, root), sequence_set, selected_edges, pre, post)

        # Calculate xor set, can exceed recursion limit, due to the recursive nature of the function
        xor_set: list[set] = cut_detection.xor(alphabet, selected_edges)
        if xor_set is not None:
            return self.build_tree(pt.ProcessTree(pt.Operator.XOR, root), xor_set, selected_edges, pre, post)

        # Calculate and set
        and_set: list[set] = cut_detection._and(alphabet, selected_edges, tmp_start, tmp_end, incoming=float(self.incoming), epsilon_std=self.epsilon_std)
        if and_set is not None:
            return self.build_tree(pt.ProcessTree(pt.Operator.PARALLEL, root), and_set, selected_edges, pre, post)

        # Calculate loop set, can exceed recursion limit, due to the recursive nature of the function
        # create a dict with the start and end activities --> expected by pm4pys loop detection
        loop_start: dict[str: int] = {a: 1 for a in tmp_start}
        loop_end: dict[str: int] = {a: 1 for a in tmp_end}

        loop_set: list[set] = loop.detect(selected_edges, alphabet, loop_start, loop_end)
        if loop_set is not None:
            return self.build_tree(pt.ProcessTree(pt.Operator.LOOP, root), loop_set, selected_edges, pre, post, alphabet=alphabet)

        # Calculate once per trace set
        once_per_trace_set: list[set] = cut_detection.once_per_trace(alphabet, self.trace_occurences, float(self.incoming), epsilon_std=self.epsilon_std)
        if once_per_trace_set is not None:
            return self.build_tree(pt.ProcessTree(pt.Operator.PARALLEL, root), once_per_trace_set, selected_edges, pre, post)

        # Calculate strict tau loop set
        strict_tau_loop_set, selected_edges = cut_detection.strict_tau_loop(alphabet, selected_edges, tmp_start, tmp_end)
        if strict_tau_loop_set is not None:
            return self.xor_tau_loop(pt.ProcessTree(pt.Operator.XOR, root), strict_tau_loop_set, selected_edges, pre, post, alphabet)

        # Calculate tau loop set
        tau_loop_set, selected_edges = cut_detection.tau_loop(alphabet, selected_edges, tmp_start)
        if tau_loop_set is not None:
            return self.build_tree(pt.ProcessTree(pt.Operator.LOOP, root), tau_loop_set, selected_edges, pre, post, alphabet)
    
        # flower set
        return pm4py_utils.flower(alphabet, root)


    # recursive building of the Process Tree
    def build_tree(self, tree: pt.ProcessTree, cut_set: set, selected_edges: dict[tuple: float], pre: dict[str: set], post: dict[str: set], alphabet=None) -> pt.ProcessTree:
        """
        Builds a process tree based on the given cut_set. Using the selected edges, the tree is built recursively by calling the relations() function
        should the length of a subset of the cut_set be greater than one. 
        Additionally it is checked if a appended activity is a start or end activity, should that be the case the start or end set is updated accordingly
        using the successors and predecessors.

        Parameters:
            tree (pt.ProcessTree): The process tree to be built.
            cut_set (set): The set of activities to be considered for building the tree.
            selected_edges (dict[tuple: float]): The dictionary of selected edges and their scores.
            pre (dict[str: set]): The dictionary of activities and their pre-activities.
            post (dict[str: set]): The dictionary of activities and their post-activities.

        Returns:
            pt.ProcessTree: The built process tree.
        """

        viewed_acts = set()
        for permutation, score in selected_edges.items():
            for act in permutation:
                if act not in viewed_acts:
                    viewed_acts.add(act)
                    self.trace_occurences[act] = score
                else:
                    self.trace_occurences[act] += score

        # update start and end activities accordinf to the operator, as we must pay for AND & Loops extra budget
        if tree.operator != pt.Operator.XOR and tree.operator != pt.Operator.SEQUENCE:
            if self.DP:
                self.epsilon = self.epsilon /2
            self.start, self.end = start_end_iterators.start_end_loop_and_iter(cut_set=cut_set, traceList=self.traceList, start=self.start, end=self.end, epsilon=self.epsilon)

        elif tree.operator == pt.Operator.XOR:
           xor_dict: dict[str: dict] = start_end_iterators.start_end_xor_iter(cut_set=cut_set, successor=self.successor, predecessor=self.predecessor, start=self.start, end=self.end)

        elif tree.operator == pt.Operator.SEQUENCE:
            sequence_dict: dict[str: dict] = start_end_iterators.start_end_seq_iter(cut_set=cut_set, start=self.start, end=self.end, successor=self.successor, predecessor=self.predecessor)

        # check if the current operator is not a loop
        if tree.operator != pt.Operator.LOOP:

            for s in cut_set:

                # create a dfg based on the current set (branch) of the tree
                tmp_edges = list(product(s, repeat=2))
                tmp_selected_edges = {edge:selected_edges[edge] for edge in selected_edges if edge in tmp_edges}

                if len(list(s)) == 1:

                    # self loop detection
                    if len(tmp_selected_edges) == 0:
                        
                        # add a xor-tau cut to the tree if the activitys occurence is less than the expected occurence
                        if self.trace_occurences[list(s)[0]] < self.incoming -self.epsilon_std:
                           tree.children.append(self.xor_tau(pt.ProcessTree(pt.Operator.XOR, parent=tree), s, selected_edges, pre, post, alphabet))

                        # add the activity to the tree
                        else:
                            # error handling to ensure that the dummy start and end are not appended
                            if list(s)[0] != '0xb2e-start-0x31c' and list(s)[0] != '0x31c-end-0x1021':
                                tree.children.append(pt.ProcessTree(label=list(s)[0], parent=tree))
                            else:
                                tree.children.append(pt.ProcessTree(parent=tree))
                    
                    # if a self loop is detected, add a loop to the tree
                    else:
                        tree.children.append(self.relations(tmp_selected_edges, alphabet=s, root=tree))

                else:
                    # if the current cut is a sequence or xor update the start and end activities accordingly
                    if tree.operator == pt.Operator.SEQUENCE:
                        self.start = sequence_dict[str(s)]['start'].copy()
                        self.end = sequence_dict[str(s)]['end'].copy()

                    elif tree.operator == pt.Operator.XOR:
                        self.start = xor_dict[str(s)]['start'].copy()
                        self.end = xor_dict[str(s)]['end'].copy()

                    # do another iteration of the cut detection and append the created subtree to the tree
                    if len(s) > 0:
                        tree.children.append(self.relations(tmp_selected_edges, alphabet=s, root=tree))
                    else:
                        tree.children.append(pt.ProcessTree(parent=tree))

            # append 'tau' to the tree -> tau is interpreted as an empty tree
            if len(cut_set) <= 1:
                tree.children.append(pt.ProcessTree(parent=tree))

            # if the sum of occurences of the activities in the cut set is less than the expected occurence, add a tau to the tree
            elif sum(self.trace_occurences[elem] for s in cut_set for elem in s) < self.incoming -self.epsilon_std:
                tree.children.append(pt.ProcessTree(parent=tree))
                
        # if the tree is a loop, add a loop to the tree
        else:
            for s in cut_set:
                # check if only one elemt is in the current watched set
                if len(list(s)) == 1:
                    # append the activity to the tree
                    tree.children.append(pt.ProcessTree(label=list(s)[0], parent=tree))
                
                else:
                    # check which alphabet should be used for the next iteration of the cut detection
                    if len(s) > len(alphabet):
                        tree.children.append(self.relations(selected_edges, alphabet=s, root=tree))
                    elif len(s) > 0:
                        tree.children.append(self.relations(selected_edges, alphabet=alphabet, root=tree))
                    else:
                        tree.children.append(pt.ProcessTree(parent=tree))
            
            # append 'tau' to the tree -> tau is interpreted as an empty tree
            if len(cut_set) <= 1:
                tree.children.append(pt.ProcessTree(parent=tree))

        return tree


    # add a xor cut with an tau to each tau-loop
    def xor_tau_loop(self, tree, tau_loop_set, selected_edges, pre, post, alphabet) -> pt.ProcessTree:
        tree.children.append(pt.ProcessTree(parent=tree))
        tree.children.append(self.build_tree(pt.ProcessTree(pt.Operator.LOOP, tree), tau_loop_set, selected_edges, pre, post, alphabet))

        return tree

    # only add xor cut with tau when needed
    def xor_tau(self, tree, act, selected_edges, pre, post, alphabet) -> pt.ProcessTree:
        tree.children.append(pt.ProcessTree(parent=tree))
        tree.children.append(pt.ProcessTree(label=list(act)[0], parent=tree))

        return tree


if __name__ == "__main__":
    DPIM().initialization()
