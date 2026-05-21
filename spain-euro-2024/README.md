# Spain at Euro 2024 — A Tactical Analysis

An analytical breakdown of Spain's UEFA Euro 2024 campaign using StatsBomb open event data. The project uses Python for data collection and analysis, and Power BI for dashboard output.

**Status: In Progress**

## Overview

Spain won UEFA Euro 2024 undefeated across seven matches, playing a fluid, press-heavy style without relying on a traditional striker. This project analyses their campaign across three tactical dimensions: attacking threat creation, defensive pressing, and passing network structure.

The dataset covers all seven Spain matches (group stage through final) using StatsBomb open data, accessed via raw HTTP requests. Event data comprises positional coordinates, player actions, and timing across 3,300+ events per match.

## Analytical Questions

1. Where did Spain's shots originate, and which players arrived in goal-scoring positions?
2. How high did Spain press, and where did they win the ball back?
3. How distributed was Spain's passing network — evidence of positional fluidity?

## Data Source

- **Provider:** StatsBomb Open Data
- **Competition:** UEFA Euro 2024 (competition_id 55, season_id 282)
- **Matches:** 7 (group stage, round of 16, quarter-final, semi-final, final)
- **Access method:** Raw HTTP requests to StatsBomb's public GitHub repository
- **Data type:** Event data + 360 freeze-frame data

## Project Structure

- [`01_fetch_data.py`](./01_fetch_data.py) — Fetch and validate raw event JSON for each match
- `02_explore_events.py` — Inspect event types, fields, and data structure *(in progress)*
- `03_shots_analysis.py` — Shot locations and goal-scoring positions *(planned)*
- `04_press_analysis.py` — Press height and ball recovery locations *(planned)*
- `05_passing_network.py` — Passing network structure and distribution *(planned)*

## Tools

- Python, pandas, Matplotlib
- StatsBomb Open Data API
- Power BI

## Limitations

*To be completed as analysis progresses.*

## Dashboard

*Power BI dashboard to be published on completion.*