import random
import os
from utils import *
from file_handler import log_statistics
from greedy_algorithm import GreedyAlgorithm
from random_search import RandomSearch


class EvolutionaryAlgorithm:
    def __init__(
        self,
        params,
        nodes,
        items,
        population_size=100,
        generations=100,
        crossover_rate=0.7,
        mutation_rate=0.01,
        tournament_size=5,
        filename=None,
        log_statistics=False,
    ):
        self.params = params
        self.nodes = nodes
        self.items = items
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.population = []
        self.stats = {"best": [], "avg": [], "worst": []}
        self.log_statistics = log_statistics
        self.filename = f"/Users/murad-sh/Private/TTP/results/{filename}.csv"
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def initialize_population(self):
        # Split the population initialization between greedy(80%) and random(20%) solutions
        greedy_count = int(self.population_size * 0.8)
        random_count = self.population_size - greedy_count

        for _ in range(greedy_count):
            solution = GreedyAlgorithm(
                self.params, self.nodes, self.items
            ).generate_greedy_solution()
            self.population.append(solution)

        for _ in range(random_count):
            solution = RandomSearch(
                self.params, self.nodes, self.items
            ).generate_random_solution()
            self.population.append(solution)

        for solution in self.population:
            fitness(self.params, self.nodes, self.items, solution)

    def tournament_selection(self):
        contenders = random.sample(self.population, self.tournament_size)
        best = max(contenders, key=lambda x: x.fitness)
        return best

    def crossover_ox(self, parent1, parent2):
        size = min(len(parent1.route), len(parent2.route))
        cx1, cx2 = sorted(random.sample(range(size), 2))

        child_route = [None] * size

        for i in range(cx1, cx2 + 1):
            child_route[i] = parent1.route[i]

        p2_index = 0
        for i in range(size):
            if child_route[i] is None:
                while parent2.route[p2_index] in child_route:
                    p2_index += 1
                child_route[i] = parent2.route[p2_index]

        child = Solution(child_route)
        child.items = random.choice([parent1.items, parent2.items])
        return child

    def calculate_generation_stats(self):
        gen_fitness = [solution.fitness for solution in self.population]
        self.stats["best"].append(best_fitness(gen_fitness))
        self.stats["avg"].append(avg_fitness(gen_fitness))
        self.stats["worst"].append(worst_fitness(gen_fitness))

    def swap_mutation(self, solution):
        idx1, idx2 = random.sample(range(len(solution.route)), 2)
        solution.route[idx1], solution.route[idx2] = (
            solution.route[idx2],
            solution.route[idx1],
        )
        return solution

    def run(self):
        self.initialize_population()

        for generation in range(self.generations):
            new_population = []
            for _ in range(self.population_size):
                # Selection
                parent1, parent2 = (
                    self.tournament_selection(),
                    self.tournament_selection(),
                )

                # Cross-over
                if random.random() < self.crossover_rate:
                    child = self.crossover_ox(parent1, parent2)
                else:
                    child = random.choice([parent1, parent2])

                # Mutation
                if random.random() < self.mutation_rate:
                    child = self.swap_mutation(child)
                fitness(self.params, self.nodes, self.items, child)
                new_population.append(child)

            # Elitism
            self.population = sorted(
                self.population + new_population, key=lambda x: x.fitness, reverse=True
            )[: self.population_size]
            self.calculate_generation_stats()
            if log_statistics:
                log_statistics(
                    self.filename,
                    generation + 1,
                    {
                        "best": self.stats["best"][-1],
                        "average": self.stats["avg"][-1],
                        "worst": self.stats["worst"][-1],
                    },
                )
        return max(self.stats["best"])
