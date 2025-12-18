import itertools

K_RED_TILE = '#'
K_GREEN_TILE = 'X'
K_OTHER_TILE = '.'

# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    all_nodes = []
    for i, line in enumerate(lines):
        coordinates = line.split(',')
        coordinates = [int(s) for s in coordinates]
        node = (coordinates[0], coordinates[1])
        all_nodes.append(node)        

    return all_nodes

# remember to add 1 for number of items (and not distance)
def calculate_tiles_in_area(node1, node2) -> int:
    x = abs(node1[0] - node2[0]) + 1
    y = abs(node1[1] - node2[1]) + 1
    area = x*y
    return area

def part1_answer(all_nodes: list) -> None:
    # use itertools to generate a combination of 2 nodes
    biggest_area = 0
    for node1, node2 in itertools.combinations(all_nodes, 2):
        area = calculate_tiles_in_area(node1=node1, node2=node2)
        if area > biggest_area:
            biggest_area = area

    print(f'Biggest area: {biggest_area}')

def part2_answer(grid: list, all_nodes: list) -> None:
    # use itertools to generate a combination of 2 nodes
    biggest_area = 0
    for i, (node1, node2) in enumerate(itertools.combinations(all_nodes, 2)):
        # sub_grid = get_sub_grid(grid, node1, node2)
        # flattened_sub_grid = flatten(sub_grid)
        # is_valid = is_allowed_sub_grid(flattened_sub_grid)
        is_valid = is_red_green_grid(grid, node1, node2)

        if is_valid:
            area = calculate_tiles_in_area(node1=node1, node2=node2)
            if area > biggest_area:
                biggest_area = area
        
        print(f'Running {i} biggest area {biggest_area}')

    print(f'Biggest area: {biggest_area}')

def populate_red_tiles(grid: list, all_nodes: list) -> list:
    print('Populating red tiles...')
    for node in all_nodes:
        x = node[0]
        y = node[1]
        grid[y][x] = K_RED_TILE
    
    return grid

def populate_green_tiles(grid: list, all_nodes: list) -> list:
    print('Populating green tiles...')
    for node1, node2 in itertools.combinations(all_nodes, 2):
        c1 = node1[0]
        c2 = node2[0]
        r1 = node1[1]
        r2 = node2[1]

        if c1 == c2:
            start = r1
            end = r2
            if r1 > r2:
                start = r2
                end = r1
            
            for i in range(start+1, end):
                grid[i][c1] = K_GREEN_TILE
                
        
        if r1 == r2:
            start = c1
            end = c2
            if c1 > c2:
                start = c2
                end = c1
            
            temp = list(grid[r1])
            for i in range(start+1, end):
                grid[r1][i] = K_GREEN_TILE
                
    return grid

def fill_in_green_tiles(grid: list) -> list:
    print('Filling in green tiles...')
    for i in range(0, len(grid)):
        row = grid[i]
        start, end = colored_tile_boundary(row)

        if start >= 0 and end >=0:
            for j in range(start, end + 1):
                if row[j] == K_OTHER_TILE:
                    row[j] = K_GREEN_TILE

    return grid

def colored_tile_boundary(row: list) -> tuple[int, int]:
    start = -1
    end = -1
    for i in range(len(row)):
        if row[i] == K_GREEN_TILE or row[i] == K_RED_TILE:
            start = i
            break
    
    if start > -1:
        for i in range(len(row)-1, 0, -1):
            if row[i] == K_GREEN_TILE or row[i] == K_RED_TILE:
                end = i
                break

    return start, end

# def get_sub_grid(grid: list, node1: tuple[int, int], node2: tuple[int, int]) -> list:
#     c1 = node1[0]
#     c2 = node2[0]
#     r1 = node1[1]
#     r2 = node2[1]

#     if c1 > c2:
#         temp = c1
#         c1 = c2
#         c2 = temp

#     if r1 > r2:
#         temp = r1
#         r1 = r2
#         r2 = temp
    
#     sub_grid = []

#     for i in range(r1, r2+1):
#         row = grid[i]
#         sub_grid.append(row[c1:c2+1])
    
#     return sub_grid
    
# def flatten(grid: list) -> list:
#     flat = []
#     for row in grid:
#         flat.extend(row)

#     return flat

# def is_allowed_sub_grid(flattened_grid: list) -> bool:
#     allowed = True
#     if K_OTHER_TILE in flattened_grid:
#         allowed = False

#     return allowed

def is_red_green_grid(grid: list, node1: tuple[int, int], node2: tuple[int, int]) -> bool:
    valid = True

    c1 = node1[0]
    c2 = node2[0]
    r1 = node1[1]
    r2 = node2[1]

    if c1 > c2:
        temp = c1
        c1 = c2
        c2 = temp

    if r1 > r2:
        temp = r1
        r1 = r2
        r2 = temp

    for i in range(r1, r2+1):
        line = grid[i][c1:c2+1]
        if K_OTHER_TILE in line:
            valid = False
            break

    return valid 

def grid_size(all_nodes: list) -> tuple[int, int]:
    c_max = 0
    r_max = 0
    for node in all_nodes:
        if node[0] > c_max:
            c_max = node[0]
        
        if node[1] > r_max:
            r_max = node[1]

    return (c_max+1, r_max+1)

def translate_grid(all_nodes: list) -> list:
    c_min = min(all_nodes, key=lambda x: x[0])[0]
    r_min = min(all_nodes, key=lambda x: x[1])[1]
    
    new_nodes = []
    for i in range(len(all_nodes)):
        node = (all_nodes[i][0] - c_min, all_nodes[i][1] - r_min)
        new_nodes.append(node)

    return new_nodes

def main():
    fname = r'Day_09\inputs.txt'
    fname = r'Day_09\sample_inputs.txt'

    all_nodes = load_data_set(data_file=fname)
    # print(all_nodes)    
    part1_answer(all_nodes=all_nodes)

    # prepare for part 2
    # build the grid
    all_nodes = translate_grid(all_nodes)
    cols, rows = grid_size(all_nodes=all_nodes)
    print(rows, cols)
    grid = ['.'] * rows
    for i in range(len(grid)):
        grid[i] = ['.'] * cols

    grid = populate_red_tiles(grid, all_nodes)
    grid = populate_green_tiles(grid, all_nodes)

    for i in grid:
        print(''.join(i))

    # print()
    grid = fill_in_green_tiles(grid)
    # for i in grid:
    #     print(''.join(i))

    # sub_grid = get_sub_grid(grid, all_nodes[0], all_nodes[2])
    # for i in sub_grid:
    #     print(''.join(i))

    # flat_sub_grid = flatten(sub_grid)
    # print(flat_sub_grid)

    print('Starting solving Part 2...')
    part2_answer(grid, all_nodes)

if __name__ == '__main__':
    main()
