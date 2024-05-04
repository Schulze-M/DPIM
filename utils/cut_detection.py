from itertools import product

from pm4py.algo.discovery.inductive.variants.im_clean import utils as pm4py_utils


def xor(alphabet: set, dfg: dict[tuple, float]) -> list[set] or None:
    """
    Finds the connected components in a graph and returns a list of sets representing the xor cut.

    Args:
        alphabet (set): The set of nodes in the graph.
        dfg (dict[tuple, float]): The directed graph represented as a dictionary of edges and weights.

    Returns:
        list[set] or None: A list of sets representing the cuts if there are multiple connected components,
                           Returns None if there is only one group.
    """
    import networkx as nx

    # Create a directed graph from the dfg, ignoring weights
    try:
        nx_dfg = nx.DiGraph()
        nx_dfg.add_nodes_from(alphabet)
        nx_dfg.add_edges_from(dfg.keys())  # the keys of the dfg are the edges
    except RecursionError:
        return None

    # Find connected components in the directed graph
    conn_comps = list(nx.strongly_connected_components(nx_dfg))

    # Convert each component to a set of nodes
    cuts = [set(nodes) for nodes in conn_comps]

    # Return the list of cuts if there are multiple components, otherwise return None
    if len(cuts) > 1:
        return cuts
    else:
        return None
        

def _and(alphabet: set, dfg: dict[tuple: float], start_acts: set, end_acts: set, incoming: float, epsilon_std: float) -> list[set] or None:
    """
    Groups the elements of the alphabet based on their relationships within a specified range of the incoming value.
    If the sum of the weights of the relationships between two elements is greater than the incoming value, the elements are merged into the same group.

    Args:
        alphabet (set): The set of elements in the alphabet.
        dfg (dict[tuple: float]): The directed graph represented as a dictionary of tuples with their corresponding weights.
        start_acts (set): The set of start activities.
        end_acts (set): The set of end activities.
        incoming (float): The incoming value.
        epsilon (float): The privacy budget, used to calculate the std.
    
    Returns:
        list[set] or None: A list of sets, where each set represents a group of elements within the specified range of the incoming value.
                           Returns None if there is only one group.
    """

    groups = [{a} for a in alphabet]
    for a, b in product(alphabet, alphabet):
        if (a, b) not in dfg or (b, a) not in dfg:
            groups = pm4py_utils.__merge_groups_for_acts(a, b, groups)
        # check if a, b have a strong relationship due to an extensive score
        elif dfg[(a, b)] + dfg[(b, a)] > incoming +epsilon_std:
            groups = pm4py_utils.__merge_groups_for_acts(a, b, groups)
        
        
    groups = sorted(groups, key=len)
    i = 0
    while i < len(groups) and len(groups) > 1:
        if any(act in start_acts for act in groups[i]) and any(act in end_acts for act in groups[i]):
            i += 1
            continue
        group = groups.pop(i)
        if i == 0:
            groups[i].update(group)
        else:
            groups[i - 1].update(group)
    
    return groups if len(groups) > 1 else None


def once_per_trace(alphabet: set, occurences: dict[str: float], incoming: float, epsilon_std: float) -> list[set] or None:
    """
    Groups the elements of the alphabet based on their occurrences within a specified range of the incoming value.

    Args:
        alphabet (set): The set of elements in the alphabet.
        occurences (dict[str: float]): A dictionary containing the occurrences of each activity in the event-log.
        incoming (float): The incoming value.
        epsilon (float): The privacy budget, used to calculate the std.

    Returns:
        list[set] or None: A list of sets, where each set represents a group of elements within the specified range of the incoming value.
                           Returns None if there is only one group.
    """
    
    groups = list()
    
    for act in alphabet:
        if incoming - epsilon_std < occurences[act] < incoming + epsilon_std:
            groups.append({act})

    observed = {act for _set in groups for act in _set}
    tmp_set = {act for act in alphabet if act not in observed}

    groups.append(tmp_set)
    
    return groups if len(groups) > 1 else None


def strict_tau_loop(alphabet: set, dfg: dict[tuple, float], start: set, end: set) -> (list[set] or None) and dict[tuple, float]:
    """
    Detects tau-loops in a directed graph and removes them from the graph.

    Args:
        alphabet (set): The set of activities in the graph.
        dfg (dict[tuple, float]): The directed graph represented as a dictionary of tuples with their corresponding weights.
        start (set): The set of start nodes in the graph.
        end (set): The set of end nodes in the graph.

    Returns:
        tuple: A tuple containing a list of groups and the updated directed graph.
            - If self-loops are detected and removed, returns a list of groups and the updated directed graph.
            - If no self-loops are detected, returns None and the original directed graph.
    """

    # self loop detection
    if len(alphabet) == 1 and len(dfg) == 1:
        return [alphabet], dfg

    # check if there is a loop present
    # if true -> remove the permutation causing the loop
    permu_to_drop = list()
    for permu in dfg:
        if permu[1] in start and permu[0] in end:
            permu_to_drop.append(permu)

    # create a new graph without the detected loops
    tmp_dfg = {permu: dfg[permu] for permu in dfg if permu not in permu_to_drop}
    
    # if the graph has been changed, return the new graph, else return None
    if len(tmp_dfg) != len(dfg):
        dfg = {permu: dfg[permu] for permu in dfg if permu not in permu_to_drop}
    else:
        return None, dfg

    # create a new group containing the activities that are not part of the loop
    group = {a for permu in dfg for a in permu}
    groups = [group]

    # return the groups and the new graph
    return groups, dfg if len(groups) > 0 else (None, dfg)


def tau_loop(alphabet: set, dfg: dict[tuple, float], start: set) -> (list[set] or None) and dict[tuple, float]:

    # check if there is a loop present
    # if true -> remove the permutation causing the loop
    permu_to_drop = list()
    for permu in dfg:
        if permu[1] in start:
            permu_to_drop.append(permu)

    # create a new graph without the detected loops
    tmp_dfg = {permu: dfg[permu] for permu in dfg if permu not in permu_to_drop}
    
    # if the graph has been changed, return the new graph, else return None
    if len(tmp_dfg) != len(dfg):
        dfg = {permu: dfg[permu] for permu in dfg if permu not in permu_to_drop}
    else:
        return None, dfg

    # create a new group containing the activities that are not part of the loop
    group = {a for permu in dfg for a in permu}
    groups = [group]

    # return the groups and the new graph
    return groups, dfg if len(groups) > 0 else (None, dfg)