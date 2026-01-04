import networkx as nx
import itertools
import matplotlib.pyplot as plt
from datetime import datetime
from math import prod

K_END_NODE = 'out'
K_START_NODE = 'svr' 

# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    all_edges = []
    for i, line in enumerate(lines):
        items = line.split(':')
        parent = items[0]
        children = items[1].strip().split()
        for child in children:
            all_edges.append((parent, child))

    return all_edges

def part1_solution(fname: str, start_node: str = K_START_NODE, end_node: str = K_END_NODE):
    all_edges = load_data_set(data_file=fname)

    g = nx.DiGraph(name='reactor')
    g.add_edges_from(all_edges)

    all_paths = nx.all_simple_paths(g, start_node, end_node)
    all_path_counts = len(list(all_paths))

    print(f'There are {all_path_counts} paths from {start_node} to {end_node}')

    # for result in results:     
    #     print(result)
    print('########### End part 1 ###########')
    
    return

# Counting paths between a source node \(S\) and a destination node \(D\) 
# in a Directed Acyclic Graph (DAG) is a classic dynamic programming problem. 
# The key is to process the nodes in a topological order. 
def part2_solution(fname: str, start_node: str, end_node: str) -> int:
    # build the base graph
    all_edges = load_data_set(data_file=fname)
    g2 = nx.DiGraph(name='reactor2')
    g2.add_edges_from(all_edges)

    # Python generators can only be iterated through once.
    # topological_sort returns a Generator
    sorted = list(nx.topological_sort(g2))
    # print(sorted)

    start = sorted.index(start_node)
    end = sorted.index(end_node)

    target = list(sorted[start: end + 1])
    # print(target)
    counts = [0] * len(target)
    counts[0] = 1

    for i, t in enumerate(target):
        successors = list(g2.successors(t))
        # print(f'{i}: {t} successors {successors}')
        for s in successors:
            try:
                idx = target.index(s)
                counts[idx] = counts[idx] + counts[i]
                # print(counts)
            except ValueError as e:
                print(f'{i}: {t} successor {s} is not in sublist')

    # print(f'Number of paths from {start_node} to {end_node}: {counts[-1]}')
    return counts[-1]
          
def main():
    # # Part 1
    execute_part_1 = True
    if execute_part_1:
        start_node = 'you'
        fname = r'Day_11\inputs.txt'
        # fname = r'Day_11\sample_inputs.txt'
        part1_solution(fname, start_node)

    # Part 2
    start_node = 'fft'
    end_node = 'dac'
    fname = r'Day_11\inputs.txt'
    # fname = r'Day_11\sample_inputs_part2.txt'

    paths1 = 1
    paths2 = 1
    paths3 = 1 
    paths1 = part2_solution(fname, K_START_NODE, start_node)
    paths2 = part2_solution(fname, start_node, end_node)
    paths3 = part2_solution(fname, end_node, K_END_NODE)

    print(f'Results:')
    print(f'Paths from {K_START_NODE} to {start_node}: {paths1}')
    print(f'Paths from {start_node} to {end_node}: {paths2}')
    print(f'Paths from {end_node} to {K_END_NODE}: {paths3}')
    paths = prod([paths1, paths2, paths3])
    print(f'Paths from {K_START_NODE} to {K_END_NODE} visiting {start_node} and {end_node}: {paths}')

    # Answer is: 479511112939968
    # Paths from svr to fft: 2588
    # Paths from fft to dac: 18007824
    # Paths from dac to out: 10289
    # Paths from svr to out visiting fft and dac: 479511112939968
    
    # using nx.all_simple_paths works for smaller graphs or node set. 
    # It was successful and within reasonable computational time to discover
    # paths from svr to fft, and dac to out by breaking them up
    # svr to fft is 2588 paths (with no dac inbetween)
    # dac to out is 10,289 paths (with no fft inbetween)
    # but the approach was not reasonable to fft to dac.
    # The code was started on "2025-12-21T15:08:25::Starting counting all paths from svr to fft"
    # and as of 2026-01-04 15:30 (2 weeks later), it was still running!
    # A parallel code that was printing each path found had found 4,337,797 paths of the 18,007,824 paths (~25% of the way there!)  

if __name__ == '__main__':
    main()
