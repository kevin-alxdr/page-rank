import sys
import os
import time
import argparse
from progress import Progress
import random


def load_graph(args):

    """
    Load graph from text file

    Parameters:
    args -- arguments named tuple

    Returns:
    A dict mapping a URL (str) to a list of target URLs (str).
    """

    # Sets current_node as None
    current_node = None

    global school_web_dict
    school_web_dict = {}

    global edgelist
    edgelist = []

    # Iterate through the file line by line
    for line in args.datafile:
        # And split each line into two URLs
        node, target = line.split()

        # Base Case 1: first run
        if current_node is None:
            current_node = node

        # If current_node = node, append edge to the edge list
        if current_node == node:
            # Appends the current edge to the list
            edgelist.append(target)

        # If current_node doesn't = node, empty edge list and update dict so that the node = current_node
        elif current_node != node:

            # Update school_web_dict to the current_node and current edgelist
            school_web_dict.update({current_node: edgelist})

            # Empties edgelist
            edgelist = []
            edgelist.append(target)

            # Sets current_node = to the current_node in "school_web.txt"
            current_node = node

    school_web_dict.update\
        ({current_node: edgelist})
    return school_web_dict

# ======================================================================================================================


def print_stats(graph):
    """Print number of nodes and edges in the given graph"""

    # Prints total number of keys in "school_web.txt"
    print("There are", len(school_web_dict.keys()), "nodes in this graph.")

    # Sets edges to 0
    edges = 0

    # Goes through all of the values/items in school_web.txt
    for x, value in graph.items():

        # Sets edges as the length of the list of values within the graph
        edges += len(list(value))

    # Prints total number of edges
    print("There are", edges, "edges in this graph.")


# ======================================================================================================================

def stochastic_page_rank(graph, args):

    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.

    # PSEUDO CODE
    initialize hit_count[node] with 0 for all nodes
    repeat n_repetitions times:
        current_node <- randomly selected node
        repeat n_steps times:
            current_node <- uniformly randomly chosen among the out edges of current_node
        hit_count[current_node] += 1/n_repetitions 
    """

    # Creates an empty dictionary "hit_count" to save hit frequencies
    hit_count = {}

    # Goes through all of the keys in the graph
    for x in graph.keys():

        # Sets hit frequencies to 0
        hit_count[x] = 0

    # Chooses a random website
    for i in range(args.repeats+1):

        # Chooses a random node from the list of keys in the graph
        current_node = random.choice(list(graph.keys()))

        # Increase the amount of steps by 1
        for j in range(args.steps+1):
            # Chooses a random node from the current node in the graph
            current_node = random.choice(list(graph[current_node]))

        # Divides 1 by the number of repetitions it takes to reach the edges
        hit_count[current_node] += 1/args.repeats

        # Updates the dictionary "hit_count" to display the current node as well as the hitcount of the current node.
        hit_count.update\
            ({current_node: hit_count[current_node]})

    return hit_count

# ======================================================================================================================

def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.

    # PSEUDO CODE
    initialize node_prob[node] = 1/(number of nodes) for all nodes
    repeat n_steps times:
        initialize next_prob[node] = 0 for all nodes
        for each node:
            p <- node_prob[node] divided by its out degree
            for each target among out edges of node:
                next_prob[target] += p
        node_prob <- next_prob
    """

    # Creates empty dictionary "node_prob"
    node_prob = {}

    # Creates temporary empty dictionary "next_prob"
    next_prob = {}

    # For every key in the graph, divide 1 by the length of the keys in the graph
    for x in graph.keys():
        node_prob[x] = 1/len(graph.keys())

    # Set probability to 0 for all nodes
    for i in range(args.repeats + 1):
        for x in graph.keys():
            next_prob[x] = 0

        # For every key in the graph, divide by its out degree
        for x in graph.keys():
            edgeprobability = node_prob[x] / len(graph[x])

            # Adding p to update the edge probability
            for value in graph[x]:
                next_prob[value] += edgeprobability

        # Update the dictionary "node_prob"
        node_prob.update\
            (next_prob)

    return node_prob

# ======================================================================================================================


parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")

# ======================================================================================================================

if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")