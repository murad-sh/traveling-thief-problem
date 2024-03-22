import csv
from file_handler import read_file
from utils import best_fitness, worst_fitness, avg_fitness
from evolutionary_algorithm import EvolutionaryAlgorithm

path = "/Users/murad-sh/Private/TTP"

params, nodes, items = read_file(
    path + "/data/eil51_n150_uncorr-similar-weights_01.ttp"
)

population_sizes = [50, 100, 200, 400, 500]
crossover_rates = [0.3, 0.4, 0.5, 0.7, 0.9]
mutation_rates = [0.01, 0.1, 0.2, 0.3, 0.5]


def run_experiment(filename, variable, values):
    with open(filename, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Parameter Value", "Best", "Worst", "Avg"])

        for value in values:
            if variable == "population_size":
                algorithm = EvolutionaryAlgorithm(
                    params, nodes, items, population_size=value
                )
            elif variable == "crossover_rate":
                algorithm = EvolutionaryAlgorithm(
                    params, nodes, items, crossover_rate=value
                )
            elif variable == "mutation_rate":
                algorithm = EvolutionaryAlgorithm(
                    params, nodes, items, mutation_rate=value
                )

            algorithm.run()
            writer.writerow(
                [
                    value,
                    best_fitness(algorithm.stats["best"]),
                    worst_fitness(algorithm.stats["worst"]),
                    avg_fitness(algorithm.stats["avg"]),
                ]
            )


run_experiment(
    path + "/results/population_experiment.csv", "population_size", population_sizes
)
run_experiment(
    path + "/results/crossover_experiment.csv", "crossover_rate", crossover_rates
)
run_experiment(
    path + "/results/mutation_experiment.csv", "mutation_rate", mutation_rates
)
