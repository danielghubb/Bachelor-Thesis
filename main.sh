#!/bin/bash

# assign edge weights to the initial graphs
python3 create_instances/assign_edge_weights.py

# generate habitats by random walks
python3 create_instances/assign_random_walks.py

# apply reduction rules. The original graph is not overwritten
python3 experiments/apply_reduction_rules/apply_reduction_rules.py

# solve 2-Reach GBP on instances. Use argument "Approx", "Exact" or "Both" to select a solver
python3 experiments/apply_solvers/apply_solvers.py "Both"

#visualize results
python3 experiments/analyse_results/analyse_results.py