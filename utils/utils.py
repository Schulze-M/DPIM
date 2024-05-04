import numpy as np


def get_pred_succ(selected_edges: dict[tuple: float]) -> dict[str: set] and dict[str: set]:
    """
    Get the predecessors and successors of nodes in the graph based on the selected edges.

    Parameters:
        selected_edges (dict[tuple: float]): The dictionary of selected edges with their weights.

    Returns:
        tuple: A tuple containing two dictionaries - pred and succ.
            pred (dict[str: set]): The dictionary of nodes and their direct predecessors.
            succ (dict[str: set]): The dictionary of nodes and their direct successors.
    """

    pred = dict()
    succ = dict()
    
    # initialize the predecessors and successors of each node
    for a, b in list(selected_edges.keys()):
        succ.update({a: set()})
        succ.update({b: set()})
        
        pred.update({a: set()})
        pred.update({b: set()})
        
    # get the direct predecessors and successors of each node
    for a, b in list(selected_edges.keys()):
        succ[a].add(b)
        pred[b].add(a)

    return pred, succ


def get_start_end(cut_set: list[set], start_set: set, end_set: set, pred: dict[str: set], succ: dict[str: set]) -> dict[str: set] and dict[str: set]:
    """
    Returns the start and end sets based on the given cut set, start set, end set, predecessor dictionary, and successor dictionary.

    Parameters:
        cut_set (list[set]): A list of sets representing the cut set.
        start_set (set): The set of starting elements.
        end_set (set): The set of ending elements.
        pred (dict[str: set]): A dictionary mapping elements to their predecessor sets.
        succ (dict[str: set]): A dictionary mapping elements to their successor sets.

    Returns:
        tuple: A tuple containing two dictionaries. The first dictionary represents the start set, and the second dictionary represents the end set.
    """
    
    start = set()
    end = set()

    for group in cut_set:
        if len(group) == 1:
            if list(group)[0] in start_set:
                start.update(succ[list(group)[0]])

            if list(group)[0] in end_set:
                end.update(pred[list(group)[0]])

    # error handling, as the start and end sets should not be empty
    # can happen if all groups are > 1
    if len(start) > 0 and len(end) > 0:
        return start, end
    
    elif len(start) == 0 and len(end) > 0:
        return start_set, end

    elif len(start) > 0 and len(end) == 0:
        return start, end_set

    elif len(start) == 0 and len(end) == 0:
        return start_set, end_set
    

def add_laplace_noise(original_value: float, sensitivity: float, epsilon: float) -> float:
    """
    Adds Laplace noise to the given original value.

    Parameters:
        original_value (float): The original value to which noise is added.
        sensitivity (float): The sensitivity of the original value.
        epsilon (float): The privacy budget.

    Returns:
        float: The original value with added Laplace noise.
    """
    scale = sensitivity / epsilon
    noise = np.random.laplace(0., scale)

    noised_val = original_value + noise

    # return the noised value
    return noised_val