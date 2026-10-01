# Movie Database Web Application (Exercise 3)

A Python-based three-tier web application using the **Bottle** micro-framework, connected to a MySQL relational movie database, providing web-based interface controls for database updates, network queries, and graph traversal logic.

## Overview

This project implements the application logic layer (`app.py`) for a movie database web interface. It executes specific data retrieval and manipulation operations adhering strictly to the architectural constraints of the course (e.g., prohibition of `JOIN`, `LIMIT`, and subqueries within `SELECT`/`FROM` clauses).

## Key Features & Functions

- **`updateRank`:** Updates a movie's rank by computing the average of its current rank and two user-provided input values, handling potential errors for missing films or duplicate titles.
- **`colleaguesOfColleagues`:** Discovers indirect collaborative links between actors based on shared movie appearances.
- **`actorPairs`:** Identifies actor pairs who share strict genre separation constraints while collaborating across a minimum threshold of diverse categories.
- **`selectTopNactors`:** Retrieves the top $N$ actors per movie genre based on their total volume of film appearances.
- **`traceActorInfluence` (Bonus):** Computes the transitive closure of actor influence networks across shared film timelines and genres.

## Technical Restrictions & Compliance

- **No Advanced SQL Operators:** Avoids subqueries in `FROM`/`SELECT` clauses and completely excludes `JOIN` commands.
- **No Result Limiting:** Strictly refrains from using `LIMIT` clauses.
- **Data Structure Constraints:** Returns lists of tuples where the first row contains column headers as required by the web framework.

## Files Included

- **`app.py`:** Core application logic file containing the implemented database handlers and backend routing support.
