import gurobipy as gp
from gurobipy import GRB, LinExpr, QuadExpr
import networkx as nx
from itertools import chain, combinations
from time import time
from Solver.solver import Solver
from Solver.edge import Edge



def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

#parameters to use gurobi API, expires september 2024
options = {
    "WLSACCESSID": "c4de8d26-933e-404b-9690-0823dc9bb7ba",
    "WLSSECRET": "27554046-af94-44de-a520-8354f9125c61",
    "LICENSEID": 2531715,
}

class Solver(Solver):
    def __init__(self, fullname, path_instances):
        super().__init__(fullname, path_instances)
        self.solutionPrefix = 'Solver'
        self._gap = 0.0

    def __str__(self):
        return '2-reach Solver'

    @property
    def gap(self):
        return self._gap

    def solve_by_approximation(self, reduced):
        #for every habitat (1)calculate minimum spanning tree on powergraph, (2)resolve intermediate edges, (3)remove duplicate edges 
        res = set()
        G = self._nx_graph(reduced)

        habitats = self._habitats_reduced if reduced else self._habitats
        graph = self._G_reduced if reduced else self._G

        for h in habitats:
            S = G.subgraph(h)
            #(1)calculate minimum spanning tree on powergraph
            mst = nx.minimum_spanning_edges(S, algorithm="kruskal", data=False)
            edges = []

            #(2)resolve intermediate edges
            for u, v in mst:
                found = False
                for edge_data in graph[u]:

                    adj, weight = edge_data[:2]
                    intermediate = edge_data[2] if len(edge_data) > 2 else None

                    if adj == v:
                        if intermediate is not None:
                            weight_u_intermediate = next(
                                (w for a, w in self._original_graph[str(u)]['adj'] if a == intermediate), None)
                            weight_intermediate_v = next(
                                (w for a, w in self._original_graph[str(intermediate)]['adj'] if a == v), None)

                            if weight_u_intermediate is None or weight_intermediate_v is None:
                                raise ValueError(f"Edge weights not found in original graph for nodes {u}, {intermediate}, {v}")

                            edges.append(Edge([u, intermediate], weight_u_intermediate))
                            edges.append(Edge([intermediate, v], weight_intermediate_v))
                        else:
                            edges.append(Edge([u, v], weight))
                        found = True
                        break

                if not found: #search in the second node of the edge, this part of the code is just for safety should not be executed
                    for edge_data in graph[v]:

                        adj, weight = edge_data[:2]
                        intermediate = edge_data[2] if len(edge_data) > 2 else None

                        if adj == u:
                            if intermediate is not None:
                                weight_v_intermediate = next(
                                    (w for a, w in self._original_graph[str(v)]['adj'] if a == intermediate), None)
                                weight_intermediate_u = next(
                                    (w for a, w in self._original_graph[str(intermediate)]['adj'] if a == u), None)

                                if weight_v_intermediate is None or weight_intermediate_u is None:
                                    raise ValueError(f"Edge weights not found in original graph for nodes {v}, {intermediate}, {u}")

                                edges.append(Edge([v, intermediate], weight_v_intermediate))
                                edges.append(Edge([intermediate, u], weight_intermediate_u))
                            else:
                                edges.append(Edge([v, u], weight))
                            break

                if not found:
                    raise ValueError(f"Edge between {u} and {v} not found in the graph.")
            #(3)remove duplicate edges by using set res
            res.update(edges)
        return list(res)

    def solve_by_ilp(self, reduced):
        G = self._nx_graph(reduced)
        habitats = self._habitats_reduced if reduced else self._habitats
        
        with gp.Env(empty=True, params=options) as env:
            env.setParam('OutputFlag', 0)
            env.setParam('TimeLimit', 60000) #over 16h timelimit (is not needed on our generated instances)
            env.start()
            with gp.Model("walks_mip", env=env) as m:
                buildStart = time() #catch time needed to set up the solver
                edges = list(G.edges(data=True))
                vs = [m.addVar(vtype=GRB.BINARY, name=str(i)) for i in range(len(edges))]
                for i, (u, v, data) in enumerate(edges):
                    G[u][v]['idx'] = i

                #objective minimise total cost of edge set
                expr = LinExpr([(data['weight'], vs[i]) for i, (u, v, data) in enumerate(edges)])
                m.setObjective(expr, GRB.MINIMIZE)

                for i, h in enumerate(habitats):
                    for j, s in enumerate(powerset(h)):
                        if len(s) == 0 or len(s) == len(h):
                            continue
                        nots = [x for x in h if x not in s]

                        #constraint: two non-empty subgraphs of a habitat graph are connected by a edge
                        linear_expr = LinExpr(
                            sum(vs[G[e[0]][e[1]]['idx']]
                                for e in G.edges(s, data=True)
                                if (e[0] in s and e[1] in h and e[1] not in s) or (e[1] in s and e[0] in h and e[0] not in s))
                        )
                        #constraint: two non-empty subgraphs of a habitat graph are connected by a path of length two
                        quadratic_expr = QuadExpr(
                            sum(vs[G[e1[0]][e1[1]]['idx']] * vs[G[e2[0]][e2[1]]['idx']]
                                for e1 in G.edges(s, data=True)
                                for e2 in G.edges(nots, data=True)
                                if (e1[1] == e2[0]) or (e1[0] == e2[1]) or (e1[1] == e2[1]) or (e1[0] == e2[0]))
                        )
                        m.addConstr(linear_expr + quadratic_expr >= 1, f"c{i}_{j}")
                buildEnd = time()

                if reduced:
                    self.exact_buildTime_reduced = buildEnd - buildStart
                else:
                    self.exact_buildTime = buildEnd - buildStart

                m.optimize()

                #check if gurobi found a optimal solution, if not return a empty list
                # self._gap is a measure of how close the current solution is to being optimal
                if m.Status != GRB.OPTIMAL:
                    self._gap = m.MIPGap
                    return []

                sol = []
                for v in m.getVars():
                    if int(v.x) == 1:
                        u, v, data = edges[int(v.varName)]
                        sol.append(Edge((u, v), data['weight']))

                return sol

    def construct_powergraph(self, reduced=False):
        buildStart = time()
        #construct powergraph for approximation solver
        new_edges = {}
        edges_to_remove = []
        graph = self._G_reduced if reduced else self._G

        # Loop through all nodes
        for node_id, neighbors in graph.items():
            # Loop through adjacent nodes of the current node
            for adjacent_node, weight in neighbors:
                adjacent_node_info = graph[adjacent_node]
                
                # Loop through adjacent nodes of the adjacent node
                for adj_adj_node, adj_weight in adjacent_node_info:
                    if adj_adj_node != int(node_id):
                        # Calculate the total weight for the new edge
                        total_weight = weight + adj_weight
                        
                        # Ensure the edge is consistently represented (smaller node ID first)
                        n1, n2 = sorted([int(node_id), adj_adj_node])

                        # Check if a direct edge already exists between n1 and n2
                        direct_edge_exists = False
                        for adj in graph[n1]:
                            if adj[0] == n2 and len(adj) == 2:  # Edge without intermediate node
                                direct_edge_exists = True
                                existing_weight = adj[1]

                                # Compare weights and decide whether to replace the edge
                                if total_weight < existing_weight:
                                    # Schedule the removal of the existing edge
                                    edges_to_remove.append((n1, adj))
                                    edges_to_remove.append((n2, [n1, existing_weight]))
                                    new_edges[(n1, n2)] = [total_weight, adjacent_node]
                                break

                        # If no direct edge exists, or if the new edge is lighter, add it
                        if not direct_edge_exists:
                            if (n1, n2) not in new_edges:
                                new_edges[(n1, n2)] = [total_weight, adjacent_node]
                            else:
                                # If the edge exists in new_edges, only update if the new weight is smaller
                                existing_weight = new_edges[(n1, n2)][0]
                                if total_weight < existing_weight:
                                    new_edges[(n1, n2)] = [total_weight, adjacent_node]

        # Remove edges marked for deletion
        for n1, adj in edges_to_remove:
            if adj in graph[n1]:
                graph[n1].remove(adj)

        # Add the new edges to the selected graph (modifies _G or _G_reduced directly)
        for (n1, n2), (weight, intermediate_node) in new_edges.items():
            graph.setdefault(n1, []).append([n2, weight, intermediate_node])
            graph.setdefault(n2, []).append([n1, weight, intermediate_node])

        buildEnd = time()
        if reduced:
            self.approx_buildTime_reduced = buildEnd - buildStart
        else:
            self.approx_buildTime = buildEnd - buildStart
