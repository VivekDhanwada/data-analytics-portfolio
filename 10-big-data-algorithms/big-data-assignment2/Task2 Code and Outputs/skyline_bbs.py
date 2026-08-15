import time

def read_dataset(file_path):
    points = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                point_id = int(parts[0])
                x = float(parts[1])
                y = float(parts[2])
                points.append((point_id, x, y))
    return points

def dominates(a, b):
    return (a[1] <= b[1] and a[2] >= b[2]) and (a[1] < b[1] or a[2] > b[2])

class RTreeNode:
    def __init__(self, points):
        self.points = points
        self.mbr = self.compute_mbr()

    def compute_mbr(self):
        min_x = min(p[1] for p in self.points)
        min_y = min(p[2] for p in self.points)
        max_x = max(p[1] for p in self.points)
        max_y = max(p[2] for p in self.points)
        return (min_x, min_y, max_x, max_y)

    def representative_point(self):
        return (None, self.mbr[0], self.mbr[3])

def bbs_simple(points, group_size=100):
    nodes = []
    for i in range(0, len(points), group_size):
        group = points[i:i + group_size]
        nodes.append(RTreeNode(group))

    candidates = []
    for node in nodes:
        rep = node.representative_point()
        if not any(dominates(s, rep) for s in candidates):
            for p in node.points:
                if not any(dominates(s, p) for s in candidates):
                    candidates = [s for s in candidates if not dominates(p, s)]
                    candidates.append(p)
    return candidates

def write_output(skyline_points, output_path, runtime):
    with open(output_path, 'a') as f:  # append mode
        f.write("=======================================\n")
        f.write("Algorithm: BBS (Grouped RTreeNode)\n")
        for point in skyline_points:
            f.write(f"id={point[0]}, x={point[1]}, y={point[2]}\n")
        f.write(f"\nTotal runtime: {runtime:.6f} seconds\n")
        f.write(f"Average time per skyline point: {runtime / len(skyline_points):.8f} seconds\n\n")

if __name__ == "__main__":
    file_path = r"C:\Users\wahip\Downloads\Assignment 2 Datasets\Task2_Datasets\city1.txt"
    output_path = "task2_output.txt"

    dataset = read_dataset(file_path)
    print(f"Loaded {len(dataset)} points.")

    start_time = time.time()
    skyline = bbs_simple(dataset)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Skyline has {len(skyline)} points. Took {duration:.6f} seconds.")

    write_output(skyline, output_path, duration)
    print(f"Results written to {output_path}")
