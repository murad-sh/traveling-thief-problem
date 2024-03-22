import os
from utils import best_fitness, worst_fitness, avg_fitness
from file_handler import read_file, log_results
from random_search import RandomSearch
from greedy_algorithm import GreedyAlgorithm
from evolutionary_algorithm import EvolutionaryAlgorithm
from simulated_annealing import SimulatedAnnealing


folder = "/Users/murad-sh/Private/TTP/data"
files = os.listdir(folder)
file_number = 4

if len(files) > 0:
    file = files[file_number]
    file_path = os.path.join(folder, file)

results_dir = "/Users/murad-sh/Private/TTP/results"
params, nodes, items = read_file(file_path)

print("Random Search")
random_search_algorithm = RandomSearch(params, nodes, items)
best_solution = random_search_algorithm.run()
print("Best: ", random_search_algorithm.best_solution)
print("Worst: ", random_search_algorithm.worst_solution)
print("Avg: ", random_search_algorithm.avg_solution)
log_results(
    results_dir,
    file,
    "Random Search",
    random_search_algorithm.best_solution,
    random_search_algorithm.worst_solution,
    random_search_algorithm.avg_solution,
)
print()


print("Greedy Algorithm")
greedy_algorithm = GreedyAlgorithm(params, nodes, items)
solution = greedy_algorithm.run()
print("Best: ", greedy_algorithm.best_solution)
print("Worst: ", greedy_algorithm.worst_solution)
print("Avg: ", greedy_algorithm.avg_solution)
log_results(
    results_dir,
    file,
    "Greedy Algorithm",
    greedy_algorithm.best_solution,
    greedy_algorithm.worst_solution,
    greedy_algorithm.avg_solution,
)
print()

print("Evolutionary Algorithm")
evolutionary_algorithm = EvolutionaryAlgorithm(
    params, nodes, items, filename=file, log_statistics=False
)
best_solution = evolutionary_algorithm.run()
best = best_fitness(evolutionary_algorithm.stats["best"])
worst = worst_fitness(evolutionary_algorithm.stats["worst"])
avg = avg_fitness(evolutionary_algorithm.stats["avg"])
print("Best: ", best)
print("Worst: ", worst)
print("Avg: ", avg)
log_results(results_dir, file, "Evolutionary Algorithm", best, worst, avg)
print()

print("Simulated Annealing")
sa = SimulatedAnnealing(params, nodes, items)
sa_best_solution = sa.run()
print("Best: ", sa_best_solution)
