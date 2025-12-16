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

def sort_edges(edges: list) -> list:
    print('Sorting edges...')
    for i in range(0, len(edges)-1):
        for j in range(i+1, len(edges)):
            print(f'Working {i}, {j}')
            if edges[i][2] > edges[j][2]:
                # swap
                temp = edges[i]
                edges[i] = edges[j]
                edges[j] = temp

    return edges

def find_shortest_edge(edges: list):
    smallest = 1e38
    smallest_edge = None
    for edge in edges:
        if edge[2] < smallest:
            smallest = edge[2]
            smallest_edge = edge

    return smallest_edge

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

    us = []
    vs = []
    ds = []
    edge_info = []
    for u, v, data in g.edges(data=True):
        # print(u, v, data['distance'])
        # us.append(u)
        # vs.append(v)
        # ds.append(data['distance'])
        edge_info.append((u, v, data['distance']))

    # before sorting
    # print(edge_info)

    # after sorting
    limit = 1000
    shortest_edges = []
    for i in range(0, limit):
        shortest_edge = find_shortest_edge(edge_info)
        shortest_edges.append(shortest_edge)
        edge_info.remove(shortest_edge)

    # edge_info = sort_edges(edge_info)
    # print(edge_info)

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

    print(f'The answer is {prod}')
    # pos = nx.spring_layout(g)
    # nx.draw(connected, with_labels=True)
    # edge_labels = nx.get_edge_attributes(g, 'distance')
    # nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
    # plt.show()
if __name__ == '__main__':
    main()
