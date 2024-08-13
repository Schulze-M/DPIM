import subprocess

import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.visualization.process_tree import visualizer as pt_visualizer


def run_non_dp(event_log):
    # read .xes file and do the necessary preprocessing
    event_log = xes_importer.apply(event_log)

    # apply inductive miner
    tree = pm4py.discover_process_tree_inductive(event_log)

    # visualize the tree
    gviz = pt_visualizer.apply(tree, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"})
    pt_visualizer.view(gviz)


if __name__ == "__main__":
    # run on event log A of the runnning example -> trace variants 1-3
    print("Event logs A and B are now generated using the Inductive Miner:")
    
    print("Event Log A:")
    
    run_non_dp("event_logs\Event_Log_A.xes")
    
    input("Press Enter to continue...")

    # run on event log B of the running example -> trace variants 4
    print("Event Log B:")
    run_non_dp("event_logs\Event_Log_B.xes")
    
    print("As one can see the process tree is different for the two event logs. \n" \
            "The process tree for Event log B introduces a loop, which is not present in the process tree for Event log A. \n" \
            "This is due to the fact that Event log B contains a single trace variant that introduces a loop. \n" \
            "This behaviour enables an attacker to infer the presence of a trace variant \n")

    input("Press Enter to continue...")

    # run event log A on the DPIM
    print("Now we run Event log A using the DPIM")

    subprocess.Popen(
        ["python3", ".\main.py", "prototype\event_logs\Event_Log_A.xes", "-e", "0.1"], cwd=".."
    ).wait()

    print("As one can see when comparing the process trees of Event log A run using the Inductive Miner and the DPIM, \n" \
            "the process trees are different. \n" \
            "The DPIM introduces noise to the process tree, which makes it harder for an attacker to infer the presence of a trace variant. \n")