import random
import math
from utils import *
from greedy_algorithm import GreedyAlgorithm


class SimulatedAnnealing:
    def __init__(
        self,
        params,
        nodes,
        items,
        initial_temperature=1000,
        alpha=0.95,
        stopping_temperature=1e-3,
    ):
        self.params = params
        self.nodes = nodes
        self.items = items
        self.temperature = initial_temperature
        self.alpha = alpha
        self.stopping_temperature = stopping_temperature
        self.iteration = 1
        self.current_solution = GreedyAlgorithm(
            params, nodes, items
        ).generate_greedy_solution()
        self.best_solution = self.current_solution

    def accept_probability(self, candidate_fitness, current_fitness):
        if candidate_fitness > current_fitness:
            return 1.0
        else:
            return math.exp(
                -abs(candidate_fitness - current_fitness) / self.temperature
            )

    def run(self, iterations=100):
        while (
            self.temperature > self.stopping_temperature and self.iteration < iterations
        ):
            candidate_solution = self.mutate_solution(self.current_solution)
            candidate_fitness = fitness(
                self.params, self.nodes, self.items, candidate_solution
            )
            current_fitness = fitness(
                self.params, self.nodes, self.items, self.current_solution
            )

            if random.random() < self.accept_probability(
                candidate_fitness, current_fitness
            ):
                self.current_solution = candidate_solution
                if candidate_fitness > fitness(
                    self.params, self.nodes, self.items, self.best_solution
                ):
                    self.best_solution = candidate_solution

            self.temperature *= self.alpha
            self.iteration += 1

        return self.best_solution.fitness

    def mutate_solution(self, solution):
        new_route = solution.route.copy()
        idx1, idx2 = random.sample(range(len(new_route)), 2)
        new_route[idx1], new_route[idx2] = new_route[idx2], new_route[idx1]
        mutated_solution = Solution(new_route, solution.items.copy())
        return mutated_solution
