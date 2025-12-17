K_ENTRY = 'S'
K_SPLITTER = '^'
K_EMPTY = '.'
K_BEAM = '|'

# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    # convert to matrix
    m = [''] * len(lines)
    for i, line in enumerate(lines):
        m[i] = list(line)

    return m

def get_all_indices(line: list, token: str) -> list:
    indices = []
    pos = 0
    while True:
        try:
            idx = line.index(token, pos)
        except ValueError as e:
            break

        indices.append(idx)
        pos = idx + 1

    return indices

def process_line_beams(line: list) -> list:
    beam_indices = get_all_indices(line=line, token=K_BEAM)
    return beam_indices

def process_line_splitters(line: list) -> list:
    splitter_indices = get_all_indices(line=line, token=K_SPLITTER)
    return splitter_indices

def process_first_line(first_line: list) -> list:
    start_index = get_all_indices(line=first_line, token=K_ENTRY)
    return start_index

def advance_beams(previous_line_beams: list, line_splitters: list, line: list) -> tuple[int, list]:
    split_count = 0
    for beam in previous_line_beams:
        if beam in line_splitters:
            split_count += 1
            try:    
                line[beam-1] = K_BEAM
            except IndexError as e:
                # beam falls off the edge
                continue
            try:
                line[beam+1] = K_BEAM
            except IndexError as e:
                # beam falls off the edge
                continue
        else:
            line[beam] = K_BEAM
    
    return split_count, line

def main():
    fname = r'Day_07\inputs.txt'
    # fname = r'Day_07\sample_inputs.txt'

    m = load_data_set(data_file=fname)
    
    start_index = process_first_line(m[0])
    print(start_index)

    # initialize beam
    updated_line = advance_beams(previous_line_beams=start_index, line_splitters=[], line=m[0])
    print(updated_line)
    
    previous_line_beams = start_index
    # previous_line = updated_line
    pos = 1
    total_splits = 0
    while pos < len(m):
        line = m[pos]
        splitter_indices = process_line_splitters(line=line)
        split_count, updated_line = advance_beams(previous_line_beams=previous_line_beams, line_splitters=splitter_indices, line=line)
        total_splits += split_count
        print(f'Line {pos}, {updated_line}')
        previous_line_beams = process_line_beams(line=updated_line)
        pos += 1

    
    print(f'Part 1: The answer is {total_splits}')

if __name__ == '__main__':
    main()
