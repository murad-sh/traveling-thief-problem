class Solution:
    def __init__(
        self,
        route=[],
        items=[],
        total_profit=0,
        total_weight=0,
        total_traveling_time=0,
        fitness=0,
        total_distance=0,
    ):
        self.route = route
        self.items = items
        self.total_profit = total_profit
        self.total_weight = total_weight
        self.total_traveling_time = total_traveling_time
        self.fitness = fitness
        self.total_distance = total_distance


def calculate_distance(node1, node2):
    dx = node1[1] - node2[1]
    dy = node1[2] - node2[2]
    return (dx**2 + dy**2) ** 0.5


def avg_fitness(fitness_values):
    return sum(fitness_values) / len(fitness_values)


def best_fitness(fitness_values):
    return max(fitness_values)


def worst_fitness(fitness_values):
    return min(fitness_values)


def ksp_is_valid(total_weight, knapsack_capacity):
    return total_weight <= knapsack_capacity


def fitness(params, nodes, items, solution, greedy=False):
    max_speed = params["max_speed"]
    min_speed = params["min_speed"]
    knapsack_capacity = params["knapsack_capacity"]
    total_distance = 0
    total_profit = 0
    total_weight = 0
    total_traveling_time = 0

    for i in range(len(solution.route)):
        curr_node_index = solution.route[i] - 1
        next_node_index = solution.route[(i + 1) % len(solution.route)] - 1

        if greedy:
            curr_node_index = solution.route[i]
            next_node_index = solution.route[(i + 1) % len(solution.route)]

        curr_node = nodes[curr_node_index]
        next_node = nodes[next_node_index]
        distance = calculate_distance(curr_node, next_node)

        for item in items:
            if item[3] == curr_node_index + 1:
                if item[0] in solution.items:
                    total_profit += item[1]
                    total_weight += item[2]

        current_speed = (
            max_speed - total_weight * (max_speed - min_speed) / knapsack_capacity
        )

        total_distance += distance
        traveling_time = distance / current_speed
        total_traveling_time += traveling_time
    fitness = total_profit - total_traveling_time
    solution.total_profit = total_profit
    solution.total_weight = total_weight
    solution.total_traveling_time = total_traveling_time
    solution.total_distance = total_distance
    solution.fitness = fitness
    return fitness
