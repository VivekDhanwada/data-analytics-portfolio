import heapq
import math
import time
import itertools
from Create_Tree_Node import create_rtree, TreeNode  # Ensure this file is in the same folder

# Load data points from a file
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

# Distance from point to rectangle
def min_dist_point_to_rect(px, py, rect):
    min_x = max(rect[0], min(px, rect[2]))
    min_y = max(rect[1], min(py, rect[3]))
    return math.sqrt((px - min_x)**2 + (py - min_y)**2)

# Best-First Search with unique counter
def best_first_search(query_point, rtree_root):
    heap = []
    counter = itertools.count()
    heapq.heappush(heap, (0.0, next(counter), rtree_root))

    while heap:
        dist, _, node = heapq.heappop(heap)

        if node.is_leaf:
            return node.entries[0]  # (x, y, id)

        for entry in node.entries:
            rect = entry[0]
            child = entry[1]
            d = min_dist_point_to_rect(query_point[1], query_point[2], rect)
            heapq.heappush(heap, (d, next(counter), child))

    return None

# Run the algorithm on all queries
def run_best_first_nn(dataset_file, query_file, output_file):
    dataset = load_file(dataset_file)
    queries = load_file(query_file)

    point_data = [(p[1], p[2], p[0]) for p in dataset]
    rtree_root = create_rtree(point_data)

    start_time = time.time()
    results = []

    for query in queries:
        nn = best_first_search(query, rtree_root)
        results.append((query[0], nn[2], nn[0], nn[1]))

    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / len(queries)

    with open(output_file, 'w') as f:
        for result in results:
            f.write(f"Query {result[0]} → Nearest: id={result[1]}, x={result[2]}, y={result[3]}\n")
        f.write(f"\nTotal runtime: {total_time:.6f} seconds\n")
        f.write(f"Average time per query: {avg_time:.6f} seconds\n")

# Main function
if __name__ == "__main__":
    run_best_first_nn(
        dataset_file='shop_dataset.txt',
        query_file='query_points.txt',
        output_file='task1_output_bestfirst.txt'
    )