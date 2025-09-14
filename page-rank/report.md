Code Optimisation

In order to optimise my code, I made several changes that improve its quality, efficiency, and flexibility. These optimisations make the program easier to maintain, more adaptable to different datasets, and more efficient when processing large inputs.

1. Dynamic starting node (removing hard-coding)

Originally, the starting node was hard-coded as:

current_node = "http://www.ncl.ac.uk/computing/"


This tied the program to one dataset. I replaced it with:

current_node = None

if current_node is None:
    current_node = node


This ensures the first node in the input file (school_web.txt) is automatically set as the starting node, making the code work for any dataset without manual changes.

2. Efficient graph loading

In the load_graph() function, all outgoing edges for a node are collected in a temporary list before being written to the dictionary. This avoids updating the dictionary for every single edge:

if current_node == node:
    edgelist.append(target)
elif current_node != node:
    school_web_dict.update({current_node: edgelist})
    edgelist = []
    edgelist.append(target)
    current_node = node


This reduces unnecessary dictionary operations and improves efficiency when handling larger input files.

3. Built-in random selection

In the stochastic PageRank method, I used Python’s built-in function:

current_node = random.choice(list(graph.keys()))
current_node = random.choice(list(graph[current_node]))


This is simpler and more efficient than manually generating random indices, while being easier to understand and maintain.

4. Incremental normalisation in stochastic PageRank

When counting hits during the random walks, I normalised results incrementally instead of performing an additional pass at the end:

hit_count[current_node] += 1/args.repeats


This avoids an extra loop, reducing unnecessary work.

5. Reusing probability dictionaries in distribution PageRank

In the distribution method, probabilities are updated in a temporary dictionary (next_prob) that is reset each iteration:

for i in range(args.repeats + 1):
    for x in graph.keys():
        next_prob[x] = 0
    ...
    node_prob.update(next_prob)


This reuses the same dictionary instead of creating a new one each time, which is more memory-efficient.

6. Sorting rankings once

To produce the top-ranked pages, I sort the results once and slice the top N:

top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)


This is more efficient than repeatedly searching for the highest values.

7. Usability with argparse defaults

The program uses argparse with sensible defaults such as:

parser.add_argument('-r', '--repeats', type=int, default=1_000_000)
parser.add_argument('-s', '--steps', type=int, default=100)


This allows the program to run immediately without requiring extra arguments, improving usability.

8. Accurate performance measurement

Only the ranking algorithm itself is wrapped in a timer:

start = time.time()
ranking = algorithm(graph, args)
stop = time.time()


This ensures that only the computation time of the chosen PageRank algorithm is measured, giving a fair comparison between methods.