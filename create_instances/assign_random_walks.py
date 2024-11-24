import sys
import os
import json
import os
import copy
from typing import List
from natsort import os_sorted
from numpy.random import default_rng


def getAllGraphs(fp):
    graphs = os_sorted(os.listdir(fp))
    return [g for g in graphs if g.split('.')[-1] == 'json']

def load_graph(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['graph']

def save_graph(graph,habitats, h, d, new_folder, original_filename):
    habitatData ={}
    habitatData = {
            'n': len(habitats),
            'habitats': habitats,
        }
    data = {
            'graph': graph,
            'habitatData': habitatData
        }
    filename = os.path.splitext(original_filename)[0]

    fp = os.path.join(new_folder, f"{filename}_{h[0]}-{h[2]}_{d}density.json")
    os.makedirs(new_folder, exist_ok=True)
    with open(fp, 'w') as file:
        json.dump(data, file, indent=4)

def show_progress(x, n):
    sys.stdout.write('\r')
    sys.stdout.write("[{:{}}] {:.1f}%".format("=" * x, n, (100 / n * x)))
    sys.stdout.flush()


def clean_up_instance_folder(folder_path):
    #the instance folder contains the original graphs without habitats. These are no longer needed and removed
    #we distinguish by suffix of the file name
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not filename.endswith('density.json'):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")



def create_powergraph(graph):
    #for every vertex find the adjacent to adjacent vertices. Duplicates are removed.
    #combine with adjacent vertices and again remove duplicates. for random walk now every vertex has the same chance to be choosen.
    for node_id, node_info in graph.items():
        adjacent_of_adjacent = set()
        for adjacent_node, _ in node_info['adj']:  # ignore weights
            adjacent_node_info = graph[str(adjacent_node)]
            for adj_adj_node, _ in adjacent_node_info['adj']:  # ignore weights
                if adj_adj_node != int(node_id):
                    adjacent_of_adjacent.add(adj_adj_node)
        
        combined_adj = {adj[0] for adj in node_info['adj']}  # Take only the first value (node ID)
        combined_adj.update(adjacent_of_adjacent)  # Add second-degree neighbors
        
        # Convert back to a list of single-element lists
        node_info['adj_d2'] = [[adj_node] for adj_node in sorted(combined_adj)]

    return graph

def save_habitats_in_graph(graph, habitat_data):
    for v in graph.values():
        v['habitat'] = []
    
    #every vertex gets a habitat argument
    for h, habitat in enumerate(habitat_data):
        if isinstance(habitat, int):
            habitat = [habitat]
        for n in habitat:
            graph[str(n)]['habitat'].append(h)

    # Remove 'adj_d2' from every node in the graph
    for node_id, node_info in graph.items():
        if 'adj_d2' in node_info:
            del node_info['adj_d2']
    
    return graph

def random_walk(G, start, steps, rng) -> List[int]:
    if len(G) <= steps:
        return [int(k) for k in G]
    nodes = [start]
    while steps > 0:
        current_index = rng.integers(0, len(nodes))
        c = nodes[current_index]
        next_index = rng.integers(0, len(G[str(c)]['adj_d2']))
        n = G[str(c)]['adj_d2'][next_index][0]
        if n not in nodes:
            nodes.append(n)
            steps -= 1
    return nodes

def assign_random_walk(graph, habitat_size, d, seed):
    G = copy.deepcopy(graph)
    if not G:
        return
    
    rng = default_rng(seed)
    habitats = []
    nodes_with_habitats = set()
    total_nodes = len(G)

    threshold = int(total_nodes * (d / 100.0))

    while len(nodes_with_habitats) < threshold:
        steps = int(rng.integers(min(habitat_size), max(habitat_size), endpoint=True)) - 1
        start_node = int(rng.integers(0, total_nodes))
        nodes = random_walk(G, start_node, steps, rng)
        habitats.append(nodes)
        nodes_with_habitats.update(nodes)
     
    return habitats
    


def assign_random_walks(graphs, path_instances):
    #hyperparameters are set a priori
    habitat_size = [[j for j in range(i, i + 3)] for i in range(4, 14, 2)] #habitat sizes [[4, 5, 6], [6, 7, 8], [8, 9, 10], [10, 11, 12], [12, 13, 14]]
    density = [10, 20, 30, 40, 50, 60, 70, 80, 90]

    #for loading bar
    pb_n = 100
    total = len(graphs) * len(habitat_size) * len(density)
    i = 0
    print("\nGenerate Random Walk Instances...")

    for g in graphs:
        for h in habitat_size:
            for d in density:
                graph = load_graph(f'{path_instances}/{g}')
                graph = create_powergraph(graph)
                habitats = assign_random_walk(graph, h, d, i)
                graph = save_habitats_in_graph(graph, habitats)

                save_graph(graph, habitats, h, d, path_instances, g)

                i += 1
                show_progress(int((i / total) * 100), pb_n)

if __name__ == "__main__":

    path_instances = 'create_instances/instances'
    
    graphs = getAllGraphs(path_instances)
    assign_random_walks(graphs, path_instances)
    clean_up_instance_folder(path_instances)
