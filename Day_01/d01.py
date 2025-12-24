# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    return lines

def calculate_position(current_pos: int, instruction: str) -> int:
    direction = instruction[0]
    magnitude = int(instruction[1:])
    sign = 1
    if direction == 'L':
        sign = -1

    # a magnitude of 100 is a complete rotation
    # get the remainder of x % 100
    magnitude = magnitude % 100

    increment = sign * magnitude
    new_position = current_pos + increment 

    if new_position < 0:
        new_position = 100 + new_position
    elif new_position >= 100:
        new_position =  new_position - 100

    return new_position

def calculate_position_method_0x434C49434B(current_pos: int, instruction: str) -> int:
    pass_zero = 0
    direction = instruction[0]
    magnitude = int(instruction[1:])
    sign = 1
    if direction == 'L':
        sign = -1

    # a magnitude of 100 is a complete rotation
    # get number of full rotations
    pass_zero = magnitude // 100
    # get the remainder of x % 100
    magnitude = magnitude % 100

    increment = sign * magnitude
    new_position = current_pos + increment 

    if new_position < 0:
        new_position = 100 + new_position
        if current_pos != 0:
            pass_zero += 1
    elif new_position >= 100:
        new_position =  new_position - 100
        if new_position !=0:
            pass_zero += 1

    return new_position, pass_zero

def main():
    fname = 'Day_01\inputs.txt'
    # fname = 'Day_01\sample_inputs.txt'

    lines = load_data_set(data_file=fname)
    # print(lines)

    current_position = 50
    password_count = 0
    for line in lines:
        new_position = calculate_position(current_pos=current_position, instruction=line)
        if new_position == 0:
            password_count += 1
        current_position = new_position

    print(f'The password is: {password_count}')

    # method_0x434C49434B password
    current_position = 50
    password_count = 0
    for line in lines:
        new_position, pass_zero = calculate_position_method_0x434C49434B(current_pos=current_position, instruction=line)
        # print(new_position, pass_zero)
        password_count += pass_zero
        if new_position == 0:
            password_count += 1
        current_position = new_position

    print(f'The password is: {password_count}')

if __name__ == '__main__':
    main()