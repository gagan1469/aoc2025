import networkx as nx
import itertools
import matplotlib.pyplot as plt
# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    all_nodes = []
    for i, line in enumerate(lines):
        coordinates = line.split(',')
        coordinates = [int(s) for s in coordinates]
        node = (i, {'x': coordinates[0], 'y': coordinates[1], 'z': coordinates[2]})
        all_nodes.append(node)        

    return all_nodes

def calculate_distance(g: nx.Graph, node1, node2) -> int:
    distance = (g.nodes[node1]['x'] - g.nodes[node2]['x']) ** 2
    distance += (g.nodes[node1]['y'] - g.nodes[node2]['y']) ** 2
    distance += (g.nodes[node1]['z'] - g.nodes[node2]['z']) ** 2
    return distance

def part1_solution(g: nx.Graph, shortest_edges: list) -> None:
    connected = nx.Graph()
    print('Building the subset connected graph')
    for i, item in enumerate(shortest_edges):
        print(f'Processing item {i}')
        node1 = g.nodes[item[0]]
        node2 = g.nodes[item[1]]
        
        if item[0] not in connected:
            connected.add_node(item[0], x=node1['x'], y=node1['y'], z=node1['z'])

        if item[1] not in connected:
            connected.add_node(item[1], x=node2['x'], y=node2['y'], z=node2['z'])

        edge_data = g.get_edge_data(item[0], item[1])
        connected.add_edge(item[0], item[1], **edge_data)

    print('Count connected nodes')
    connected_nodes = []
    for i, node in enumerate(connected.nodes):
        print(f'Processing item {i}')
        count = nx.node_connected_component(connected, node)
        if count not in connected_nodes:
            connected_nodes.append(count)

    print(connected_nodes)
    # number of circuits
    circuit_size = []
    print('Calculating circuit sizes...')
    for i, connected_node in enumerate(connected_nodes):
        print(f'Processing item {i}')
        if len(connected_node) not in circuit_size:
            circuit_size.append(len(connected_node))
    
    circuit_size.sort(reverse=True)
    print(circuit_size)

    prod = 1
    for size in circuit_size[:3]:
        prod *= size

    print(f'Part 1: The answer is {prod}')

def part2_solution(g: nx.Graph, sorted_edges: list) -> None:
    connected = nx.Graph()
    print('Building the subset connected graph')

    # add all the nodes
    print(f'Adding all nodes to graph...')
    for i, item in enumerate(sorted_edges):
        
        node1 = g.nodes[item[0]]
        node2 = g.nodes[item[1]]
        
        if item[0] not in connected:
            connected.add_node(item[0], x=node1['x'], y=node1['y'], z=node1['z'])

        if item[1] not in connected:
            connected.add_node(item[1], x=node2['x'], y=node2['y'], z=node2['z'])

    # start connecting the nodes in ascending order of distance
    print(f'Connecting nodes in ascending order of distance...')
    for i, item in enumerate(sorted_edges):
        edge_data = g.get_edge_data(item[0], item[1])
        connected.add_edge(item[0], item[1], **edge_data)

        # if isolates becomes 0, everything is connected
        count_isolates = nx.number_of_isolates(connected)
        print(f'Junction boxes remaining: {count_isolates}')
        if count_isolates == 0:
            print(f'Circuit is complete!!!!')
            final_set = item
            break
    
    print(f'The final connection is: {final_set}')
    print(f'Node1 {connected.nodes[final_set[0]]}')
    print(f'Node1 {connected.nodes[final_set[1]]}')
    x1 = connected.nodes[final_set[0]]['x']
    x2 = connected.nodes[final_set[1]]['x']
    prod = x1 * x2
    print(f'Part 2: The answer is {prod}')

def main():
    fname = r'Day_08\inputs.txt'
    # fname = r'Day_08\sample_inputs.txt'

    all_nodes = load_data_set(data_file=fname)
    # print(all_nodes)    

    g = nx.Graph(name='junction_boxes')
    g.add_nodes_from(all_nodes)

    # use itertools to generate a combination of 2 nodes to build complete graph
    for node1, node2 in itertools.combinations(g.nodes, 2):
        if not g.has_edge(node1, node2):
            distance = calculate_distance(g, node1, node2)
            g.add_edge(node1, node2, distance=distance)

    # To sort edges in NetworkX by an attribute, you retrieve the edges using G.edges(data=True) 
    # and then use Python's built-in sorted() function with a key argument. 
    # More efficient than writing a sort routine!
    edge_info = g.edges(data=True)
    # edge_info is:
    # [(0, 1, {'distance': 620651}), (0, 2, {'distance': 825889}), (0, 3, {'distance': 315528}), ..]
    # TypeError: 'EdgeDataView' object is not subscriptable
    # The attribute dict is index 2, i.e., x[2]
    # can use x[2].get('distance', 1e38) to be safe
    sorted_edges = sorted(edge_info, key=lambda x: x[2]['distance'])
    
    # Part 1
    limit = 1000
    shortest_edges = sorted_edges[:limit]
    part1_solution(g, shortest_edges)

    # Part 2 - keep adding connections until there is only one circuit
    # identify the first connection that connects everything together
    part2_solution(g, sorted_edges)

    # pos = nx.spring_layout(g)
    # nx.draw(connected, with_labels=True)
    # edge_labels = nx.get_edge_attributes(g, 'distance')
    # nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
    # plt.show()

if __name__ == '__main__':
    main()
