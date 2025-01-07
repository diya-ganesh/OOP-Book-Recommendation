# Property Graph Book Recommendation System

**This project is a book recommendation engine developed for DS3500: Advanced Programming with Data. It leverages a property graph model to recommend books using network analysis techniques.**

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributors](#contributors)

## Introduction

This project explores the application of property graphs, a type of graph database model, in building a personalized book recommendation system. Property graphs are a powerful tool for modeling complex, interconnected data, widely used in areas such as social networks, recommendation systems, and biological networks.

The recommendation engine implements:
- **Node and Relationship Modeling:** Nodes (e.g., persons and books) and relationships (e.g., "Knows" and "Bought") are categorized and enriched with properties like "price."
- **Network Analysis:** Uses relationships between nodes to suggest books purchased by people known to a given user, excluding books already purchased by them.
- **Graph Visualization:** Outputs the original property graph and a recommendation subgraph for a specific user.

## Features

- **Property Graph Framework:** Models nodes and relationships with flexible key-value properties.
- **Book Recommendation Engine:** Generates personalized book suggestions based on a user's network connections.
- **OOP Implementation:** Employs object-oriented principles for modular and reusable code.
- **Unit Testing:** Ensures functionality through comprehensive pytest unit tests.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/diya-ganesh/OOP-Book-Recommendation.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd OOP-Book-Recommendation
   ```
3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Recommendation Engine:**
   ```bash
   python recommend.py
   ```
   - Outputs the original property graph, the recommendation subgraph for a specific user (e.g., Spencer), and a new property graph linking the user to recommended books.

2. **Run Unit Tests:**
   ```bash
   python -m pytest -v --cov --cov-report term-missing
   ```
   - Outputs the test coverage report and validates the implementation of all methods.

## Documentation

- **`propertygraph.py`**: Implements the property graph with nodes, relationships, and graph-level methods.
- **`recommend.py`**: Uses the property graph to generate book recommendations based on user connections.
- **`test_propertygraph.py`**: Contains unit tests for all methods, covering various scenarios and edge cases.

## Contributors

- **Diya Ganesh**: Developer and contributor.

---

For further details, see the [project repository](https://github.com/diya-ganesh/OOP-Book-Recommendation).
