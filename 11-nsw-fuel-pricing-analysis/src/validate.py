import glob
import json
from collections import Counter
from datetime import datetime

p = json.load(open(sorted(glob.glob("../data/raw/prices/*/prices.json"))[-1]))
s = json.load(open(sorted(glob.glob("../data/raw/stations/*/stations.json"))[-1]))

print(f"rows: {len(p)} prices | {len(s)} stations")

# 1. schema: required keys present and non-null
for key in ("stationcode", "fueltype", "price", "lastupdated"):
    print(f"null/missing {key}:", sum(r.get(key) in (None, "") for r in p))

# 2. duplicates on the natural key
keys = Counter((r["stationcode"], r["fueltype"]) for r in p)
print("duplicate (station, fuel) pairs:", sum(v > 1 for v in keys.values()))

# 3. price range by fuel type (cents per litre)
print("\nprice range by fuel type:")
by_fuel = {}
for r in p:
    by_fuel.setdefault(r["fueltype"], []).append(r["price"])
for fuel, prices in sorted(by_fuel.items()):
    print(f"  {fuel:4} n={len(prices):5} min={min(prices):6.1f} max={max(prices):6.1f}")

# 4. freshness: age of each price in days
now = datetime.now()
ages = [(now - datetime.strptime(r["lastupdated"], "%d/%m/%Y %H:%M:%S")).days for r in p]
print("\nfreshness (share of price rows):")
for label, limit in (("<=1 day", 1), ("<=7 days", 7), ("<=30 days", 30)):
    print(f"  {label:10} {sum(a <= limit for a in ages) / len(ages):.1%}")
print("  oldest:", max(ages), "days")

# 5. coordinates inside NSW/ACT bounding box
out = [x for x in s if not (-37.6 <= x["location"]["latitude"] <= -28.1
                            and 140.9 <= x["location"]["longitude"] <= 153.7)]
print("\nstations outside NSW/ACT bounding box:", len(out))
for x in out[:5]:
    print("  ", x["code"], x["name"], x["address"])
