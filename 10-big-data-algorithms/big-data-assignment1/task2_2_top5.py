# Read unsorted totals and write top 5 to final output
lines = []

with open("task2_2_unsorted.txt") as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            user = parts[0].strip('"')
            total = float(parts[1])
            lines.append((user, total))

top5 = sorted(lines, key=lambda x: x[1], reverse=True)[:5]

with open("task2_2_output.txt", "w") as f:
    for user, total in top5:
        f.write(f"{user}\t{round(total, 2)}\n")

