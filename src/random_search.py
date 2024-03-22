import random
from utils import *


class RandomSearch:
    def __init__(self, params, nodes, items):
        self.params = params
        self.nodes = nodes
        self.items = items
        self.fitness_values = []
        self.best_solution = None
        self.worst_solution = None
        self.avg_solution = None

    def generate_random_solution(self):
        route = list(range(1, len(self.nodes) + 1))
        random.shuffle(route)

        items_selected = [-1] * len(self.items)
        total_weight = 0

        for node_id in route:
            node_items = [item for item in self.items if item[3] == node_id]
            for item in node_items:
                if random.random() < 0.5:
                    item_index, _, item_weight, _ = item
                    new_total_weight = total_weight + item_weight

                    if ksp_is_valid(new_total_weight, self.params["knapsack_capacity"]):
                        items_selected[item_index - 1] = item_index
                        total_weight = new_total_weight
                        break

        return Solution(route, items_selected)

    def run(self, iterations=100):
        for _ in range(iterations):
            solution = self.generate_random_solution()
            fitness_value = fitness(self.params, self.nodes, self.items, solution)
            solution.fitness = fitness_value
            self.fitness_values.append(fitness_value)

        self.best_solution = best_fitness(self.fitness_values)
        self.worst_solution = worst_fitness(self.fitness_values)
        self.avg_solution = avg_fitness(self.fitness_values)

        return self.best_solution
