import sys
import os
import json
import os
from natsort import os_sorted
from numpy.random import default_rng


def getAllGraphs(fp):
    graphs = os_sorted(os.listdir(fp))
    return [g for g in graphs if g.split('.')[-1] == 'json']

def load_graph(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['graph']

def save_graph(graph, letter, new_folder, original_filename):
    data = {
        'graph': graph,
    }
    
    filename = os.path.splitext(original_filename)[0]
    #remove "Graph_" Prefix
    if filename.startswith("Graph_"):
        filename = filename[len("Graph_"):]

    fp = os.path.join(new_folder, f"{filename}_{letter}.json")
    os.makedirs(new_folder, exist_ok=True)
    
    with open(fp, 'w') as file:
        json.dump(data, file, indent=4)


def show_progress(x, n):
    sys.stdout.write('\r')
    sys.stdout.write("[{:{}}] {:.1f}%".format("=" * x, n, (100 / n * x)))
    sys.stdout.flush()

def assign_edge_weights(instances, path_basegraph, path_instances):
    #Hyperparameter set a priori
    letters = ['a', 'b', 'c', 'd', 'e']
    min_weight = 1
    max_weight = 8

    rngSeeds = {
            'a': 2,
            'b': 73,
            'c': 179,
            'd': 283,
            'e': 419
        }

    #for loading bar
    pb_n = 100
    total = len(instances) * len(letters)
    i = 0

    print("Assign Edge Weights...")

    for g in instances:
        graph = load_graph(f'{path_basegraph}{g}')
        for letter in letters:
            rng = default_rng(rngSeeds[letter])
            seen = {}
            
            for n1, v in graph.items():
                n1 = int(n1)
                edges = []
                for n2 in v['adj']:
                    if isinstance(n2, tuple):
                        n2 = int(n2[0])  # for the case n2 is tupel
                    else:
                        n2 = int(n2)
                    e = tuple(sorted([n1, n2]))
                    w = seen.get(e, int(rng.integers(min_weight, max_weight, endpoint=True)))
                    seen[e] = w
                    edges.append((n2, w))
                v['adj'] = edges
            
            save_graph(graph, letter, path_instances, g)

            i += 1
            show_progress(int((i / total) * 100), pb_n)
            



if __name__ == "__main__":

    path_instances = 'create_instances/instances'
    path_basegraph = 'create_instances/basegraphs/'
   
    graphs = getAllGraphs(path_basegraph)
    assign_edge_weights(graphs, path_basegraph ,path_instances)


