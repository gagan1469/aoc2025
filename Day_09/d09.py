import itertools
from datetime import datetime

# Part 2: evaluating each candidate takes a long time. In ~8 hours, 1215 candidates were evaluated!
# each candidate takes ~0.6 minutes to evaluate. That would take 51 days for 500*499/2 candidates!
# try multiprocessing
import multiprocessing
from functools import partial
import os

K_RED_TILE = '#'
K_GREEN_TILE = 'X'
K_OTHER_TILE = '.'

K_COLUMN_COORDINATE = 'column'
K_ROW_COORDINATE = 'row'

# read the inputs 
# coordinates are (column, row)
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

# remember to add 1 for number of items (and not distance between the points)
def calculate_tiles_in_area(node1, node2) -> int:
    x = abs(node1[0] - node2[0]) + 1
    y = abs(node1[1] - node2[1]) + 1
    area = x*y
    return area

# identify biggest area candidates for testing for Part 2
def big_area_candidates(biggest_area: int, all_nodes: list, threshold: float = 0.25) -> list:
    candidates = []
    for node1, node2 in itertools.combinations(all_nodes, 2):
        area = calculate_tiles_in_area(node1=node1, node2=node2)
        if area > threshold * biggest_area:
            candidates.append((node1, node2, area))

    candidates = sorted(candidates, key=lambda x: x[2], reverse=True)
    return candidates

# find the first and last coloured tiles in a row
# everything in between can be made green later
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

# get the size of grid needed based on all coordinates read in
def grid_size(all_nodes: list) -> tuple[int, int]:
    c_max = 0
    r_max = 0
    for node in all_nodes:
        if node[0] > c_max:
            c_max = node[0]
        
        if node[1] > r_max:
            r_max = node[1]

    return (c_max+1, r_max+1)

# start with an empty grid and place all red tiles according to the coordinates
# process in chunks of rows
# order the coordinates by row in ascending order
# place the red tiles in the row and then fill in green tiles between
# the left most and right most red tiles
def place_grid_red_green_tiles(rows: int, cols: int, all_nodes: list, chunk_size: int = 5000) -> None:
    output = r'Day_09\output'
    remaining_nodes = list(all_nodes)
    remaining_nodes = sort_nodes(remaining_nodes)

    for i in range(0, rows, chunk_size):
        ofile = output + '_' + str(i) + '.txt'
        print(f'Initial red/green tile placement: Processing file {ofile}...')
        with open(ofile, 'w') as f:            
            end = i + chunk_size if i + chunk_size < rows else rows
            for j in range(i, end):
                row_nodes, remaining_nodes = get_nodes_at_coordinate(j, remaining_nodes)
                # print(j, remaining_nodes)
                line = ['.'] * cols
                min_c = cols + 1
                max_c = -1
                for node in row_nodes:
                    line[node[0]] = K_RED_TILE
                    min_c = node[0] if min_c > node[0] else min_c
                    max_c = node[0] if max_c < node[0] else max_c

                # place green tiles
                # for i in range(min_c+1, max_c):
                #     if line[i] == K_OTHER_TILE:
                #         line[i] = K_GREEN_TILE

                line = ''.join(line)
                if j < end - 1:
                    line += '\n'
                f.write(line)

    return
