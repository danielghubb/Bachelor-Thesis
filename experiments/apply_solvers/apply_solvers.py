import os
import sys
from enum import Enum
from natsort import os_sorted

from Solver.solving_logic import Solver


def getAllGraphs(fp):
    graphs = os_sorted(os.listdir(fp))
    # Filter out only `.json` files and remove the extension
    return [g.split('.')[0] for g in graphs if g.endswith('.json')]
    
def show_progress(x, n):
    sys.stdout.write('\r')
    sys.stdout.write("[{:{}}] {:.1f}%".format("=" * x, n, (100 / n * x)))
    sys.stdout.flush()

def solveInstances(instances, path_instances, choosen_solver):
    #for loading bar
    pb_n = 100
    total = len(instances)
    progress = 0

    print("\nApply Approximate and/or Exact Solver on Instances...")
    for inst in enumerate(instances):
        inst = inst[1].split('.')[0]
        solver = Solver(inst, path_instances)
        solver.run(choosen_solver)

        progress += 1
        show_progress(int((progress / total) * 100), pb_n)


if __name__ == '__main__':

    path_instances = 'create_instances/instances'
    choosen_solver = sys.argv[1]

    if choosen_solver != "Both" and choosen_solver !="Exact" and choosen_solver !="Approx":
        print("Please choose Approx, Exact or Both as second argument")
        sys.exit(0)

    graphs = getAllGraphs(path_instances)

    solveInstances(graphs, path_instances, choosen_solver)

