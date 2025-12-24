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

def propagate_timelines(line: list, previous_line: list, previous_line_beam_indices: list) -> list:

    # if the corresponding position in current line is a beam, set its timeline value from the previous line
    for idx in previous_line_beam_indices:
        if line[idx]  == K_BEAM:
            previous_timeline_count = previous_line[idx]
            line[idx] = previous_line[idx]

    # now add the split timelines
    for idx in previous_line_beam_indices:
        if line[idx] == K_SPLITTER:
            previous_timeline_count = previous_line[idx]

            if isinstance(line[idx-1], int):
                line[idx-1] = line[idx-1] + previous_timeline_count
            else:
                line[idx-1] = previous_timeline_count

            if isinstance(line[idx+1], int):
                line[idx+1] = line[idx+1] + previous_timeline_count
            else:
                line[idx+1] = previous_timeline_count            

    #print(f'Output line: {line}')
    return line

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
    pos = 1
    total_splits = 0
    while pos < len(m):
        line = m[pos]
        splitter_indices = process_line_splitters(line=line)
        split_count, updated_line = advance_beams(previous_line_beams=previous_line_beams, line_splitters=splitter_indices, line=line)
        total_splits += split_count
        # print(f'Line {pos}, {updated_line}')
        previous_line_beams = process_line_beams(line=updated_line)
        pos += 1

    
    print(f'Part 1: The answer is {total_splits}')
    # print(f'After all splits:')
    # for line in m:
    #     print(line)

    # Part 2 - count the timelines
    # start with all the splits already done
    pos = 0
    previous_line = m[pos]
    previous_beam_indices = process_line_beams(previous_line)
    for idx in previous_beam_indices:
        previous_line[idx] = 1

    while pos < len(m)-1:
        pos += 1
        line = m[pos]
        beam_indices = process_line_beams(line)
        line = propagate_timelines(line, previous_line, previous_beam_indices)
        m[pos] = line
        # print(line)        
        
        previous_line = line
        previous_beam_indices = beam_indices

    sum = 0
    for i in line:
        if isinstance(i, int):
            sum += i

    print(f'Part 2: The total number of timelines is {sum}')

if __name__ == '__main__':
    main()
