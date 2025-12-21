import networkx as nx
import itertools
import matplotlib.pyplot as plt
from datetime import datetime

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
        # node = (parent, children)
        # all_nodes.append(node)        

    return all_edges

# detect circular dependence and remove that edge
def discover_successors(grph: nx.DiGraph, node_name: str, parents: list = [], exits: int = 0, results: list = [], end_node: str = K_END_NODE) -> tuple[int, list]:
    successors = list(grph.successors(node_name))
    local_parents = list(parents)
    
    if node_name not in local_parents:
        local_parents.append(node_name)
    else:
        # circular dependence
        print(f'HOW DID WE GET HERE: Loop back alert: Node {node_name} already exists in parents list {local_parents}.')
    
    # print(local_parents)

    for successor in successors:
        if successor in local_parents:
        # circular dependence
            print(f'Loop back alert: Node {successor} already exists in parents list {local_parents}.')
            print(f'Breaking connection between node {node_name} and node {successor}')
            grph.remove_edge(node_name, successor)

    # refresh successor list with circular dependencies removed
    successors = list(grph.successors(node_name))
    for successor in successors:
        if successor == end_node:
            exits += 1
            result = list(local_parents)
            result.append(successor)
            # print(exits, result)
            if result in results:
                print(f'Path already exists: {result}')
                input('Something is up!')

            results.append(result)
        else:
            exits, results = discover_successors(grph, successor, local_parents, exits, results, end_node)

    return exits, results

# detect circular dependence and remove that edge
def discover_predecessors(grph: nx.DiGraph, node_name: str, children: list = [], exits: int = 0, results: list = [], start_node: str = K_START_NODE) -> tuple[int, list]:
    predecessors = list(grph.predecessors(node_name))
    local_children = list(children)

    if node_name not in local_children:
        local_children.append(node_name)
    else:
        # circular dependence
        print(f'HOW DID WE GET HERE: Loop back alert: Node {node_name} already exists in childrens list {local_children}.')
    
    # print(local_parents)

    for predecessor in predecessors:
        if predecessor in local_children:
        # circular dependence
            print(f'Loop back alert: Node {predecessor} already exists in parents list {local_children}.')
            print(f'Breaking connection between child node {node_name} and parent node {predecessor}')
            grph.remove_edge(predecessor, node_name)

    # refresh successor list with circular dependencies removed
    predecessors = list(grph.predecessors(node_name))
    for predecessor in predecessors:
        if predecessor == start_node:
            exits += 1
            result = list(local_children)
            result.append(predecessor)
            result.reverse()
            print(exits, result)
            if result in results:
                print(f'Path already exists: {result}')
                input('Something is up!')

            results.append(result)
        else:
            exits, results = discover_predecessors(grph, predecessor, local_children, exits, results, start_node)

    return exits, results

def list_extraneous_terminal_nodes(grph: nx.DiGraph, target_terminal_node: str = K_END_NODE) -> tuple[int, list]:
    extraneous_node_count = 0
    extraneous_terminal_nodes = []
    for node_name in grph.nodes:
        successors = list(grph.successors(node_name))
        successor_count = len(successors)

        if successor_count == 0 and node_name != target_terminal_node:
            extraneous_terminal_nodes.append(node_name)
            extraneous_node_count += 1 

    return extraneous_node_count, extraneous_terminal_nodes

# a node that has exactly one successor and its sole predecessor has exactly one successor (this node)
def list_pass_through_nodes(grph: nx.DiGraph, target_terminal_node: str = K_END_NODE) -> tuple[int, list]:
    pass_through_node_count = 0
    pass_through_nodes = []
    for node_name in grph.nodes:
        successors = list(grph.successors(node_name))
        successor_count = len(successors)
        
        predecessors = list(grph.predecessors(node_name))
        predecessor_count = len(predecessors)
        if successor_count == 1 and predecessor_count == 1:
            parent_node = predecessors[0]
            parent_node_children_count = len(list(grph.successors(parent_node)))
            if parent_node_children_count == 1:
                pass_through_nodes.append(node_name)
                pass_through_node_count += 1

    return pass_through_node_count, pass_through_nodes

def remap_pass_through_node(grph: nx.DiGraph, node_name: str):
    # there should be only one successor but check
    successors = list(grph.successors(node_name))

    # there should be at least on predecessor
    predecessors = list(grph.predecessors(node_name))

    if len(successors) == 1 and len(predecessors) == 1:
        grph.remove_edge(node_name, successors[0])

        for predecessor in predecessors:
            # disconnect predecessor from node
            grph.remove_edge(predecessor, node_name)

            # connect predecessor to successor
            grph.add_edge(predecessor, successors[0])

        # drop the node
        # grph.remove_node(node_name)

    return

def part1_solution(fname: str, start_node: str = K_START_NODE, end_node: str = K_END_NODE):
    all_edges = load_data_set(data_file=fname)
    # print(all_edges)    

    g = nx.DiGraph(name='reactor')
    g.add_edges_from(all_edges)

    all_paths = nx.all_simple_paths(g, start_node, end_node)
    all_path_counts = len(list(all_paths))

    print(f'There are {all_path_counts} paths from {start_node} to {end_node}')

    # for result in results:     
    #     print(result)
    print('########### End part 1 ###########')
    
    return

