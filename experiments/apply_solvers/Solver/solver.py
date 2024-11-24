import json
import os
import networkx as nx
import copy
from time import time

class Solver:
    def __init__(self, fullname, path_instances):

        self._full_name = fullname
        self._path_instances = path_instances
        data = self.__load_json()

        self._original_graph = copy.deepcopy(data['original_graph'])
        self._reduced_graph = copy.deepcopy(data['reduced_graph'])
        self._solution_by_rr = data['solution_by_rr']

        self._G = {int(k): v['adj'] for k, v in data['original_graph'].items()}
        self._G_reduced = {int(k): v['adj'] for k, v in data['reduced_graph'].items()}

        self._habitats = data['habitatData']['habitats']
        self._habitats_reduced = data['reduced_habitatData']['habitats']


    def __str__(self):
        return 'BaseSolver'
    
    def run_exact_solver(self):
        start = time()
        reduced = False
        self.exact_solution_edges = self.solve_by_ilp(reduced)
        end = time()
        self.exact_time = end - start

        start = time()
        reduced = True
        self.exact_solution_edges_reduced = self.solve_by_ilp(reduced)
        end = time()
        self.exact_time_reduced = end - start
    
    def run_approximate_solver(self):
        start = time()
        reduced = False
        self.construct_powergraph(reduced)
        self.approximate_solution_edges = self.solve_by_approximation(reduced)
        end = time()
        self.approximate_time = end - start

        start = time()
        reduced = True
        self.construct_powergraph(reduced)
        self.approximate_solution_edges_reduced = self.solve_by_approximation(reduced)
        end = time()
        self.approximate_time_reduced = end - start




    def run(self, choosen_solver):
        if choosen_solver == "Approx":
            self.run_approximate_solver()

        if choosen_solver == "Exact":
            self.run_exact_solver()

        if choosen_solver == "Both":
            self.run_exact_solver()
            self.run_approximate_solver() #hint: approximate_solver modifies self._G should run after exact_solver
            

        self.__storeSolution(choosen_solver)


    def solution(self, edges):
        return [(e.nodes[0], e.nodes[1]) for e in edges]

    def solutionCost(self, edges):
        return sum([e.weight for e in edges])

    def _nx_graph(self, reduced):
        seen = {}
        if reduced == False:
            G = nx.Graph()
            for k, v in self._G.items():
                for l in v:
                    e = (l[0], k)
                    if e in seen: continue
                    G.add_edge(k, l[0], weight=l[1])
                    seen[e] = True
            return G
        else:
            G = nx.Graph()
            for k, v in self._G_reduced.items():
                for l in v:
                    e = (l[0], k)
                    if e in seen: continue
                    G.add_edge(k, l[0], weight=l[1])
                    seen[e] = True
            return G


    def __load_json(self):
        fp = f"{self._path_instances}/{self._full_name}.json"
        if os.path.isfile(fp):
            with open(fp, 'r') as file:
                data = json.load(file)
                return data
        else:
            print(f'ERROR: {self} can not load json data. The graph file {fp} does not exist.')

    def __storeSolution(self, choosen_solver ):
        
        habitatData = {
            'n': len(self._habitats),
            'habitats': self._habitats
        }
        reduced_habitatData = {
            'n': len(self._habitats_reduced),
            'habitats': self._habitats_reduced
        }

        if choosen_solver == "Approx":
            approximation_solver = {
                'approximate_solutionCost': self.solutionCost(self.approximate_solution_edges),
                'approximate_solutionCost_reduced': self.solutionCost(self.approximate_solution_edges_reduced),

                'approximate_time': self.approximate_time ,
                'approximate_time_reduced': self.approximate_time_reduced ,

                'approx_buildTime': self.approx_buildTime ,
                'approx_buildTime_reduced': self.approx_buildTime_reduced ,

                'approximate_solution_edges': self.solution(self.approximate_solution_edges),
                'approximate_solution_edges_reduced': self.solution(self.approximate_solution_edges_reduced)
            }
            data = {
                'original_graph': self._original_graph,
                'reduced_graph': self._reduced_graph,
                'solution_by_rr': self._solution_by_rr,
                #'powergraph': self._G,
                #'powergraph_reduced': self._G_reduced,
                'habitatData': habitatData,
                'reduced_habitatData': reduced_habitatData,
                'approximation_solver': approximation_solver,
            }

        if choosen_solver == "Exact":
            exact_solver = {
                'exact_solutionCost': self.solutionCost(self.exact_solution_edges),
                'exact_solutionCost_reduced': self.solutionCost(self.exact_solution_edges_reduced),

                'exact_time': self.exact_time ,
                'exact_time_reduced': self.exact_time_reduced ,

                'exact_buildTime': self.exact_buildTime ,
                'exact_buildTime_reduced': self.exact_buildTime_reduced ,

                'exact_solution_edges': self.solution(self.exact_solution_edges),
                'exact_solution_edges_reduced': self.solution(self.exact_solution_edges_reduced)
            }
            data = {
                'original_graph': self._original_graph,
                'reduced_graph': self._reduced_graph,
                'solution_by_rr': self._solution_by_rr,
                #'powergraph': self._G,
                #'powergraph_reduced': self._G_reduced,
                'habitatData': habitatData,
                'reduced_habitatData': reduced_habitatData,
                'exact_solver': exact_solver,
            }

        if choosen_solver == "Both":
            approximation_solver = {
                'approximate_solutionCost': self.solutionCost(self.approximate_solution_edges),
                'approximate_solutionCost_reduced': self.solutionCost(self.approximate_solution_edges_reduced),

                'approximate_time': self.approximate_time ,
                'approximate_time_reduced': self.approximate_time_reduced ,

                'approx_buildTime': self.approx_buildTime ,
                'approx_buildTime_reduced': self.approx_buildTime_reduced ,

                'approximate_solution_edges': self.solution(self.approximate_solution_edges),
                'approximate_solution_edges_reduced': self.solution(self.approximate_solution_edges_reduced)
            }
            exact_solver = {
                'exact_solutionCost': self.solutionCost(self.exact_solution_edges),
                'exact_solutionCost_reduced': self.solutionCost(self.exact_solution_edges_reduced),

                'exact_time': self.exact_time ,
                'exact_time_reduced': self.exact_time_reduced ,

                'exact_buildTime': self.exact_buildTime ,
                'exact_buildTime_reduced': self.exact_buildTime_reduced ,

                'exact_solution_edges': self.solution(self.exact_solution_edges),
                'exact_solution_edges_reduced': self.solution(self.exact_solution_edges_reduced)
            }

            data = {
                'original_graph': self._original_graph,
                'reduced_graph': self._reduced_graph,
                'solution_by_rr': self._solution_by_rr,
                #'powergraph': self._G,
                #'powergraph_reduced': self._G_reduced,
                'habitatData': habitatData,
                'reduced_habitatData': reduced_habitatData,
                'approximation_solver': approximation_solver,
                'exact_solver': exact_solver,
            }


        fp = f"{self._path_instances}/{self._full_name}.json"
        with open(fp, 'w') as file:
            json.dump(data, file, indent=4)


