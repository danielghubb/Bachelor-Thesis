This repository contains the code implementations for our study on reconnecting fragmented biotopes. Below is an overview of the repository's purpose, structure, and functionality.

Overview
The objective of this repository is to provide a codebase for solving the problem of reconnecting habitats in fragmented biotopes by paths of length two.
The code models fragmented landstrips as vertices of a graph, with weighted edges representing potential green bridges and their corresponding costs. The main tasks implemented in the repository include:

Graph Modeling and Input Generation:
- Creation of graph instances based on real-world data.
- Assigning edge weights.
- Creating habitats with Random Walks


Experiments on generated Input:
- Implementation of reduction rules to simplify the graph before solving.
- Analysis of the effectivity of these reduction rules in terms of graph simplification.

- Implementation of an exact algorithm for solving the problem optimally.
- Development of an approximation algorithm to provide near-optimal solutions efficiently.


Comparison of the algorithms in terms of:
- Running time.
- Total cost of the solution.
