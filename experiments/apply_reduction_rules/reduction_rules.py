

def update_habitats_in_graph(graph, habitatData):

    habitatData["n"] = len(habitatData["habitats"])
    #Update node in the graphs
    for node, data in graph.items():
        new_habitats = []
        # Iterate over all habitat lists in graph["habitatData"]["habitats"]
        for index, habitat_list in enumerate(habitatData["habitats"]):
            if int(node) in habitat_list:
                new_habitats.append(index)
        # Update graph[node]['habitat'] with the indices of habitats containing the node
        data['habitat'] = new_habitats

    return graph, habitatData


def red_1_1(graph, habitatData):
    #if a habitat only has one vertex, delete the habitat
    changed = False
    habitats = habitatData["habitats"]

    original_count = len(habitats)
    updated_habitats = [habitat for habitat in habitats if len(habitat) > 1]
    deleted_habitats = original_count - len(updated_habitats)

    if deleted_habitats > 0:
        changed = True

    habitatData["habitats"] = updated_habitats

    graph, habitatData = update_habitats_in_graph(graph, habitatData)

    return graph, changed, deleted_habitats, 0, 0, habitatData



def red_1_2(graph):
    #if a vertex has no habitat and degree 0 or 1 delete the vertex
    nodes_to_remove_1 = []
    nodes_to_remove_0 = []
    changed = False
    #find vertices without habitat and degree at most 1
    for node, data in graph.items():
        if len(data['habitat']) == 0:
            if len(data['adj']) == 1:
                nodes_to_remove_1.append(node)
            if len(data['adj']) == 0:
                nodes_to_remove_0.append(node)
    
    deleted_nodes = 0
    deleted_edges = 0

    for node in nodes_to_remove_1:
        adj_node = graph[str(node)]['adj'][0][0]  #adj is a list of [node ID, weight], because node only has degree 1, adj_node has to be the first in 'adj'
        graph[str(adj_node)]['adj'] = [n for n in graph[str(adj_node)]['adj'] if str(n[0]) != str(node)]

        del graph[node]
        deleted_nodes += 1
        deleted_edges += 1  

    for node in nodes_to_remove_0:
        del graph[node]
        deleted_nodes += 1

    changed = bool(nodes_to_remove_0) | bool(nodes_to_remove_1)
    return graph, changed, 0, deleted_nodes, deleted_edges



def red_1_4(graph, k, solution, habitatData):
    #Let v1, v2, v3 ∈ V , deg(v1) = 1, deg(v2) = 2 and {v1, v2}, {v2, v3} ∈ E. 
    #Furthermore let c{1,2}, c{2,3} be the costs associated with the corresponding edge.
    #has v2 no habitat delete the vertices v1, v2 and set k = k − (c{1,2} + c{2,3}).
    
    nodes_to_remove = []
    nodes = list(graph.keys())

    deleted_nodes = 0
    deleted_edges = 0
    changed = False
    #iterate over all vertices
    for i in range(len(nodes)):
        x = nodes[i]
        data_x = graph[x]

        #check if vertex v1 has habitat and degree 1
        if len(data_x['habitat']) > 0 and len(data_x['adj']) == 1:
            y = data_x['adj'][0][0] #adj is a list of [node ID, weight], because node only has degree 1, adj_node has to be the first in 'adj'
            data_y = graph[str(y)]
            
            #check if vertex v2 has no habitat and degree 2
            if len(data_y['adj']) == 2 and len(data_y['habitat']) == 0:
                
                #find v3
                if data_y['adj'][0][0] != int(x):
                    z = data_y['adj'][0][0]
                else:
                    z = data_y['adj'][1][0]

                total_edge_cost = data_y['adj'][0][1] + data_y['adj'][1][1]
                k -= total_edge_cost

                nodes_to_remove.append((x, y, z))

                deleted_nodes += 2
                deleted_edges += 2

                edge_cost = data_x['adj'][0][1]
                solution.append({'edge': (int(x), int(y)), 'weight': edge_cost})
                solution.append({'edge': (int(y), int(z)), 'weight': total_edge_cost - edge_cost})

                    
    changed = bool(nodes_to_remove)
    for x, y, z in nodes_to_remove:
        del graph[str(x)]
        if str(y) in graph: #if the graph is a path of length three it could happen, that y appears twice to be deleted
            del graph[str(y)]

        if str(z) in graph: #if the graph is a path of length three it could happen, that z is already deleted
            # Remove the edge from node z to node y
            graph[str(z)]['adj'] = [n for n in graph[str(z)]['adj'] if str(n[0]) != str(y)]

    if changed == True:
        #remove deleted vertices from habitats
        habitats = habitatData['habitats']
        updated_habitats = []
        #only remove x we know by construction, that y has no habitat
        nodes_to_remove_set = {str(x) for x, _, _ in nodes_to_remove} #hier nochmal vertesten
        for habitat in habitats:
            updated_habitat = [node for node in habitat if str(node) not in nodes_to_remove_set]
            if updated_habitat:
                updated_habitats.append(updated_habitat)

        habitatData['habitats'] = updated_habitats
        graph, habitatData = update_habitats_in_graph(graph, habitatData)

    return graph, changed, deleted_nodes, deleted_edges, k, solution, habitatData