# fill in green tiles vertically between the top most and bottom most red times by column by file chunk
def vertical_fill_green_tiles(cols: int, all_nodes: list, chunk_size: int = 5000) -> None:
    prefix = r'Day_09\output'    
    col_nodes = []
    remaining_nodes = list(all_nodes)
    remaining_nodes = sort_nodes(all_nodes, sort_by='column')
    # print(f'Sorted by column: {remaining_nodes}')

    for j in range(0, cols):
        col_nodes, remaining_nodes = get_nodes_at_coordinate(j, remaining_nodes, K_COLUMN_COORDINATE)
        col_nodes = sort_nodes(col_nodes)
        # print(f'col {j} nodes: {col_nodes}, remaining: {remaining_nodes}')
        
        # if there are than 1 red tiles in the column
        min_row = int(1e38)
        max_row = int(-1e38)
        if len(col_nodes) > 1:
            for node in col_nodes:
                min_row = node[1] if node[1] < min_row else min_row
                max_row = node[1] if node[1]> max_row else max_row

            r1_file_number = min_row // chunk_size
            r2_file_number = max_row // chunk_size
            r1_t = min_row % chunk_size
            r2_t = max_row % chunk_size
            
            # print(f'original rows {min_row}, {max_row} translated files: ({r1_file_number},{r2_file_number}) rows ({r1_t}, {r2_t})')

            for k in range(r1_file_number, r2_file_number + 1):
                small_grid = [] 
                file_index = k * chunk_size
                working_file = prefix + '_' + str(file_index) + '.txt'
                print(f'Vertical filling: Processing file {working_file} for column {j}')
            
                with open(working_file, 'r') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        small_grid.append(list(line))

                # if in the same file
                if r1_file_number == r2_file_number:
                    local_start = r1_t + 1
                    local_end = r2_t
                else: # (r1_file_number > r2_file_number)
                    if k == r1_file_number:
                        local_start = r1_t + 1
                        local_end = chunk_size
                    elif k == r2_file_number:
                        local_start = 0
                        local_end = r2_t
                    else:
                        local_start = 0
                        local_end = chunk_size

                for i in range(local_start, local_end):
                    if small_grid[i][j] == K_OTHER_TILE:
                        # print(f'file {working_file}: Filling in {K_GREEN_TILE} at row {i} col {j}')
                        small_grid[i][j] = K_GREEN_TILE
                        
                output_lines = []
                for line in small_grid:             
                    row = ''.join(line)
                    output_lines.append(row)

                with open(working_file, 'w') as f:
                    f.writelines(output_lines)
    
    return

# finally, fill in green tiles in a row between the left most red/green tile and the right most red/green tile
def horizontal_fill_green_tiles(total_rows: int, chunk_size: int = 5000) -> None:
    prefix = r'Day_09\output'
    for i in range(0, total_rows, chunk_size):
        output_lines = []
        working_file = prefix + '_' + str(i) + '.txt'
        print(f'Horizontal filling: Processing file {working_file}...')
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

# test that each row of the candidate area between its columns only has red/green tile
def is_red_green_candidate(candidate: tuple[tuple[int, int], tuple[int, int], int], chunk_size: int = 5000) -> tuple[bool, tuple[tuple[int, int], tuple[int, int], int]]:
    prefix = r'Day_09\output'
    candidate_start = datetime.now()
    print(f'Started {os.getpid()}::candidate: {candidate}: ::: Start time: {candidate_start.isoformat(timespec='seconds')}')
    
    node1 = candidate[0]
    node2 = candidate[1]
    # area = candidate[2]
    valid = True

    c1 = min(node1[0], node2[0])
    c2 = max(node1[0], node2[0])
    r1 = min(node1[1], node2[1])
    r2 = max(node1[1], node2[1])

    r1_file_number = r1 // chunk_size
    r2_file_number = r2 // chunk_size
    r1_t = r1 % chunk_size
    r2_t = r2 % chunk_size
            
    # print(f'original rows {r1}, {r2} translated files: ({r1_file_number},{r2_file_number}) rows ({r1_t}, {r2_t})')

    for k in range(r1_file_number, r2_file_number + 1):
        file_index = k * chunk_size
        working_file = prefix + '_' + str(file_index) + '.txt'
        # print(f'Opening file #{k}: {working_file}')

        # get lines of interest
        # if in the same file
        if r1_file_number == r2_file_number:
            row_start = r1_t
            row_end = r2_t + 1
        else: # (r1_file_number > r2_file_number)
            if k == r1_file_number:
                row_start = r1_t
                row_end = chunk_size
            elif k == r2_file_number:
                row_start = 0
                row_end = r2_t + 1
            else:
                row_start = 0
                row_end = chunk_size

        with open(working_file, 'r') as f:
            # no need to read in all lines in the file
            # lines = f.readlines()
            # selected_lines = lines[row_start:row_end]
            
            # read one line at a time
            for i, line in enumerate(f):
                # print(row_start, row_end, i, line)
                if i >= row_start and i < row_end:
                    
            # for line in selected_lines:
                    row = list(line)
                    test_range = row[c1:c2+1]   # to get the correct slide, right index + 1
                    # print(c1, c2+1, test_range)
                    if K_OTHER_TILE in test_range:
                        # print(f'Invalid: found {K_OTHER_TILE} in file {working_file} test range: {test_range}')                    
                        valid = False
                        break
                    
        if valid == False:
            break

    candidate_end = datetime.now()
    duration = candidate_end - candidate_start
    duration_minutes = duration.total_seconds()/60
    print(f'Finished {os.getpid()}::candidate: {candidate}: valid: {valid}::: End time: {candidate_end.isoformat(timespec='seconds')} Duration {duration_minutes}')

    return valid, candidate 

