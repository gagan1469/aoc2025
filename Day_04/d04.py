K_ROLL = '@'
# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    # convert to matrix
    m = [''] * len(lines)
    for i, line in enumerate(lines):
        n = [''] * len(line)
        for j, c in enumerate(line):
            n[j] = c
        m[i] = n

    size = [len(m), len(n)]    
    # print(m)
    return m, size

def count_rolls(grid: list, x, y, threshold: int = 4) -> bool:
    x_min = x - 1 if x > 0 else 0
    x_max = x + 1 if x < len(grid[0]) - 1 else len(grid[0]) - 1

    y_min = y - 1 if y > 0 else 0
    y_max = y + 1 if y < len(grid[0]) - 1 else len(grid[0]) - 1

    # print(x, y, x_min, x_max, y_min, y_max)

    count = 0
    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            if i == x and j == y:
                pass
            else:
                if grid[i][j] == K_ROLL:
                    count += 1
                # print(i, j, grid[i][j], count)

            if count >= threshold:
                # print(x, y, count, 'inaccessible')
                break
    
    accessible = True if count < threshold else False
    # print(x, y, count, accessible)
    return accessible

def main():
    fname = 'Day_04\inputs.txt'
    # fname = 'Day_04\sample_inputs.txt'

    grid, size = load_data_set(data_file=fname)
    print(size[0], size[1])
    # print(grid)

    total_removed_count = 0
    iter = 0
    # for part 1 - only do 1 iterations
    part_1_solution = False

    while True:
        accessible_locations = []
        accessible_count = 0

        # make a pass at removing the rolls of paper
        for r in range(0, size[0]):
            for c in range(0, size[1]):
                v = grid[r][c]
                # print(r, c, v)
                if v == K_ROLL:
                    accessible = count_rolls(grid=grid, x=r, y=c)
                    if accessible == True:
                        accessible_count = accessible_count + 1 
                        accessible_locations.append((r, c))

        total_removed_count += accessible_count
        print(f'Iteration: {iter} Rolls removed: {accessible_count} Total removed: {total_removed_count}')
        
        # mark the removed locations
        for location in accessible_locations:
            grid[location[0]][location[1]] = 'x'

        if part_1_solution == False and accessible_count > 0:
            iter += 1
        else:
            break

    with open(r'Day_04/output.txt', 'w') as f:
        for line in grid:
            f.write(''.join(line))
            f.write('\n')

    # print(grid)

if __name__ == '__main__':
    main()
