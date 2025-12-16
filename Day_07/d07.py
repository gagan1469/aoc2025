K_MULTIPLY = '*'
K_ADD = '+'

# read the inputs
def part1_load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    # convert to matrix
    m = [''] * len(lines)
    for i, line in enumerate(lines):
        items = line.split()
        n = [''] * len(items)
        for j, c in enumerate(items):
            n[j] = c
        m[i] = n

    size = [len(m), len(n)]    
    # print(m)
    return m, size

# read the inputs
# in part 2, the left/right alignment of numbers within each problem CANNOT be ignored.
def part2_load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    # convert to matrix
    m = [''] * len(lines)
    for i, line in enumerate(lines):
        m[i] = list(line)

    # print(m)
    return m

def part1_grand_total(m: list) -> None:
    grand_total = 0
    row = 0
    for c in range(0, len(m[row])):
        operation = m[len(m)-1][c]
        # print(f'Operation: {operation}')

        nums = []
        for r in range(0, len(m)-1):
            num = int(m[r][c])
            nums.append(num)
        
        result = compute_problem(numbers=nums, operation=operation)
        # print(result)
        grand_total += result
        row += 1
    
    return grand_total

def part2_cephalopod_math(m):
    grand_total = 0
    
    # bottom row is the operations
    bottom_row = m[len(m) - 1]
    bottom_row = ''.join(bottom_row)
    ops = bottom_row.split()
    
    total_problems = len(ops)
    problem_rows = len(m) - 1
    pointer = 0
    max_pointer = len(bottom_row)
    problem_count = 0
    quantities = []
    qty = ''

    while problem_count < total_problems:
        op = ops[problem_count]

        while pointer < max_pointer:        
            # get the whole column
            for r in range(0, problem_rows):
                qty += m[r][pointer]

            # if it's an empty row, new problem is starting
            if len(qty.strip()) == 0:
                pointer += 1
                break

            num = int(qty.strip())
            quantities.append(num)
            qty = ''
            pointer += 1

        print(quantities, op)
        computed_value = compute_problem(numbers=quantities, operation=op)
        print(computed_value)
        grand_total += computed_value

        quantities = []
        problem_count += 1
    
    return grand_total

def compute_problem(numbers: list, operation: str) -> int:
    if operation == K_MULTIPLY:
        result = 1
    else:
        result = 0

    for num in numbers:
        if operation == K_MULTIPLY:
            result *= num
        else:
            result += num

    return result

def main():
    fname = 'Day_07\inputs.txt'
    fname = 'Day_07\sample_inputs.txt'

    m, size = part1_load_data_set(data_file=fname)
    print(size)

    grand_total = part1_grand_total(m)
    print(f'Part 1 result: {grand_total}')

    m = part2_load_data_set(data_file=fname)
    grand_total = part2_cephalopod_math(m)
    print(f'Part 2 result: {grand_total}')

if __name__ == '__main__':
    main()
