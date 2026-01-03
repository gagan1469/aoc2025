# part 2 solution using similar logic as part 1 worked for the sample data but the
# but had serious performance issue in testing 10^n combinations
# the solution lies in handling it as a linear programming optimization problem
# used PuLP for it.

from datetime import datetime
from d10_lp_fx import run_lp

K_LOW_INDICATOR = '.'
K_HIGH_INDICATOR = '#'

# read the inputs 
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    data = []
    for i, line in enumerate(lines):
        machine_data = line.split()
        # ignore the indicator light for part 2
        # indicator_lights = machine_data[0]
        # indicator_lights = indicator_lights.replace(K_HIGH_INDICATOR, str(1))
        # indicator_lights = indicator_lights.replace(K_LOW_INDICATOR, str(0))
        # indicator_lights = indicator_lights.replace('[', '')
        # indicator_lights = indicator_lights.replace(']', '')
        # num_indicator_lights = len(indicator_lights)
        
        joltage = machine_data[-1]
        joltage = joltage.replace('{', '')
        joltage = joltage.replace('}', '')
        joltage = joltage.split(',')
        joltage = [int(x) for x in joltage]
        
        wiring = machine_data[1:-1]
        for i, item in enumerate(wiring):
            wiring[i] = wiring[i].replace('(', '')
            wiring[i] = wiring[i].replace(')', '')
            wiring[i] = [int(s) for s in wiring[i].split(',')]
        # print(indicator_lights, wiring, joltage)
        
        machine = [wiring, joltage]
        data.append(machine)

    return data

def part2_solution(all_machine_data: list) -> None:
    result = 0
    for machine_data in all_machine_data:
        buttons = machine_data[0]
        target = machine_data[1]
        
        # print(target, buttons)
        value = run_lp(target, buttons)
        result += value

    print(f'Configure joltage levels of all machines: {result}')


def main():
    fname = r'Day_10\inputs.txt'
    # fname = r'Day_10\sample_inputs.txt'

    all_machine_data = load_data_set(data_file=fname)
    part2_solution(all_machine_data)

if __name__ == '__main__':
    main()
