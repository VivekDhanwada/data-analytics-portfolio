import math
import time
import heapq
import itertools
from Create_Tree_Node import create_rtree, TreeNode  # Reuse working code

# Load data points
def load_points(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                pid = parts[0]
                x = float(parts[1])
                y = float(parts[2])
                points.append((pid, x, y))
    return points

# Distance from point to rectangle
def min_dist_point_to_rect(px, py, rect):
    min_x = max(rect[0], min(px, rect[2]))
    min_y = max(rect[1], min(py, rect[3]))
    return math.sqrt((px - min_x)**2 + (py - min_y)**2)

# Distance between two points
def euclidean(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# Best-First Search
def best_first_search(query, root):
    heap = []
    counter = itertools.count()
    heapq.heappush(heap, (0.0, next(counter), root))

    while heap:
        dist, _, node = heapq.heappop(heap)
        if node.is_leaf:
            return node.entries[0]  # (x, y, id)

        for rect, child in node.entries:
            d = min_dist_point_to_rect(query[1], query[2], rect)
            heapq.heappush(heap, (d, next(counter), child))
    return None

# Main function
def main():
    dataset_file = "parking_dataset.txt"
    query_file = "query_points.txt"
    output_file = "task1_output_bestfirst_divide.txt"

    dataset = load_points(dataset_file)
    queries = load_points(query_file)

    # Sort dataset by x to divide
    dataset_sorted = sorted(dataset, key=lambda p: p[1])
    mid = len(dataset_sorted) // 2
    left = dataset_sorted[:mid]
    right = dataset_sorted[mid:]

    # Convert to (x, y, id) format
    left_points = [(float(p[1]), float(p[2]), p[0]) for p in left]
    right_points = [(float(p[1]), float(p[2]), p[0]) for p in right]

    # Build R-trees
    left_tree = create_rtree(left_points)
    right_tree = create_rtree(right_points)

    start = time.time()
    results = []

    for query in queries:
        nn_left = best_first_search(query, left_tree)
        nn_right = best_first_search(query, right_tree)

        dist_left = euclidean((nn_left[0], nn_left[1]), (query[1], query[2]))
        dist_right = euclidean((nn_right[0], nn_right[1]), (query[1], query[2]))

        final_nn = nn_left if dist_left < dist_right else nn_right
        results.append((query[0], final_nn[2], final_nn[0], final_nn[1]))

    end = time.time()
    total_time = end - start
    avg_time = total_time / len(queries)

    # Write output
    with open(output_file, 'w') as f:
        for result in results:
            f.write(f"Query {result[0]} → Nearest: id={result[1]}, x={result[2]}, y={result[3]}\n")
        f.write(f"\nTotal runtime: {total_time:.6f} seconds\n")
        f.write(f"Average time per query: {avg_time:.6f} seconds\n")

if __name__ == "__main__":
    main()