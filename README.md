# Traveling Thief Problem (TTP) Solutions

This repository contains implementations for solving the Traveling Thief Problem (TTP), a complex optimization problem that combines elements of the Knapsack Problem and the Traveling Salesman Problem.

## Implemented Algorithms

- **Random Search**: A basic approach that generates random solutions, evaluating them to find the best one.
- **Greedy Algorithm**: Utilizes a nearest-neighbor strategy for route selection and item picking based on value-weight ratio.
- **Simulated Annealing (SA)**: Starts with a solution generated by the Greedy Algorithm and tries to improve it through a process simulating the annealing of metals.
- **Evolutionary Algorithm (EA)**: Begins with an initial population of solutions generated by Greedy and Random Search methods, then applies genetic operations such as selection, crossover, and mutation to evolve towards better solutions.
