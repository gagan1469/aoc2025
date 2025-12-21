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

def part1_answer(all_nodes: list) -> int:
    # use itertools to generate a combination of 2 nodes
    biggest_area = 0
    for node1, node2 in itertools.combinations(all_nodes, 2):
        area = calculate_tiles_in_area(node1=node1, node2=node2)
        if area > biggest_area:
            biggest_area = area

    print(f'Biggest area: {biggest_area}')
    return biggest_area

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

def big_area_candidates(biggest_area: int, all_nodes: list, threshold: int = 0.25) -> list:
    candidates = []
    for node1, node2 in itertools.combinations(all_nodes, 2):
        area = calculate_tiles_in_area(node1=node1, node2=node2)
        if area > threshold * biggest_area:
            candidates.append((node1, node2, area))

    candidates = sorted(candidates, key=lambda x: x[2], reverse=True)
    return candidates

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

# def translate_grid(all_nodes: list) -> list:
#     c_min = min(all_nodes, key=lambda x: x[0])[0]
#     r_min = min(all_nodes, key=lambda x: x[1])[1]
    
#     new_nodes = []
#     for i in range(len(all_nodes)):
#         node = (all_nodes[i][0] - c_min, all_nodes[i][1] - r_min)
#         new_nodes.append(node)

#     return new_nodes

def build_grid(rows: int, cols: int, chunk_size: int = 5) -> None:
    output = r'Day_09\output'
 
    grid = ['.'] * rows
    for i in range(0, len(grid), chunk_size):
        ofile = output + '_' + str(i) + '.txt'
        with open(ofile, 'w') as f:
            end = i + chunk_size if i + chunk_size < len(grid) else len(grid)
            for j in range(i, end):
                f.write('.' * cols)
                f.write('\n')
        # grid[i] = ['.'] * cols

    return

def place_grid_red_green_tiles(rows: int, cols: int, all_nodes: list, chunk_size: int = 5) -> None:
    output = r'Day_09\output'
    remaining_nodes = list(all_nodes)
    remaining_nodes = sort_nodes_by_row(remaining_nodes)

    grid = ['.'] * rows
    for i in range(0, len(grid), chunk_size):
        ofile = output + '_' + str(i) + '.txt'
        with open(ofile, 'w') as f:
            end = i + chunk_size if i + chunk_size < len(grid) else len(grid)
            for j in range(i, end):
                remaining_nodes, row_nodes = get_row_nodes(j, remaining_nodes)
                print(j, remaining_nodes)
                line = ['.'] * cols
                min_c = cols + 1
                max_c = -1
                for node in row_nodes:
                    line[node[0]] = K_RED_TILE
                    min_c = node[0] if min_c > node[0] else min_c
                    max_c = node[0] if max_c < node[0] else max_c

                for i in range(min_c+1, max_c):
                    if line[i] == K_OTHER_TILE:
                        line[i] = K_GREEN_TILE

                line = ''.join(line)
                f.write(line)
                f.write('\n')
    return

