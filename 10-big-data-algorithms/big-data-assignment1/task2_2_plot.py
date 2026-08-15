import matplotlib.pyplot as plt
import collections

# Step 1: Load top 5 users
top_users = []
with open("task2_2_output.txt") as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            top_users.append(parts[0].strip('"'))

# Step 2: Load monthly data
monthly_spend = collections.defaultdict(lambda: collections.defaultdict(float))

with open("task2_2_monthly_output.txt") as f:
    for line in f:
        try:
            key, value = line.strip().split('\t')
            user, month = key.strip("[]").replace('"', '').split(',')
            user = user.strip()
            month = int(month.strip())
            value = float(value.strip())
            if user in top_users:
                monthly_spend[user][month] += value
        except:
            continue

# Step 3: Plot line chart
months = list(range(1, 13))

plt.figure(figsize=(12, 6))
for user in top_users:
    sales = [monthly_spend[user].get(m, 0) for m in months]
    plt.plot(months, sales, marker='o', label=user)

plt.xlabel("Month")
plt.ylabel("Consumption ($)")
plt.title("Monthly Spending of Top 5 Users")
plt.xticks(months)
plt.legend()
plt.tight_layout()
plt.savefig("task2_2_output.pdf")
plt.close()

print("Line chart saved as task2_2_output.pdf")
