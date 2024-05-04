from itertools import product

import numpy as np

from utils.utils import add_laplace_noise


def start_end_loop_and_iter(cut_set: list[set], traceList: list[list[tuple]], start: set, end: set, epsilon: float) -> set and set:
    """
    Calcutes the start and end activities for a loop/and and modifies the traceList accordingly. For this several steps are performed, to ensure 
    that the start and end activities are correctly calculated.
    
    Args:
        cut_set (list[set]): The set of activities to be cut.
        traceList (list[list[tuple]]): The list of traces.
        start (set): The set of current start activities.
        end (set): The set of current end activities.
        
    Returns:
        tuple: A tuple containing the calculated start and end activities.
    """

    tmp_traceList = traceList.copy()
    tmp_traceList = np.array(tmp_traceList, dtype=object).flatten()
    tmp_traceList = np.unique(tmp_traceList)

    alphabet = {a for s in cut_set for a in s}
    # error handling to avoid division by zero
    if len(alphabet) <= 0:
        return start, end

    # create permuatations of the alphabet
    tmp_permuatations = list(product(alphabet, repeat=2))

    # remove sall permutations of a trace that are not part of the cut set
    for i in range(len(tmp_traceList)):
        tmp_traceList[i] = [permu for permu in tmp_traceList[i] if permu in tmp_permuatations]

    elems_to_drop_start = [list(a)[0] for a in cut_set if len(a) == 1 and list(a)[0] in start]
    elems_to_drop_end = [list(a)[0] for a in cut_set if len(a) == 1 and list(a)[0] in end]
    
    # error handling: if no elements to drop, return, since no start and end activities are affected
    if (len(elems_to_drop_start) + len(elems_to_drop_end)) == 0:
        return start, end
    
    elif len(elems_to_drop_start) > 0 and len(elems_to_drop_end) == 0:
        # initialize a temporary start dictionary
        tmp_start = {a: 0 for a in alphabet}

        # update the start activities, the score is incremented by 1 for each activity if it is a new start activity
        for i in range(len(tmp_traceList)):
            if len(tmp_traceList[i]) > 1 and tmp_traceList[i][0][0] in elems_to_drop_start:
                tmp_start.update({tmp_traceList[i][1][0]: tmp_start.get(tmp_traceList[i][1][0], 0) + 1})
            elif len(tmp_traceList[i]) == 1 and tmp_traceList[i][0][0] in elems_to_drop_start:   
                tmp_start.update({tmp_traceList[i][0][1]: tmp_start.get(tmp_traceList[i][0][1], 0) + 1})

        # add laplace noise to the start activities
        for elem, score in tmp_start.items():
            tmp_start[elem] = add_laplace_noise(score, 1, epsilon/2)

        # remove the elements to drop from the start activities
        for elem in elems_to_drop_start:
            start.remove(elem)

        # update the start activities with the new start activities
        union_set = {a for a, score in tmp_start.items() if score > np.sqrt(2)*2*1/((epsilon/4))}

        start.update(union_set)

        return start, end

    elif len(elems_to_drop_start) == 0 and len(elems_to_drop_end) > 0:
        # initialize a temporary end dictionary
        tmp_end = {a: 0 for a in alphabet}

        # update the end activities, the score is incremented by 1 for each activity if it is a new end activity
        for i in range(len(tmp_traceList)):
            if len(tmp_traceList[i]) > 1 and tmp_traceList[i][-1][1] in elems_to_drop_end:
                tmp_end.update({tmp_traceList[i][-2][1]: tmp_end.get(tmp_traceList[i][-2][1], 0) + 1})
            elif len(tmp_traceList[i]) == 1 and tmp_traceList[i][0][1] in elems_to_drop_end:
                tmp_end.update({tmp_traceList[i][-1][0]: tmp_end.get(tmp_traceList[i][0][0], 0) + 1})

        # add laplace noise to the end activities
        for elem, score in tmp_end.items():
            tmp_end[elem] = add_laplace_noise(score, 1, epsilon/2)

        # remove the elements to drop from the end activities
        for elem in elems_to_drop_end:
            end.remove(elem)

        # update the end activities with the new end activities
        union_set = {a for a, score in tmp_end.items() if score > np.sqrt(2)*2*1/((epsilon/4))}
        
        end.update(union_set)

        return start, end

    else:
        # initialize a temporary start and end dictionary
        tmp_start = {a: 0 for a in alphabet}
        tmp_end = {a: 0 for a in alphabet}

        # update the start and end activities, the score is incremented by 1 for each activity if it is a new start or end activity
        for i in range(len(tmp_traceList)):
            if len(tmp_traceList[i]) > 1 and tmp_traceList[i][0][0] in elems_to_drop_start:
                tmp_start.update({tmp_traceList[i][1][0]: tmp_start.get(tmp_traceList[i][1][0], 0) + 1})
            elif len(tmp_traceList[i]) == 1 and tmp_traceList[i][0][0] in elems_to_drop_start:
                tmp_start.update({tmp_traceList[i][0][1]: tmp_start.get(tmp_traceList[i][0][1], 0) + 1})

            elif len(tmp_traceList[i]) > 1 and tmp_traceList[i][-1][1] in elems_to_drop_end:
                tmp_end.update({tmp_traceList[i][-2][1]: tmp_end.get(tmp_traceList[i][-2][1], 0) + 1})
            elif len(tmp_traceList[i]) == 1 and tmp_traceList[i][0][1] in elems_to_drop_end:
                tmp_end.update({tmp_traceList[i][-1][0]: tmp_end.get(tmp_traceList[i][0][0], 0) + 1})

        # add laplace noise to the start and end activities
        for elem, score in tmp_start.items():
            tmp_start[elem] = add_laplace_noise(score, 1, epsilon/2)

        for elem, score in tmp_end.items():
            tmp_end[elem] = add_laplace_noise(score, 1, epsilon/2)

        # remove the elements to drop from the start and end activities
        for elem in elems_to_drop_start:
            start.remove(elem)

        for elem in elems_to_drop_end:
            end.remove(elem)

        # update the start and end activities with the new start and end activities
        union_start_set = {a for a, score in tmp_start.items() if score > np.sqrt(2)*2*1/((epsilon/4))}
        union_end_set = {a for a, score in tmp_end.items() if score > np.sqrt(2)*2*1/((epsilon/4))}

        start.update(union_start_set)
        end.update(union_end_set)

        return start, end


