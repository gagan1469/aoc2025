# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    return lines

def main():
    fname = 'Day_0x\inputs.txt'
    fname = 'Day_0x\sample_inputs.txt'

    lines = load_data_set(data_file=fname)
    print(lines)

if __name__ == '__main__':
    main()