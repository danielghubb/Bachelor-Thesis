import json
import sys
import copy
from reduction_rules import *

def load_graph(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['graph'], data['habitatData']

def show_progress(x, n):
    sys.stdout.write('\r')
    sys.stdout.write("[{:{}}] {:.1f}%".format("=" * x, n, (100 / n * x)))
    sys.stdout.flush()

def save_combined_graph(file_path, original_graph, modified_graph, habitatData, solution, modified_habitatData):


    data = {
        'original_graph': original_graph,
        'reduced_graph': modified_graph,
        'habitatData': habitatData,
        'reduced_habitatData': modified_habitatData,
        'solution_by_rr': solution
    }

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)



def process_graph(original_graph, output_path, c_min, k, habitatData, log_file):
    solution = [] #reduction rule 1_4, 1_5 and 1_6 choose edges which have to be part of a solution for 2-Reach GBP-C
    changed = True
    modified_graph = copy.deepcopy(original_graph)
    modified_habitatData = copy.deepcopy(habitatData)
    
    while changed:
        changed = False
        
        modified_graph, graph_changed, deleted_habitats, _, _, modified_habitatData = red_1_1(modified_graph, modified_habitatData)
        changed |= graph_changed
        total_deleted_habitats["red_1_1"] += deleted_habitats

        modified_graph, graph_changed, _, deleted_nodes, deleted_edges = red_1_2(modified_graph)
        changed |= graph_changed
        total_deleted_nodes["red_1_2"] += deleted_nodes

        modified_graph, graph_changed, deleted_nodes, deleted_edges, k, solution, modified_habitatData = red_1_4(modified_graph, k, solution, modified_habitatData)
        changed |= graph_changed
        total_deleted_nodes["red_1_4"] += deleted_nodes

        modified_graph, graph_changed, deleted_nodes, deleted_edges, k, solution, modified_habitatData = red_1_5(modified_graph, k, solution, modified_habitatData)
        changed |= graph_changed
        total_deleted_nodes["red_1_5"] += deleted_nodes

        modified_graph, graph_changed, deleted_nodes, deleted_edges, k, solution, modified_habitatData = red_1_6(modified_graph, k, solution, modified_habitatData)
        changed |= graph_changed
        total_deleted_nodes["red_1_6"] += deleted_nodes

        if red_2(modified_graph, c_min, k) == 1:
            log_file.write("red_2: 2-Reach GBP-C is a no-Instance \n")
            break

        modified_graph, graph_changed, _, _, deleted_edges = red_3(modified_graph)
        changed |= graph_changed
        total_deleted_edges["red_3"] += deleted_edges

        modified_graph, graph_changed, deleted_habitats, _, _, modified_habitatData = red_5(modified_graph, modified_habitatData)
        changed |= graph_changed
        total_deleted_habitats["red_5"] += deleted_habitats

        modified_graph, graph_changed, deleted_edges = red_6(modified_graph)
        changed |= graph_changed
        total_deleted_edges["red_6"] += deleted_edges


    save_combined_graph(output_path, original_graph, modified_graph, habitatData, solution, modified_habitatData)

if __name__ == '__main__':

    path_instances = 'create_instances/instances'

    ranges = ['4-6','6-8','8-10','10-12','12-14']
    letters = ['a', 'b', 'c', 'd', 'e']
    percentages = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    states = ['SL','NI','SN','SH','MV','ST','BB','NW','RP','HE','TH','BY','BW']


    #for loading bar
    pb_n = 100
    total = len(ranges) * len(letters) * len(percentages) * len(states)
    progress = 0

    print("\nApply Reduction Rules on Instances...")
    with open("experiments/apply_reduction_rules/reduction_rules_results.txt", 'w') as log_file:
        for i in percentages:
            total_deleted_habitats = {
                "red_1_1": 0,
                "red_5": 0
            }
            total_deleted_nodes = {
                "red_1_2": 0,
                "red_1_4": 0,
                "red_1_5": 0,
                "red_1_6": 0
            }
            total_deleted_edges = {
                "red_3": 0,
                "red_6": 0
            }

            initial_nodes = 0
            initial_edges = 0
            initial_habitats = 0

            for j in states:
                for m in ranges:
                    for l in letters:
                        input_path = f'{path_instances}/{j}_{l}_{m}_{i}density.json'
                        output_path = f'{path_instances}/{j}_{l}_{m}_{i}density.json'

                        original_graph, habitatData = load_graph(input_path)

                        initial_nodes = initial_nodes + sum(1 for _ in original_graph)
                        initial_edges = initial_edges + sum(len(data['adj']) for data in original_graph.values()) // 2
                        initial_habitats = initial_habitats + sum(len(data['habitat']) for data in original_graph.values() if 'habitat' in data)

                        #Hyperparameters such that reduction rule 2 is not triggered
                        c = 1
                        k = 10000

                        process_graph(original_graph, output_path, c, k, habitatData, log_file)

                        progress += 1
                        show_progress(int((progress / total) * 100), pb_n)
                        

            log_file.write(f"Total deletions by method for percentage {i}:\n")
            for method, count in total_deleted_nodes.items():
                log_file.write(f"  {method} - Nodes: {count} ({count / initial_nodes:.2%} of initial nodes)\n")
            for method, count in total_deleted_edges.items():
                log_file.write(f"  {method} - Edges: {count} ({count / initial_edges:.2%} of initial edges)\n")
            for method, count in total_deleted_habitats.items():
                log_file.write(f"  {method} - Habitats: {count} ({count / initial_habitats:.2%} of initial habitats)\n")
            log_file.write("\n")