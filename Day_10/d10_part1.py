import itertools
from datetime import datetime

K_LOW_INDICATOR = '.'
K_HIGH_INDICATOR = '#'
K_PAD_CHAR = '0'

# read the inputs 
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    data = []
    for i, line in enumerate(lines):
        machine_data = line.split()
        indicator_lights = machine_data[0]
        indicator_lights = indicator_lights.replace(K_HIGH_INDICATOR, str(1))
        indicator_lights = indicator_lights.replace(K_LOW_INDICATOR, str(0))
        indicator_lights = indicator_lights.replace('[', '')
        indicator_lights = indicator_lights.replace(']', '')
        num_indicator_lights = len(indicator_lights)
        
        # indicator light to int
        # indicator_lights = int(indicator_lights, 2)

        joltage = machine_data[-1]
        joltage = joltage.replace('{', '')
        joltage = joltage.replace('}', '')
        joltage = joltage.split(',')
        joltage = [int(x) for x in joltage]
        
        wiring = machine_data[1:-1]
        for i, item in enumerate(wiring):
            wiring[i] = wiring[i].replace('(', '')
            wiring[i] = wiring[i].replace(')', '')
            wiring[i] = convert_wiring_schematic(wiring[i], num_indicator_lights)
        # print(indicator_lights, wiring, joltage)
        
        machine = [indicator_lights, wiring, joltage]
        data.append(machine)

    return data

def convert_wiring_schematic(wiring_info: str, num_lights: int) -> str:
    value = ['0'] * num_lights
    
    parts = wiring_info.split(',')
    for part in parts:
        i = int(part)
        value[i] = '1'
    
    value = ''.join(value)
    # convert the binary string to int
    value = int(value, 2)
    return value

# for part 1 solution
# Variable padding
# width = 8
# pad_char = '0'
# a = int('0101', 2)
# print(f'{a:{pad_char}{width}b}')
def process_machine_activation_combination(target: str, buttons: list) -> bool:
    triggered = False
    value = 0
    width = len(target)

    for button in buttons:
        value = value ^ button
        # print(f'Button: {button:{K_PAD_CHAR}{width}b} Result: {value:{K_PAD_CHAR}{width}b}')

    result = f'{value:{K_PAD_CHAR}{width}b}'
    if result == target:
        triggered = True

    return triggered

# for part 1 solution
def generate_activation_combinations_and_test(target: str, wiring_schematic: list, machine_number: int = 1, maximum_repeats: int = 12) -> int:
    # generate permutations with repeats
    # start with 1 to maximum repeats
    valid = False
    result = 0
    for repeat in range(1, maximum_repeats + 1):
        for p in itertools.product(wiring_schematic, repeat=repeat):
            # print(f'Testing: {p}')
            valid = process_machine_activation_combination(target, p)
            if valid == True:
                result = len(p)
                break
        
        if valid:
            break

    if valid == True:
        print(f'Machine number {machine_number} found solution: {p}. Number of presses: {result}')
    else:
        print(f'Machine number {machine_number} solution not found. Increase maximum repeats from {maximum_repeats}.')
    return result

def part1_solution(all_machine_data: list) -> None:
    activation = 0
    for i, machine_data in enumerate(all_machine_data):
        target = machine_data[0]
        wiring_schematic = machine_data[1]
        result = generate_activation_combinations_and_test(target, wiring_schematic, i, maximum_repeats=8)
        activation += result

    print(f'Activation of all machines: {activation}')

def main():
    fname = r'Day_10\inputs.txt'
    fname = r'Day_10\sample_inputs.txt'

    all_machine_data = load_data_set(data_file=fname)
    part1_solution(all_machine_data)

    # part solution using similar logic as part 1 worked for the sample data but the
    # but had serious performance issue in testing 10^n combinations
    # the solution lies in handling it as a linear programming optimization problem
    # used PuLP for it.

if __name__ == '__main__':
    main()
