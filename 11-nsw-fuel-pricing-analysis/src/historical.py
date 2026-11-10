import glob
import os
import sys

import pandas as pd

COLUMNS = ["ServiceStationName", "Address", "Suburb", "Postcode", "Brand", "FuelCode", "PriceUpdatedDate", "Price"]
STATION_COLS = ["ServiceStationName", "Address", "Suburb", "Postcode", "Brand"]
SOURCE_DIR = "../data/historical/source"
DATE_FORMATS = ("%Y-%m-%d %H:%M:%S", "%d/%m/%Y %I:%M:%S %p", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M")
AFFECTED = [f"2023-{m:02d}" for m in range(1, 11)] + ["2025-06", "2025-10", "2026-09"]
GAP_DAYS = {"2023-10": "2023-10-01", "2024-10": "2024-10-06", "2025-10": "2025-10-05"}


def parse_dates(s):
    text = s.astype(str).str.strip()
    out = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
    for fmt in DATE_FORMATS:
        todo = out.isna()
        if not todo.any():
            break
        out[todo] = pd.to_datetime(text[todo], format=fmt, errors="coerce")
    return out


def load_month(path):
    if path.lower().endswith(".csv"):
        raw = pd.read_csv(path, header=None, dtype=object, low_memory=False)
    else:
        raw = pd.read_excel(path, header=None, dtype=object)

    hits = raw.index[raw[0].astype(str).str.strip() == "ServiceStationName"]
    if len(hits) == 0:
        raise ValueError("header row not found")
    start = hits[0]

    df = raw.loc[start + 1:].copy()
    df.columns = [str(c).strip() for c in raw.loc[start]]
    if list(df.columns) != COLUMNS:
        raise ValueError(f"unexpected columns: {list(df.columns)}")
    df = df.dropna(how="all").reset_index(drop=True)

    blank = df["ServiceStationName"].isna()
    df[STATION_COLS] = df[STATION_COLS].ffill()
    df["Postcode"] = pd.to_numeric(df["Postcode"], errors="coerce").astype("Int64")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["FuelCode"] = df["FuelCode"].str.strip()
    df["PriceUpdatedDate"] = parse_dates(df["PriceUpdatedDate"])

    prev = df["PriceUpdatedDate"].shift(1)
    stats = {
        "filled_rows": int(blank.sum()),
        "filled_ts_mismatch": int((blank & (df["PriceUpdatedDate"] != prev)).sum()),
    }
    return df, stats


def check(tag, df, stats):
    year, month = int(tag[:4]), int(tag[5:7])
    dt = df["PriceUpdatedDate"]
    rec = {
        "month": tag,
        "rows": len(df),
        "filled": stats["filled_rows"],
        "fill_mismatch": stats["filled_ts_mismatch"],
        "nulls": int(df.isna().sum().sum()),
        "bad_dates": int(dt.isna().sum()),
        "off_month": int(((dt.dt.year != year) | (dt.dt.month != month)).sum()),
        "min_date": dt.min(),
        "max_date": dt.max(),
        "dup_events": int(df.duplicated(["ServiceStationName", "Address", "FuelCode", "PriceUpdatedDate"]).sum()),
    }
    if tag in GAP_DAYS:
        hour2 = dt[dt.dt.hour == 2]
        rec["hour2_rows"] = len(hour2)
        rec["gap_day_hour2"] = int((hour2.dt.strftime("%Y-%m-%d") == GAP_DAYS[tag]).sum())
    return rec


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "all":
        tags = sorted(os.path.basename(p).rsplit(".", 1)[0] for p in glob.glob(f"{SOURCE_DIR}/*.*"))
    else:
        tags = AFFECTED

    rows = []
    for tag in tags:
        path = glob.glob(f"{SOURCE_DIR}/{tag}.*")[0]
        try:
            df, stats = load_month(path)
            rows.append(check(tag, df, stats))
            print("ok", tag, len(df))
        except Exception as e:
            print("FAILED", tag, str(e)[:120])

    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", None)
    print()
    print(pd.DataFrame(rows).to_string(index=False))