def red_1_5(graph, k, solution, habitatData):
    #Let v1, v2, v3 ∈ V , deg(v1) = 1, deg(v2) = 2 and {v1, v2}, {v2, v3} ∈ E. 
    #Furthermore let c{1,2}, c{2,3} be the costs associated with the corresponding edge.
    #Has v2 at least one habitat delete vertex v1 and set k = k − c{1,2}.
    nodes_to_remove = []
    nodes = list(graph.keys())
    changed = False
    deleted_nodes = 0
    deleted_edges = 0
    #iterate over all vertices
    for i in range(len(nodes)):
        x = nodes[i]
        data_x = graph[x]
        #check if vertex v1 has habitat and degree 1
        if len(data_x['habitat']) > 0 and len(data_x['adj']) == 1:
            y = data_x['adj'][0][0] #adj is a list of [node ID, weight], because node only has degree 1, adj_node has to be the first in 'adj'
            data_y = graph[str(y)]
            #check if vertex v2 has a habitat and degree 2
            if len(data_y['adj']) == 2 and len(data_y['habitat']) > 0:

                edge_cost = data_x['adj'][0][1]
                k -= edge_cost

                nodes_to_remove.append((x,y))

                deleted_nodes += 1
                deleted_edges += 1
                solution.append({'edge': (int(x), int(y)), 'weight': edge_cost})

    changed = bool(nodes_to_remove)
    for x, y in nodes_to_remove:
        del graph[str(x)]
        # Remove the edge from node x to node y
        graph[str(y)]['adj'] = [n for n in graph[str(y)]['adj'] if str(n[0]) != str(x)]


    if changed == True:
        #remove deleted vertices from habitats
        habitats = habitatData['habitats']
        updated_habitats = []
        
        nodes_to_remove_set = {str(x) for x, _ in nodes_to_remove}
        for habitat in habitats:
            updated_habitat = [node for node in habitat if str(node) not in nodes_to_remove_set]
            if updated_habitat:
                updated_habitats.append(updated_habitat)

        habitatData['habitats'] = updated_habitats
        graph, habitatData = update_habitats_in_graph(graph, habitatData)

    return graph, changed, deleted_nodes, deleted_edges, k, solution, habitatData



def red_1_6(graph, k, solution, habitatData):
    #Let v1, v2 ∈ V and deg(v1) = 1. Furthermore let {v1, v2} ∈ E and c{1,2} be the costs associated with the corresponding edge.
    #If for all i ∈ {1...r} it holds that: v1 ∈ Vi ⇒ v2 ∈ Vi then delete v1 and set k = k − c{1,2}.
    nodes_to_remove = []
    deleted_nodes = 0
    deleted_edges = 0
    changed = False
    #iterate over every node
    for x, data_x in list(graph.items()):
        #check if vertex v1 has habitat and degree 1
        if len(data_x['habitat']) > 0 and len(data_x['adj']) == 1:
            y = data_x['adj'][0][0] #adj is a list of [node ID, weight], because node only has degree 1, y has to be the first in 'adj'
            data_y = graph[str(y)]
            #check if v1 ∈ Vi ⇒ v2 ∈ Vi
            if set(data_x['habitat']) <= set(data_y['habitat']):

                edge_cost = data_x['adj'][0][1]
                k -= edge_cost

                nodes_to_remove.append((x,y))

                deleted_nodes += 1
                deleted_edges += 1
                solution.append({'edge': (int(x), int(y)), 'weight': edge_cost})

    changed = bool(nodes_to_remove)
    for x, y in nodes_to_remove:
        del graph[str(x)]
        # Remove the edge from node x to node y
        graph[str(y)]['adj'] = [n for n in graph[str(y)]['adj'] if str(n[0]) != str(x)]

   
    if changed == True:
        #remove deleted vertices from habitats
        habitats = habitatData['habitats']
        updated_habitats = []
        
        nodes_to_remove_set = {str(x) for x, _ in nodes_to_remove}
        for habitat in habitats:
            updated_habitat = [node for node in habitat if str(node) not in nodes_to_remove_set]
            if updated_habitat:
                updated_habitats.append(updated_habitat)

        habitatData['habitats'] = updated_habitats
        graph, habitatData = update_habitats_in_graph(graph, habitatData)

    return graph, changed, deleted_nodes, deleted_edges, k, solution, habitatData



