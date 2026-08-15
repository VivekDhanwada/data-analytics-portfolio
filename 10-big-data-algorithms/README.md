# Big Data & Algorithms

Two university coursework projects implementing distributed processing and spatial search algorithms from first principles — covering MapReduce job design and R-Tree-based nearest neighbour search, without relying on third-party algorithm libraries.

**Note:** This page consolidates coursework from a single Big Data unit (COMP3210/6210) across two separate assignments rather than standing as a single end-to-end project. It's presented here to showcase algorithmic implementation from scratch rather than as a standalone production build.

## Overview

Two applied Big Data assignments completed as part of coursework: a MapReduce pipeline analysing coffee sales transaction data, and a spatial search project implementing an R-Tree index and nearest neighbour search algorithms from scratch. Together they demonstrate distributed data processing patterns and algorithmic problem-solving without relying on pre-built libraries for the core logic.

## Part 1: MapReduce — Coffee Sales Analysis (COMP6210)

**Problem:** Analyse a coffee sales transaction dataset to identify revenue patterns by coffee type and customer spending behaviour, using the MapReduce paradigm.

**Approach:**
- Data cleaning and triplet extraction pipeline (Pandas, PyMongo) — dropped incomplete rows, filtered to card-paid transactions, extracted coffee type, customer ID, amount, and timestamp fields
- Implemented custom Mapper and Reducer functions (using the `mrjob` library) across four tasks:
  - Total sales per coffee type
  - Total and monthly sales trend for the three lowest-performing coffee types
  - Total spend per customer
  - Monthly spending pattern for the top 5 customers by total spend
- Used a multi-stage reduce pattern to enable global sorting across reducers (emitting totals with a `None` key first, then sorting and re-emitting in a second reduce step) — a non-trivial MapReduce technique for cross-key ordering

**Result:** Identified top and bottom-performing coffee types by revenue, and produced monthly spend trend visualisations for both the lowest-performing products and highest-value customers, distinguishing consistent underperformance from seasonal variation.

## Part 2: R-Tree Nearest Neighbour Search (COMP3210/6210)

**Problem:** Implement and benchmark spatial nearest neighbour search algorithms of increasing sophistication, from brute-force to indexed to parallelisable.

**My role:** This was a group assignment; my individual contribution was Task 1 (Nearest Neighbour Search) — R-Tree construction, Best-First Search implementation, and the Divide-and-Conquer extension. Task 2 (Skyline Search) was completed by a teammate and is not included here.

**Approach:**
- Built an R-Tree spatial index from scratch (pure Python, no third-party spatial libraries) — recursive construction grouping nearby points into Minimum Bounding Rectangles (MBRs), forming internal nodes until a single root remains
- Implemented Best-First Search using a priority queue ordered by MINDIST (minimum distance from query point to each node's bounding rectangle), guaranteeing exact nearest-neighbour results while pruning irrelevant regions
- Extended to a Divide-and-Conquer approach: partitioned the dataset spatially, built independent R-Trees per partition, ran Best-First Search on each, and merged results — improving scalability for large datasets and parallel execution
- Benchmarked all three approaches (Sequential brute-force, R-Tree Best-First, Divide-and-Conquer) against the same dataset and query points for direct runtime comparison

**Result:** Sequential brute-force search ran in ~3.80 seconds; R-Tree Best-First Search reduced this to ~0.005 seconds through spatial pruning; the Divide-and-Conquer extension ran in ~0.006 seconds while offering better scalability for larger, parallelisable workloads. All three methods returned identical, correct nearest-neighbour results — confirming that the performance gains came from search efficiency, not reduced accuracy.

## Tech Stack

- Python (pure implementation — no third-party spatial or MapReduce algorithm libraries for core logic)
- mrjob (MapReduce job simulation)
- Pandas, PyMongo (data cleaning and storage)
- Custom R-Tree, Best-First Search, and Divide-and-Conquer implementations

## Skills Demonstrated

**Distributed Data Processing**
- MapReduce job design (Mapper/Reducer pattern)
- Multi-stage reduce patterns for cross-key sorting
- Data cleaning pipelines feeding structured processing jobs

**Algorithms & Data Structures**
- Spatial indexing: R-Tree construction (recursive, MBR-based)
- Priority-queue-based search (Best-First Search with MINDIST pruning)
- Divide-and-Conquer algorithm design for scalability
- Algorithmic benchmarking and performance comparison across implementation strategies

## Limitations

- Both are coursework assignments on academic datasets, not production systems — no deployment, monitoring, or live data pipeline.
- The R-Tree project was a group assignment; my individually-owned contribution was Task 1 (Nearest Neighbour Search: R-Tree construction, Best-First Search, Divide-and-Conquer). Task 2 (Skyline Search) was a teammate's work and is not represented here.
- Benchmark runtimes were measured on a single machine/dataset size rather than across varying scales — results demonstrate relative algorithmic efficiency, not production-scale performance guarantees.

## Key Takeaway

Implemented distributed processing and spatial search algorithms from first principles rather than relying on pre-built libraries, with benchmarked results showing over 600x speedup from brute-force to indexed search — demonstrating both algorithmic understanding and the practical value of appropriate data structure choice.