K_ROLL = '@'
# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
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
    print(m)
    return m, size

def main():
    K_MULTIPLY = '*'
    K_ADD = '+'

    fname = 'Day_06\inputs.txt'
    # fname = 'Day_06\sample_inputs.txt'

    m, size = load_data_set(data_file=fname)
    print(size)

    grand_total = 0
    row = 0
    for c in range(0, len(m[row])):
        operation = m[len(m)-1][c]
        # print(f'Operation: {operation}')

        if operation == K_MULTIPLY:
            result = 1
        else:
            result = 0

        for r in range(0, len(m)-1):
            # print(m[r])
            # print(r, c)
            num = int(m[r][c])
            if operation == K_MULTIPLY:
                result *= num
            else:
                result += num
            # print(f'{num}, {result}')

        # print(result)
        grand_total += result
        row += 1
    
    print(grand_total)


if __name__ == '__main__':
    main()
