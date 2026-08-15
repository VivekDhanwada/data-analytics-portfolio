import time
import math

# Function to load dataset or query file
def load_file(filename):
    points = []
    with open(filename, 'r') as file:
        for line in file:
            tokens = line.strip().split()
            if len(tokens) == 3:
                pid = tokens[0]
                x = float(tokens[1])
                y = float(tokens[2])
                points.append((pid, x, y))
    return points

# Function to compute Euclidean distance
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Function to find the nearest point in the dataset for one query point
def find_nearest(query, dataset):
    min_distance = float('inf')
    nearest_point = None
    for data in dataset:
        distance = euclidean_distance(query[1], query[2], data[1], data[2])
        if distance < min_distance:
            min_distance = distance
            nearest_point = data
    return nearest_point

# Main function for sequential scan
def run_sequential_nn(dataset_file, query_file, output_file):
    dataset = load_file(dataset_file)
    queries = load_file(query_file)

    start_time = time.time()
    results = []

    for query in queries:
        nearest = find_nearest(query, dataset)
        results.append((query[0], nearest[0], nearest[1], nearest[2]))

    end_time = time.time()
    total_time = end_time - start_time
    average_time = total_time / len(queries)

    with open(output_file, 'w') as out:
        for result in results:
            out.write(f"Query {result[0]} → Nearest: id={result[1]}, x={result[2]}, y={result[3]}\n")
        out.write(f"\nTotal runtime: {total_time:.6f} seconds\n")
        out.write(f"Average time per query: {average_time:.6f} seconds\n")

# Main block
if __name__ == "__main__":
    run_sequential_nn(
        dataset_file='shop_dataset.txt',         # Change to 'restaurant_dataset.txt' or 'parking_dataset.txt' as needed
        query_file='query_points.txt',
        output_file='task1_output_sequential.txt'
    )