# get nodes with row coordinate = coord
# coordinate type = row or column
# assumes that the coordinates are sorted in the correct order
def get_nodes_at_coordinate(coord: int, remaining_nodes: list, coordinate_type: str = K_ROW_COORDINATE) -> tuple[list, list]:
    selected_nodes = []
    coord_key = 1
    if coordinate_type == K_COLUMN_COORDINATE:
        coord_key = 0

    i = 0
    while len(remaining_nodes) > 0:
        item_coord = remaining_nodes[i][coord_key]
        if item_coord == coord:
            selected_nodes.append(remaining_nodes[i])
            remaining_nodes.pop(i)
        else:
            i += 1

        if item_coord > coord:
            break        

    return selected_nodes, remaining_nodes

# sort the nodes in row coordinate order (default)
# or column coordinate order
# sort_by 'row' or 'column'
def sort_nodes(all_nodes: list, sort_by: str = K_ROW_COORDINATE) -> list:
    sort_key = 1
    if sort_by == K_COLUMN_COORDINATE:
        sort_key = 0

    all_nodes = sorted(all_nodes, key=lambda x: x[sort_key])
    return all_nodes

# run part 1 solution
def part1_biggest_area(all_nodes: list):
    # Part 1 solution
    # use itertools to generate a combination of 2 nodes
    biggest_area = 0
    for node1, node2 in itertools.combinations(all_nodes, 2):
        area = calculate_tiles_in_area(node1=node1, node2=node2)
        if area > biggest_area:
            biggest_area = area

    print(f'Part 1: Biggest area: {biggest_area}')
    return biggest_area

def part2_build_grid(all_nodes: str, chunk_size: int = 5000):
    # Part 2 solution - preparation
    # the grid is too large to manipulate in memory
    # written out to file, it is 9 GB! 
    # chunk the data and write to file
    
    # get the size of the grid
    cols, rows = grid_size(all_nodes=all_nodes)
    print(f'Grid size: columns: {cols} rows: {rows}')

    # populate the grid with tiles
    print(f'Starting to place red green tiles in grid with columns: {cols} rows: {rows}. Chunk size {chunk_size}')
    place_grid_red_green_tiles(rows, cols, all_nodes, chunk_size)

    # fill in green tiles vertically
    print(f'Starting to place green tiles in columns between red green tiles...')
    vertical_fill_green_tiles(cols, all_nodes, chunk_size)

    # the pattern has been made now fill additional horizontal green tiles
    print(f'Final pass: Starting to place green tiles in between red/green edge tiles in rows...')
    horizontal_fill_green_tiles(rows, chunk_size)

    # now the grid is mapped and saved in files. 
    return

def part2_biggest_area(all_nodes: list, biggest_area: int, chunk_size: int = 5000):
    module_start = datetime.now()
    print(f'{module_start.isoformat(timespec='seconds')}::Starting find the biggest red/green tiles only area...')
    candidates = big_area_candidates(biggest_area, all_nodes)
    # print(candidates)

    successful_candidate = None
    for i, candidate in enumerate(candidates):
        valid, successful_candidate = is_red_green_candidate(candidate, chunk_size)
        if valid:
            break

    return valid, successful_candidate

# this is still slow!
# ~ 650 candidates per hour (without compressing the grid)
def part2_biggest_area_multiprocess(all_nodes: list, biggest_area: int, chunk_size: int = 5000, processor_count: int = 4):
    module_start = datetime.now()
    print(f'{module_start.isoformat(timespec='seconds')}::Starting find the biggest red/green tiles only area (multiprocessing)...')
    candidates = big_area_candidates(biggest_area, all_nodes, 0)
    # print(candidates)

    # create a new function that takes the default value of chunk_size
    is_red_green_candidate_chunk = partial(is_red_green_candidate, chunk_size=chunk_size)

    successful_candidate = []
    processed_count = 0
    with multiprocessing.Pool(processes=processor_count) as pool:
        for valid, candidate in pool.imap_unordered(is_red_green_candidate_chunk, candidates):
            processed_count += 1
            print(f'Processed candidate #{processed_count}')
            if valid:
                successful_candidate = candidate
                break
        # valid, candidate = pool.map(is_red_green_candidate_chunk, candidates)

    return valid, successful_candidate

