# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    return lines

# original approach to handle 2 batteries (Part A solution)
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

# the high number bubbles up. Smaller numbers drops off the left until target length is achieved.
# the solution came to me on the evening walk after puzzling and agonizing over it for 2 days and trying to collapse the list
# the analogy came from bubble sorting
def bubble_up(input: list, target_size: int) -> list:
    values = [int(s) for s in input]

    count = len(values)
    pointer = 0
    iter = 0
    # print(iter, pointer, count, values)

    while count > target_size:
        if values[pointer + 1] > values[pointer]:
            values.pop(pointer)
            count = len(values)
            pointer = pointer - 1 if pointer > 0 else 0
        else:
            pointer += 1 
        
        # print(iter, pointer, count, values)

        # rinse and repeat, if reached the end of list
        # and the list is still not at target size
        if pointer == count - 1:
            # print('reached the end. repeat one more time.')
            # print(iter, pointer, count, values)
            iter += 1
            pointer = 0

        # if after 3 iterations, the solution has not coverged, there is repition of digits
        # exit the loop
        if iter == 3:
            # print('Stuck without change')
            # print(iter, pointer, count, values)
            break

    # crude - if after 4 iterations, the solution did not converge, review the number and truncate the last digits
    if count > target_size:
        # print(iter, pointer, count, values)
        # print(f'Values: {values}')
        # print(f'Values right sized: {values[:target_size]}')
        values = values[:target_size]

    return values

def main():
    fname = 'Day_03\inputs.txt'
    # fname = 'Day_03\sample_inputs.txt'

    lines = load_data_set(data_file=fname)
    # print(lines)

    # Part A approach
    total_joltage = 0
    for line in lines:
        joltage = get_battery_joltage(line)
        print(joltage)
        total_joltage += joltage

    print(f'Total joltage: {total_joltage}')
    
    # Part B approach
    target_size = 12
    total_joltage = 0

    for line in lines:
        result = bubble_up(input=line, target_size=target_size)
        values = [str(i) for i in result]
        joltage = int(''.join(values))
        total_joltage += joltage
        print(joltage)

    print(f'Total joltage: {total_joltage}')

if __name__ == '__main__':
    main()