def vertical_fill_green_tiles(total_rows: int, all_nodes: list, chunk_size: int = 5) -> None:
    prefix = r'Day_09\output'    
    
    remaining_nodes = list(all_nodes)
    remaining_nodes = sort_nodes_by_col(all_nodes)

    for i in range(0, total_rows, chunk_size):
        output_lines = []
        small_grid = ['.'] * chunk_size
        working_file = prefix + '_' + str(i) + '.txt'
        with open(working_file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                small_grid[i] = list(line)

        
        cols = len(small_grid[0])
        for j in range(0, cols):
            col_nodes, remaining_nodes = get_col_nodes(j, remaining_nodes)

            # sort the col_nodes by row
            col_nodes = sort_nodes_by_row(col_nodes)
            print(col_nodes)
            processed_col_nodes = []
            
            for col_node1, col_node2 in zip(col_nodes[:-1], col_nodes[1:]):
                r1 = col_node1[1]
                r2 = col_node2[1]

                r1_t = r1 - i * chunk_size
                r2_t = r2 - i * chunk_size
                if r1_t < i + chunk_size:
                    processed_col_nodes.append(col_node1)
                    if r2_t < i + chunk_size:
                        # simplest the data is all within the chunk
                        processed_col_nodes.append(col_node1)
                        for k in range(r1_t+1, r2_t):
                            print(k)
                            if small_grid[j][k] == K_OTHER_TILE:
                                small_grid[j][k] = K_GREEN_TILE
                    else:
                        # r2 overflows
                        limit = i + chunk_size
                        for k in range(r1_t+1, limit):
                            if small_grid[j][k] == K_OTHER_TILE:
                                small_grid[j][k] = K_GREEN_TILE
                        # if r2 has flowed over, successors will too.
                        break

            for processed_node in processed_col_nodes:
                col_nodes.pop(processed_node)





                
        for line in small_grid:             
            row = ''.join(line)
            output_lines.append(row)

            with open(working_file, 'w') as f:
                f.writelines(output_lines)
    
    return

def horizontal_fill_green_tiles(total_rows: int, chunk_size: int = 5) -> None:
    prefix = r'Day_09\output'
    for i in range(0, total_rows, chunk_size):
        output_lines = []
        working_file = prefix + '_' + str(i) + '.txt'
        with open(working_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                row = list(line)
                start, end = colored_tile_boundary(row)

                if start >= 0 and end >=0:
                    for j in range(start, end + 1):
                        if row[j] == K_OTHER_TILE:
                            row[j] = K_GREEN_TILE

                row = ''.join(row)
                output_lines.append(row)

        with open(working_file, 'w') as f:
            f.writelines(output_lines)
    
    return

def get_row_nodes(row: int, remaining_nodes: list) -> tuple[list, list]:
    # ensure the nodes are sorted.
    row_nodes = []

    i = 0
    while len(remaining_nodes) > 0:
        item_row = remaining_nodes[i][1]
        if item_row == row:
            row_nodes.append(remaining_nodes[i])
            remaining_nodes.pop(i)
        else:
            i += 1

        if item_row > row:
            break        

    return remaining_nodes, row_nodes

def get_col_nodes(col: int, remaining_nodes: list) -> tuple[list, list]:
    # ensure the nodes are sorted.
    col_nodes = []

    i = 0
    while len(remaining_nodes) > 0:
        item_col = remaining_nodes[i][0]
        if item_col == col:
            col_nodes.append(remaining_nodes[i])
            remaining_nodes.pop(i)
        else:
            i += 1

        if item_col > col:
            break        

    return remaining_nodes, col_nodes

def sort_nodes_by_row(all_nodes: list) -> list:
    print(all_nodes)
    all_nodes = sorted(all_nodes, key=lambda x: x[1])
    print(all_nodes)
    return all_nodes

def sort_nodes_by_col(all_nodes: list) -> list:
    print(all_nodes)
    all_nodes = sorted(all_nodes, key=lambda x: x[0])
    print(all_nodes)
    return all_nodes

def main():
    fname = r'Day_09\inputs.txt'
    fname = r'Day_09\sample_inputs.txt'

    all_nodes = load_data_set(data_file=fname)
    # print(all_nodes)    
    biggest_area = part1_answer(all_nodes=all_nodes)

    # prepare for part 2    
    candidates = big_area_candidates(biggest_area, all_nodes)
    print(candidates)

    # build the grid
    cols, rows = grid_size(all_nodes=all_nodes)
    print(rows, cols)

    # the grid is too large to manipulate in memory
    # written out to file, it is 9 GB! 
    chunk_size = 5

    # build_grid(rows, cols, chunk_size)
    place_grid_red_green_tiles(rows, cols, all_nodes, chunk_size)
    input('Wait for it...')

    horizontal_fill_green_tiles(rows, chunk_size)
    vertical_fill_green_tiles(rows, all_nodes, chunk_size)

    exit(0)

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
    # grid is too big to build in memory
    part2_answer(grid, all_nodes)

if __name__ == '__main__':
    main()