# reduce the problem space remove rows and columns that have no red tiles in them
# translate the coordinates accordingly
# find the biggest area candidate in the reduced space 
# calculate the biggest area from the candidate's original coordinates
def simplify_grid_rows(all_nodes: list):
    # sort nodes by row
    ordered_nodes = list(all_nodes)
    ordered_nodes = sort_nodes(ordered_nodes, K_ROW_COORDINATE)

    # keep track of original coordinates by same order sort
    all_nodes = sort_nodes(all_nodes, K_ROW_COORDINATE)

    print(ordered_nodes)

    i = 0
    next_available_row = 0

    while i < len(ordered_nodes):
        current_row = ordered_nodes[i][1]
        empty_rows = current_row - next_available_row

        print(i, ordered_nodes[i], empty_rows, current_row, next_available_row)
        if empty_rows > 0:
            # move rows up
            ordered_nodes = [(node[0], node[1] - empty_rows) if node[1] > next_available_row else node for node in ordered_nodes]
            next_available_row += 1
            print(ordered_nodes)
                
        i += 1

    print(f'Original: {all_nodes}')
    print(f'Row translation: {ordered_nodes}')

    return ordered_nodes, all_nodes

# after removing empty rows, remove empty columns.
# keep with the original list and row translated list
# to preserve mapping to original grid
def simplify_grid_columns(all_nodes: list, row_translated_nodes: list):
    # sort nodes by columns
    ordered_nodes = list(row_translated_nodes)
    ordered_nodes = sort_nodes(ordered_nodes, K_COLUMN_COORDINATE)

    # keep track of original coordinates by same order sort
    all_nodes = sort_nodes(all_nodes, K_COLUMN_COORDINATE)

    print(ordered_nodes)

    i = 0
    next_available_col = 0

    while i < len(ordered_nodes):
        current_col = ordered_nodes[i][0]
        empty_cols = current_col - next_available_col

        print(i, ordered_nodes[i], empty_cols, current_col, next_available_col)
        if empty_cols > 0:
            # move rows up
            ordered_nodes = [(node[0] - empty_cols, node[1]) if node[0] > next_available_col else node for node in ordered_nodes]
            next_available_col += 1
            print(ordered_nodes)
                
        i += 1

    print(f'Original: {all_nodes}')
    print(f'Column translation: {ordered_nodes}')

    return ordered_nodes, all_nodes

def main():
    fname = r'Day_09\inputs.txt'
    # fname = r'Day_09\sample_inputs.txt'

    all_nodes = load_data_set(data_file=fname)
    # print(all_nodes)    

    part2_rebuild_grid = True
    
    biggest_area = part1_biggest_area(all_nodes)
    
    # Part 2 solution
    # the grid is too large to manipulate in memory
    # written out to file, it is 9 GB! 
    # chunk the data and write to file
    chunk_size = 5000
    
    # even chunking leaves the grid too slow to process
    # remove empty rows, and compress the grid horizontally
    translated_nodes, all_nodes = simplify_grid_rows(all_nodes)

    # additionally compressing the grid vertically causes distortion and does not give the right answer.
    # translated_nodes, all_nodes = simplify_grid_columns(all_nodes, translated_nodes)

    original_nodes = list(all_nodes)
    all_nodes = list(translated_nodes)

    if part2_rebuild_grid:
        part2_build_grid(all_nodes, chunk_size)

    # now the grid is mapped and saved in files. 
    # test each big area to see it is a valid "biggest" area
    
    # valid, candidate = part2_biggest_area(all_nodes, biggest_area, chunk_size)
    processor_count = 4
    valid, candidate = part2_biggest_area_multiprocess(all_nodes, biggest_area, chunk_size=chunk_size, processor_count=processor_count)

    if valid:
        # find idx in translated grid
        node1 = candidate[0]
        node2 = candidate[1]

        idx1 = translated_nodes.index(node1)
        idx2 = translated_nodes.index(node2)

        node1prime = original_nodes[idx1]
        node2prime = original_nodes[idx2]

        biggest_area = calculate_tiles_in_area(node1prime, node2prime)
        print(f'Part 2: Biggest area: {biggest_area} Original nodes: {node1prime} and {node2prime}')
        # 1562459680 (94553, 50158) (5939, 67789)
    else:
        print(f'Part 2: Biggest area candidate not found.')

if __name__ == '__main__':
    main()
