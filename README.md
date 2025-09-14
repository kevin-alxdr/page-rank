# PageRank – Web Graph Analysis  
Python CLI Project

This project was developed as part of the university module CSC1034 to demonstrate graph algorithms and PageRank implementation in Python.

## Overview
A Python-based implementation of the PageRank algorithm for analyzing web graphs. This project allows users to compute the relative importance of pages using both **stochastic (random walk) and distribution-based methods**. The program can process a text file containing web links and outputs the top-ranked pages along with their scores.  

Designed for a console interface, it includes interactive arguments for selecting algorithms, adjusting steps and repetitions, and limiting the number of results displayed.

## Features
- Supports two PageRank algorithms:  
  - Stochastic (random walk)  
  - Distribution (probabilistic iterative method)  
- Loads web graph data from a text file (`node target` per line)  
- Prints total number of nodes and edges  
- Displays top N ranked pages with scores  
- Adjustable parameters via CLI: steps, repetitions, number of results  
- Efficient handling of graph data for larger datasets  

## Tech Stack
- **Language:** Python 3  
- **Libraries:** `argparse`, `random`, `time`  
- **Environment:** Command-line interface  

## Usage

### Prerequisites
- Python 3 installed
- Optional: `argparse` and `random` are part of standard library  

### Installation
Clone the repository:

```bash
git clone https://github.com/yourusername/page-rank.git
cd page-rank
```
How to Run
Run the program from the command line:
```
python pagerank.py path/to/school_web.txt --method stochastic --repeats 100000 --steps 100 --number 20