def start_end_xor_iter(cut_set: list[set], successor: dict[str: set], predecessor: dict[str: set], start: set, end: set) -> dict[str: dict]:
    """
    Calculates the start and end sets for each element (branch) in the cut_set using the successors and predessors.

    Args:
        cut_set (list[set]): The list of sets representing the cut sets.
        successor (dict[str: set]): The successor dictionary.
        predecessor (dict[str: set]): The predecessor dictionary.
        start (set): The start set.
        end (set): The end set.

    Returns:
        dict[str: dict]: A dictionary containing the start and end sets for each element (branch) in the cut_set.
    """

    xor_dict = dict() 
    tmp_cut_set = cut_set.copy()

    alphabet = {a for s in cut_set for a in s}

    # iterate over the cut set and calculate the start and end sets for each element (branch) in the cut set
    for i in range(len(tmp_cut_set)):
        # in each step only view those activities that are not in the current cut set
        tmp_alphabet = alphabet.copy()
        tmp_alphabet.difference_update(tmp_cut_set[i])

        # remove the activities that are not in the current cut set from the start and end sets
        tmp_start = start.copy()
        tmp_start.intersection_update(tmp_cut_set[i])

        tmp_end = end.copy()
        tmp_end.intersection_update(tmp_cut_set[i])

        # update the start and end activities based on the predecessors and successors. Only consider the activities that are in the current cut set
        for act in tmp_alphabet:
            if act in successor:
                tmp_start.update(successor[act].intersection(alphabet.intersection(tmp_cut_set[i])))

        for act in tmp_cut_set[i]:
            if act in predecessor:
                tmp_end.update(predecessor[act].intersection(alphabet.intersection(tmp_cut_set[i])))

        xor_dict.update({str(tmp_cut_set[i]): {'start': tmp_start, 'end': tmp_end}})

    return xor_dict


