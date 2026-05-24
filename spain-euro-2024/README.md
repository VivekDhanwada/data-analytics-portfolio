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

## Key Findings

**Shot Creation**
Spain generated 123 shots across seven matches, concentrated almost entirely inside and around the penalty area. Goals were scored from close range by multiple players across different positions — not exclusively through the centre forward. Shot locations confirm attacking threat was distributed across the front line rather than routed through a single striker.

**Pressing**
Spain's median pressure location was x=67.2 on StatsBomb's 0–120 pitch scale, placing the average press just beyond the halfway line. Pressures were distributed across the full pitch rather than concentrated exclusively in the opponent's half, indicating a contextual press rather than a rigid high-press system. Ball recoveries followed a similar spread, with a concentration in the middle third.

**Passing Network**
Spain's passing network was dominated by a left-sided and central spine — Cucurella, Laporte, Le Normand, Rodri, and Fabián — accounting for the strongest passing connections across the tournament. The centre forward was not a central passing node, consistent with a system that builds through midfield rather than through the striker. Wide players Yamal and Nico Williams appeared as peripheral nodes, receiving the ball in advanced positions rather than participating in build-up circulation.

## Project Structure

- [`01_fetch_data.py`](./01_fetch_data.py) — Fetch and validate raw event JSON for each match
- [`02_explore_events.py`](./02_explore_events.py) — Inspect event types, fields, and data structure
- [`03_shots_analysis.py`](./03_shots_analysis.py) — Shot locations and goal-scoring positions
- [`04_press_analysis.py`](./04_press_analysis.py) — Press height and ball recovery locations
- [`05_passing_network.py`](./05_passing_network.py) — Passing network structure and distribution

## Tools

- Python, pandas, Matplotlib
- StatsBomb Open Data API
- Power BI

## Limitations

- Passing network filters to connections of 35+ passes, excluding lower-volume combinations
- Press analysis uses raw pressure event locations — does not account for match state or score context
- Average player positions are calculated across the full tournament, masking positional variation between matches and within matches
- 360 freeze-frame data is available but not yet used in this analysis

## Dashboard

*Power BI dashboard to be published on completion.*