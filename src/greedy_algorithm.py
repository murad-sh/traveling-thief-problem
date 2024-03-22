import random
from utils import *


class GreedyAlgorithm:
    def __init__(self, params, nodes, items):
        self.params = params
        self.nodes = {i + 1: node for i, node in enumerate(nodes)}
        self.items = items
        self.fitness_values = []
        self.best_solution = None
        self.worst_solution = None
        self.avg_solution = None

    def nearest_neighbor(self):
        nodes = self.nodes
        visited_nodes = set()
        route = []
        node_indices = list(nodes.keys())
        random_starting_node = random.choice(node_indices)
        current_node = random_starting_node

        route.append(current_node)
        visited_nodes.add(current_node)

        while len(visited_nodes) < len(nodes):
            closest_node = None
            closest_distance = float("inf")

            for next_node, _ in nodes.items():
                if next_node not in visited_nodes:
                    distance = calculate_distance(nodes[current_node], nodes[next_node])
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_node = next_node

            if closest_node is not None:
                route.append(closest_node)
                visited_nodes.add(closest_node)
                current_node = closest_node

        return route

    def select_best_items(self, solution):
        total_weight = 0
        items_selected = [-1] * len(solution.route)

        for route_index, node_index in enumerate(solution.route):
            node_items = [item for item in self.items if item[3] == node_index]

            most_valuable_item = None
            highest_ratio = -1

            for item in node_items:
                _, item_profit, item_weight, _ = item
                ratio = item_profit / item_weight
                if ratio > highest_ratio and ksp_is_valid(
                    total_weight + item_weight, self.params["knapsack_capacity"]
                ):
                    most_valuable_item = item
                    highest_ratio = ratio
                    selected_item_profit = item_profit
                    selected_item_weight = item_weight

            if most_valuable_item is not None:
                total_weight += selected_item_weight
                solution.total_weight += selected_item_weight
                solution.total_profit += selected_item_profit
                items_selected[route_index] = most_valuable_item[0]

        return items_selected

    def run(self, iterations=100):
        for _ in range(iterations):
            solution = self.generate_greedy_solution()
            fitness_value = fitness(
                self.params, self.nodes, self.items, solution, greedy=True
            )
            self.fitness_values.append(fitness_value)

        self.best_solution = best_fitness(self.fitness_values)
        self.worst_solution = worst_fitness(self.fitness_values)
        self.avg_solution = avg_fitness(self.fitness_values)
        return self.best_solution

    def generate_greedy_solution(self):
        route = self.nearest_neighbor()
        solution = Solution(route)
        solution.items = self.select_best_items(solution)
        return solution
