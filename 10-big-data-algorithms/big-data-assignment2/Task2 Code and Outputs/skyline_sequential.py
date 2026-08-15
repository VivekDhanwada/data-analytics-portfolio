import time

def read_dataset(file_path):
    points = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 3:
                continue
            point_id = int(parts[0])
            x = float(parts[1])  # cost
            y = float(parts[2])  # size
            points.append((point_id, x, y))
    return points

def dominates(a, b):
    # a and b are tuples: (id, cost, size)
    return (a[1] <= b[1] and a[2] >= b[2]) and (a[1] < b[1] or a[2] > b[2])

def skyline_sequential(points):
    skyline = []
    for p in points:
        dominated = False
        for q in points:
            if dominates(q, p):
                dominated = True
                break
        if not dominated:
            skyline.append(p)
    return skyline

def write_output(skyline_points, output_path, runtime_seconds):
    with open(output_path, 'a') as f:  # append mode
        f.write("=======================================\n")
        f.write("Algorithm: Sequential Scan\n")
        for point in skyline_points:
            f.write(f"id={point[0]}, x={point[1]}, y={point[2]}\n")
        f.write(f"\nTotal runtime: {runtime_seconds:.6f} seconds\n")
        f.write(f"Average time per skyline point: {runtime_seconds / len(skyline_points):.8f} seconds\n\n")

if __name__ == "__main__":
    file_path = r"C:\Users\wahip\Downloads\Assignment 2 Datasets\Task2_Datasets\city1.txt"
    output_path = "task2_output.txt"

    dataset = read_dataset(file_path)
    print(f"Loaded {len(dataset)} records.")

    start_time = time.time()
    skyline = skyline_sequential(dataset)
    end_time = time.time()

    total_time = end_time - start_time
    print(f"Skyline contains {len(skyline)} points. Runtime: {total_time:.6f} seconds")

    write_output(skyline, output_path, total_time)
    print(f"Results written to {output_path}")
