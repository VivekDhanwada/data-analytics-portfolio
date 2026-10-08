import json
import os
from datetime import date, datetime

import requests

from auth import get_access_token
from config import PRICES_URL, REFDATA_URL, API_KEY, EXCLUDED_BRANDS


def common_headers(token, include_if_modified_since=False):
    now = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": API_KEY,
        "Content-Type": "application/json; charset=utf-8",
        "transactionid": f"ingest-{datetime.now().timestamp()}",
        "requesttimestamp": now,
    }
    if include_if_modified_since:
        headers["if-modified-since"] = "01/01/2020 12:00:00 AM"
    return headers


def fetch_prices(token):
    resp = requests.get(PRICES_URL, headers=common_headers(token))
    resp.raise_for_status()
    data = resp.json()["prices"]
    return [row for row in data if row["fueltype"] != "EV"]


def fetch_reference_data(token):
    resp = requests.get(REFDATA_URL, headers=common_headers(token, include_if_modified_since=True))
    resp.raise_for_status()
    stations = resp.json()["stations"]["items"]
    return [s for s in stations if s["brand"] not in EXCLUDED_BRANDS]


def save_local(data, folder, filename):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    with open(path, "w") as f:
        json.dump(data, f)
    print(f"Saved {len(data)} records to {path}")


def run_ingestion():
    token = get_access_token()
    today = date.today().isoformat()

    prices = fetch_prices(token)
    stations = fetch_reference_data(token)

    # keep only stations that report at least one real (non-EV) fuel price
    fuel_station_codes = {p["stationcode"] for p in prices}
    stations = [s for s in stations if s["code"] in fuel_station_codes]

    return prices, stations, today


def lambda_handler(event, context):
    prices, stations, today = run_ingestion()
    return {
        "statusCode": 200,
        "prices_count": len(prices),
        "stations_count": len(stations),
        "date": today,
    }


if __name__ == "__main__":
    prices, stations, today = run_ingestion()
    save_local(prices, f"../data/raw/prices/dt={today}", "prices.json")
    save_local(stations, f"../data/raw/stations/dt={today}", "stations.json")