# Three parts to this:
# we know there is no dac between svr and fft
# we know there is no fft between dac and out
# we know there is only one terminal node out
# all paths are connected from svr to out
# therefore the solution is:
# n1 * n2 * n3
# where 
# n1 paths from svr to fft, 
# n2 paths from fft to dac, 
# n3 paths from dac to out
def part2_solution(fname: str):
    all_edges = load_data_set(data_file=fname)

    g2 = nx.DiGraph(name='reactor2')
    g2.add_edges_from(all_edges)

    fft_node = 'fft'
    dac_node = 'dac'
    # Python generators can only be iterated through once.
    # all_simple_paths returns a Generator
    # since the generator will take a long time, do it only once.
    start_time = datetime.now().isoformat(timespec='seconds')
    print(f'{start_time} Starting generating all paths from {K_START_NODE} to {fft_node}')
    n1 = sum(1 for path in nx.all_simple_paths(g2, K_START_NODE, fft_node))
    print(f'All paths from {K_START_NODE} to {fft_node}: {n1}')

    start_time = datetime.now().isoformat(timespec='seconds')
    print(f'{start_time} Starting generating all paths from {fft_node} to {dac_node}')
    n2 = sum(1 for path in nx.all_simple_paths(g2, fft_node, dac_node))
    print(f'All paths from {fft_node} to {dac_node}: {n2}')
    
    start_time = datetime.now().isoformat(timespec='seconds')
    print(f'{start_time} Starting generating all paths from {dac_node} to {K_END_NODE}')
    n3 = sum(1 for path in nx.all_simple_paths(g2, dac_node, K_END_NODE))
    print(f'All paths from {dac_node} to {K_END_NODE}: {n3}')

    time1 = datetime.now().isoformat(timespec='seconds')
    print(f'Done generating all paths: {time1}')

    all_paths_count = n1 * n2 * n3
    
    print(f'There are {all_paths_count} paths from {K_START_NODE} to {K_END_NODE} passing through {fft_node} and {dac_node}')
    
    # # count nodes with no successors
    # extraneous_terminal_nodes = []
    # pass_through_nodes = []
    # count, extraneous_terminal_nodes = list_extraneous_terminal_nodes(g2)
    # print(count, extraneous_terminal_nodes)
    
    # count, pass_through_nodes = list_pass_through_nodes(g2)
    # print(count, pass_through_nodes)

    # # nx.draw(g2, with_labels=True)
    # # plt.show()

    # # remap pass through nodes and simplify the map
    # for node_name in pass_through_nodes:
    #     remap_pass_through_node(g2, node_name)

    # count, pass_through_nodes = list_pass_through_nodes(g2)
    # print(count, pass_through_nodes)
    
    # # nx.draw(g2, with_labels=True)
    # # plt.show()

    # exits, results = discover_successors(g2, start_node)

    # print(f'There are {exits} paths from {start_node} to {end_node}')

    return

def main():
    # # Part 1
    execute_part_1 = False
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
    part2_solution(fname)

    exit(0)
    # starting from srv to out is just too many routes to traverse end to end
    # break it up
    # from trial error, 
    # svr to fft is 2588 paths (with no dac inbetween)
    # dac to out is 19,289 paths (with no fft inbetween)

    # start at 'dac' and find all paths to the end.
    start_node = 'dac'
    end_node = K_END_NODE
    print(f'SUCCESSORS from {start_node}')
    # weird. If results = [] is not passed, the results from previous run (above) are included.
    all_exits, successors_paths = discover_successors(g2, start_node, results=[], end_node=end_node)

    all_exits_with_target = 0
    target_node = 'fft'
    for item in successors_paths:
        if target_node in item:
            all_exits_with_target += 1

    print(f'Candidates from {start_node} to {K_END_NODE}: {all_exits}')
    print(f'Candidates from {start_node} to {K_END_NODE} with target {target_node}: {all_exits_with_target}')

    input('Waiting...')

    start_node = 'fft'
    end_node = 'dac'
    print(f'SUCCESSORS from {start_node}')
    # weird. If results = [] is not passed, the results from previous run (above) are included.
    all_exits, successors_paths = discover_successors(g2, start_node, results=[], end_node=end_node)

    print(f'Candidates from {start_node} to {end_node}: {all_exits}')

    input('Waiting...')

    print('PREDECESSORS')
    origin_node = 'svr'
    start_node = 'fft'
    target_node = 'dac'
    results = []
    all_entrances, origin_paths = discover_predecessors(g2, start_node, results=[], start_node=origin_node)

    all_entrances_with_target_node = 0
    for item in origin_paths:
        item.remove(start_node)
        if target_node in item:
            all_entrances_with_target_node += 1

    print(f'Candidates from {start_node} to {K_START_NODE}: {all_entrances}')
    print(f'Candidates from {start_node} to {K_START_NODE} with target {target_node}: {all_entrances_with_target_node}')

    input('Waiting...')
    # for item in origin_paths:
    #     print(item)

    # build all combinations of orign and successor paths
    print('Building combinations')
    candidate_count = 0
    total_count = 0
    
    for origin, successor in itertools.product(origin_paths, successors_paths):
        candidate = list(origin)
        candidate.extend(successor)
        # print(candidate)
        total_count += 1
        if target_node in candidate:
            candidate_count += 1

    print(f'Number of paths from {K_START_NODE} to {K_END_NODE} containing {start_node}: {total_count}')    
    print(f'Number of paths from {K_START_NODE} to {K_END_NODE} containing {start_node} and {target_node}: {candidate_count}')

if __name__ == '__main__':
    main()
