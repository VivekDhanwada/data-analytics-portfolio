"""
01_fetch_data.py
Fetches match event data from the StatsBomb open data API via raw HTTP requests.
Competition: UEFA Euro 2024 (competition_id 55, season_id 282)
"""

import requests
import json
import sys

BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
MATCH_ID = 3943043  # Euro 2024 Final: Spain vs England

events_url = f"{BASE_URL}/events/{MATCH_ID}.json"
print(f"Fetching: {events_url}\n")

response = requests.get(events_url)

if response.status_code != 200:
    print(f"Request failed: {response.status_code}")
    sys.exit(1)

# response.json() parses the raw JSON string into a Python list of dicts.
# Each dict is one event — a pass, shot, tackle, etc.
events = response.json()

print(f"Total events: {len(events)}")
print("\n── First event ──")
print(json.dumps(events[0], indent=2, ensure_ascii=False))
# ensure_ascii=False preserves characters like ñ, é in player names