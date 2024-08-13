import subprocess
import time

import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.visualization.process_tree import visualizer as pt_visualizer


def run_non_dp(event_log):
    # read .xes file and do the necessary preprocessing
    event_log = xes_importer.apply(event_log)

    # apply inductive miner
    tree = pm4py.discover_process_tree_inductive(event_log)

    # visualize the tree
    gviz = pt_visualizer.apply(tree, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "pdf"})
    # pt_visualizer.save(gviz, "C:\\Users\\max\\Downloads\\log_B_simple.pdf")
    pt_visualizer.view(gviz)


if __name__ == "__main__":
    # run on event log A of the runnning example -> trace variants 1-3
    run_non_dp("prototype\event_logs\Event_Log_A.xes")
    time.sleep(5)

    # run on event log B of the running example -> trace variants 4
    run_non_dp("prototype\event_logs\Event_Log_B.xes")
    time.sleep(5)

    # run event log A on the DPIM
    subprocess.Popen(
        ["python3", "./main.py", "prototype\event_logs\Event_Log_B.xes", "-e", "0.1"]
    ).wait()