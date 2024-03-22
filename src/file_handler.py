import re
import os
import csv


def read_file(file_path):

    with open(file_path, "r") as file:
        lines = file.readlines()

    params = {}
    for line in lines:
        if line.startswith("DIMENSION"):
            params["dimension"] = int(line.split(":")[1].strip())
        elif line.startswith("NUMBER OF ITEMS"):
            params["num_items"] = int(line.split(":")[1].strip())
        elif line.startswith("CAPACITY OF KNAPSACK"):
            params["knapsack_capacity"] = int(line.split(":")[1].strip())
        elif line.startswith("MIN SPEED"):
            params["min_speed"] = float(line.split(":")[1].strip())
        elif line.startswith("MAX SPEED"):
            params["max_speed"] = float(line.split(":")[1].strip())
        elif line.startswith("RENTING RATIO"):
            params["renting_ratio"] = float(line.split(":")[1].strip())

    node_section_pattern = re.compile(r"NODE_COORD_SECTION\s+\(INDEX,\s+X,\s+Y\):")
    items_section_pattern = re.compile(
        r"ITEMS SECTION\s+\(INDEX,\s+PROFIT,\s+WEIGHT,\s+ASSIGNED NODE NUMBER\):"
    )

    node_section_index = next(
        (i for i, line in enumerate(lines) if node_section_pattern.search(line)), None
    )
    items_section_index = next(
        (i for i, line in enumerate(lines) if items_section_pattern.search(line)), None
    )

    if node_section_index is None or items_section_index is None:
        raise ValueError("Sections not found in the file")

    nodes = []
    node_lines = lines[node_section_index + 1 : items_section_index]
    for line in node_lines:
        parts = line.split()
        nodes.append((int(parts[0]), float(parts[1]), float(parts[2])))

    items = []
    for line in lines[items_section_index + 1 :]:
        parts = line.split()
        items.append((int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])))

    return params, nodes, items


def log_statistics(filename, iteration, stats):
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        if not file_exists:
            writer.writerow(
                ["Iteration", "Best Fitness", "Average Fitness", "Worst Fitness"]
            )
        writer.writerow([iteration, stats["best"], stats["average"], stats["worst"]])


def log_results(results_dir, file_name, algo_name, best, worst, avg):
    full_file_path = os.path.join(results_dir, "overall_results.csv")

    os.makedirs(results_dir, exist_ok=True)

    file_exists = os.path.isfile(full_file_path)

    with open(full_file_path, "a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        if not file_exists:
            writer.writerow(
                [
                    "File Name",
                    "Algorithm",
                    "Best Fitness",
                    "Worst Fitness",
                    "Average Fitness",
                ]
            )
        writer.writerow([file_name, algo_name, best, worst, avg])