def red_2(graph, c_min, k):
    #if the count of edges multiplied with the minimum cost is higher than k there is no solution 
    vertex_with_habitat_count = sum(1 for node in graph.values() if 'habitat' in node and len(node['habitat']) > 0)
    if vertex_with_habitat_count * c_min > 2 * k:
        return 1
    return 0



def red_3(graph):
    #If there is an edge e ∈ E with none of the edge vertices has a habitat, then delete e.
    deleted_edges = 0
    changed = False
    #iterate over all nodes
    for node, data in list(graph.items()):
        #check if first node has no habitat
        if len(data['habitat']) == 0:
            #iterate over adjacent nodes of the first node
            for adj_node, _ in data['adj']:
                adj_data = graph[str(adj_node)]
                #check if adjacent node also has no habitats
                if (len(adj_data['habitat']) == 0):
                    graph[str(node)]['adj'] = [n for n in graph[str(node)]['adj'] if n[0] != adj_node]
                    graph[str(adj_node)]['adj'] = [n for n in graph[str(adj_node)]['adj'] if n[0] != node]

                    changed = True
                    deleted_edges += 1
    
    return graph, changed, 0, 0, deleted_edges//2



def red_5(graph, habitatData):
    changed = False
    deleted_habitats = 0
    habitats = habitatData["habitats"]

    #Sort each habitat list to ensure duplicates are detected regardless of order
    sorted_habitats = [sorted(habitat) for habitat in habitats]

    #Use a set to track unique habitats
    unique_habitats = []
    seen = set()

    for habitat in sorted_habitats:
        #Convert each habitat list to a tuple (hashable) and check for duplicates
        habitat_tuple = tuple(habitat)
        if habitat_tuple not in seen:
            seen.add(habitat_tuple)
            unique_habitats.append(habitat)
        else:
            deleted_habitats += len(habitat)
            changed = True

    #Update the graph with the unique habitats
    habitatData["habitats"] = unique_habitats

    graph, habitatData = update_habitats_in_graph(graph, habitatData)

    #Return graph and whether any duplicates were removed
    return graph, changed, deleted_habitats, 0, 0, habitatData




def red_6(graph):
    nodes_to_remove_edges = []
    changed = False
    deleted_edges = 0

    # Iterate over each node in the graph
    for x, data_x in graph.items():
        # Check if node x has no habitat and more than two adjacent nodes
        if len(data_x['habitat']) == 0 and len(data_x['adj']) > 1:
            adjacents = data_x['adj']
            for i, (adj_node, _) in enumerate(adjacents):
                adj_data = graph.get(str(adj_node))
                if len(adj_data['habitat']) > 0: #otherwise reduction rule 3 is deleting the edge
                    # Check if any habitat of the current adjacent node is also a habitat of any other adjacent node
                    common_habitat_found = False
                    for j, (other_adj_node, _) in enumerate(adjacents):
                        if i != j:
                            other_adj_data = graph.get(str(other_adj_node))
                            if len(other_adj_data['habitat']) > 0: #otherwise reduction rule 3 is deleting the edge
                                common_habitats = set(adj_data['habitat']).intersection(set(other_adj_data['habitat']))
                                if common_habitats:
                                    common_habitat_found = True
                                    break
                    # If no common habitat is found, mark the edge for removal
                    if not common_habitat_found:
                        nodes_to_remove_edges.append((x, adj_node))
                        deleted_edges += 1

    # Remove the marked edges
    if nodes_to_remove_edges:
        changed = True

    for x, adj_node in nodes_to_remove_edges:
        graph[str(x)]['adj'] = [n for n in graph[str(x)]['adj'] if n[0] != adj_node]
        graph[str(adj_node)]['adj'] = [n for n in graph[str(adj_node)]['adj'] if n[0] != int(x)]

    return graph, changed, deleted_edges  # Return the graph and deletion counts

