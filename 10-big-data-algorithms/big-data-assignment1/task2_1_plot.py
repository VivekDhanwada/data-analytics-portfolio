import matplotlib.pyplot as plt
import collections

# Load monthly data
monthly_sales = collections.defaultdict(lambda: collections.defaultdict(float))

with open("task2_1_monthly_output.txt") as file:
    for line in file:
        try:
            key, value = line.strip().split('\t')
            coffee, month = key.strip("[]").replace('"', '').split(',')
            coffee = coffee.strip()
            month = int(month.strip())
            sales = float(value.strip())
            monthly_sales[coffee][month] += sales
        except:
            continue

# Compute total sales and identify bottom 3
total_sales = {coffee: sum(months.values()) for coffee, months in monthly_sales.items()}
bottom3 = sorted(total_sales.items(), key=lambda x: x[1])[:3]
bottom3_names = [c for c, _ in bottom3]

# Plot line chart
months = list(range(1, 13))
plt.figure(figsize=(10, 6))

for coffee in bottom3_names:
    sales = [monthly_sales[coffee].get(m, 0) for m in months]
    plt.plot(months, sales, marker='o', label=coffee)

plt.xlabel("Month")
plt.ylabel("Sales ($)")
plt.title("Monthly Sales of Bottom 3 Coffee Types")
plt.xticks(months)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("task2_1_output.pdf")
plt.close()

print("Line chart saved as task2_1_output.pdf")
