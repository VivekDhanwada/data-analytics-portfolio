import glob
import os

import pandas as pd

import historical as h

CLEAN_DIR = "../data/historical/clean"
REJECT_DIR = "../data/historical/rejects"
os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(REJECT_DIR, exist_ok=True)

paths = sorted(glob.glob(f"{h.SOURCE_DIR}/*.*"))
rows = []

for path in paths:
    tag = os.path.basename(path).rsplit(".", 1)[0]
    out = f"{CLEAN_DIR}/{tag}.parquet"
    if os.path.exists(out):
        print("skip", tag)
        continue
    try:
        df, _ = h.load_month(path)
        bad = df["FuelCode"].isna() | df["PriceUpdatedDate"].isna() | df["Price"].isna()
        df["source_month"] = tag
        df[~bad].to_parquet(out, index=False)
        if bad.any():
            df[bad].to_csv(f"{REJECT_DIR}/{tag}.csv", index=False)
        rows.append({"month": tag, "rows_in": len(df), "clean": int((~bad).sum()), "rejected": int(bad.sum())})
        print("ok", tag, len(df), "rejected", int(bad.sum()))
    except Exception as e:
        print("FAILED", tag, str(e)[:120])

if rows:
    summary = pd.DataFrame(rows)
    print()
    print(summary.to_string(index=False))
    print("\ntotal rows in:", summary["rows_in"].sum(), "| clean:", summary["clean"].sum(), "| rejected:", summary["rejected"].sum())