def start_end_seq_iter(cut_set: list[set], start: set, end: set, successor: dict[str: set], predecessor: dict[str: set]) -> dict[str: dict]:
    """
    Calculates the start and end sets for each element (branch) in the cut_set using the successors and predessors.

    Args:
        cut_set (list[set]): The cut set.
        start (set): The start set.
        end (set): The end set.
        successor (dict[str: set]): The successor dictionary.
        predecessor (dict[str: set]): The predecessor dictionary.

    Returns:
        dict[str: dict]: A dictionary containing the start and end sets for each element (branch) in the cut_set.
    """
    
    sequence_dict = dict()
    tmp_cut_set = cut_set.copy()

    # check if the cut set contains only two elements. This is done because 2 elements are the minimum for a sequence 
    # and also this is a special case (possible IndexError if not handled properly)
    if len(tmp_cut_set) == 2:
        # iterate over the elements in the cut set
        for i in range(len(tmp_cut_set)):
            # check if is the first element in the cut set
            if i == 0:
                # remove all elements from the start and end sets that are not in the current cut set
                tmp_start = start.copy()
                tmp_start.intersection_update(tmp_cut_set[i])

                tmp_end = end.copy()
                tmp_end.intersection_update(tmp_cut_set[i])

                # update the end activities based on the predecessors of the next set in the cut set
                # it is sufficient to only update the end activities, since the start activities are already included in the first set
                for act in tmp_cut_set[i+1]:
                    tmp_pred: set = predecessor[act].copy()

                    tmp_pred.intersection_update(tmp_cut_set[i])

                    if len(tmp_pred) > 0:
                        tmp_end.update(tmp_pred)

                # update the dict for this element (branch) in the cut set
                sequence_dict.update({str(tmp_cut_set[i]): {'start': tmp_start, 'end': tmp_end}})

            else:
                # remove all elements from the start and end sets that are not in the current cut set
                tmp_start = start.copy()
                tmp_start.intersection_update(tmp_cut_set[i])

                tmp_end = end.copy()
                tmp_end.intersection_update(tmp_cut_set[i])

                # update the start activities based on the successors of the previous set in the cut set
                # it is sufficient to only update the start activities, since the end activities are already included in the last set
                for act in sequence_dict[str(tmp_cut_set[i-1])]['end']:
                    tmp_start.update(tmp_cut_set[i].intersection(successor[act]))

                # update the dict for this element (branch) in the cut set
                sequence_dict.update({str(tmp_cut_set[i]): {'start': tmp_start, 'end': tmp_end}})

        return sequence_dict

    else:
        # iterate over the elements in the cut set
        for i in range(len(tmp_cut_set)):
            # check if is the first element in the cut set
            if i == 0:
                # remove all elements from the start and end sets that are not in the current cut set
                tmp_start = start.copy()
                tmp_start.intersection_update(tmp_cut_set[i])

                tmp_end = end.copy()
                tmp_end.intersection_update(tmp_cut_set[i])

                # update the end activities based on the predecessors of the next set in the cut set
                # it is sufficient to only update the end activities, since the start activities are already included in the first set
                for j in range(i+1, len(tmp_cut_set)):
                    for act in tmp_cut_set[j]:
                        tmp_pred: set = predecessor[act].copy()

                        tmp_pred.intersection_update(tmp_cut_set[i])

                        if len(tmp_pred) > 0:
                            tmp_end.update(tmp_pred)

                # update the dict for this element (branch) in the cut set
                sequence_dict.update({str(tmp_cut_set[i]): {'start': tmp_start, 'end': tmp_end}})

            else:
                # remove all elements from the start set that are not in the current cut set
                tmp_start = start.copy()
                tmp_start.intersection_update(tmp_cut_set[i])

                # update the start activities based on the successors of the previous set in the cut set
                for act in sequence_dict[str(tmp_cut_set[i-1])]['end']:
                    tmp_start.update(tmp_cut_set[i].intersection(successor[act]))

                # remove all elements from the end set that are not in the current cut set
                tmp_end = end.copy()
                tmp_end.intersection_update(tmp_cut_set[i])

                # update the end activities based on the predecessors of the next set in the cut set
                for j in range(i+1, len(tmp_cut_set)):
                    for act in tmp_cut_set[j]:
                        tmp_pred: set = predecessor[act].copy()

                        tmp_pred.intersection_update(tmp_cut_set[i])

                        if len(tmp_pred) > 0:
                            tmp_end.update(tmp_pred)

                # update the dict for this element (branch) in the cut set
                sequence_dict.update({str(tmp_cut_set[i]): {'start': tmp_start, 'end': tmp_end}})

        return sequence_dict