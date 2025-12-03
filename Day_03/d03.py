# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    return lines

def get_battery_joltage(battery_bank: str) -> int:
    joltage = 0
    # get the maximum value and its location
    values = list(battery_bank)
    max_value = max(values)
    max_value_index = values.index(max_value)
    # print(max_value, max_value_index)

    # if the max value is the last index, find the largest number before it
    # otherwise pick the biggest number after it
    if max_value_index == len(values) -1:
        next_value = max(values[:max_value_index])
        joltage = int(next_value + max_value)
    else:
        next_value = max(values[max_value_index+1:])
        joltage = int(max_value + next_value)        
    
    return joltage

def get_12_battery_joltage(battery_bank: str) -> int:
    joltage = 0
    # get the maximum value and its location
    values = list(battery_bank)
    max_value = max(values)
    max_value_index = values.index(max_value)
    # print(max_value, max_value_index)

    # if the max value is the last index, find the largest number before it
    # otherwise pick the biggest number after it
    if max_value_index == len(values) -1:
        next_value = max(values[:max_value_index])
        joltage = int(next_value + max_value)
    else:
        next_value = max(values[max_value_index+1:])
        joltage = int(max_value + next_value)        
    
    return joltage

def main():
    fname = 'Day_03\inputs.txt'
    # fname = 'Day_03\sample_inputs.txt'

    lines = load_data_set(data_file=fname)
    # print(lines)

    total_joltage = 0
    for line in lines:
        joltage = get_battery_joltage(line)
        print(joltage)
        total_joltage += joltage

    print(f'Total joltage: {total_joltage}')
if __name__ == '__main__':
    main()