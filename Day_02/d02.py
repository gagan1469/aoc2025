import re

# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    return lines

def find_invalid_product_codes(code_range: str) -> tuple[list, int]:
    id_set = code_range.split(sep='-')
    first_id = int(id_set[0])
    last_id = int(id_set[1])

    # print(first_id, last_id)

    invalid_codes = []
    invalid_code_count = 0
    for id in range(first_id, last_id+1):
        # id is even number of digits
        # print(id)
        code = str(id)
        if len(code) % 2 == 0:
            mid = len(code) // 2
            # print(mid, code[:mid], code[mid:])
            if code[:mid] == code[mid:]:
                invalid_code_count += 1
                invalid_codes.append(id)

    return invalid_codes, invalid_code_count

def find_invalid_product_codes_2(code_range: str) -> tuple[list, int]:
    id_set = code_range.split(sep='-')
    first_id = int(id_set[0])
    last_id = int(id_set[1])

    # print(first_id, last_id)

    invalid_codes = []
    invalid_code_count = 0
    for id in range(first_id, last_id+1):
        code = str(id)
        mid = len(code) // 2
        for i in range(1, mid+1):
            pattern = code[:i]
            matches = re.findall(pattern=pattern, string=code)
            concatenated_matches = ''.join(matches)
            if len(concatenated_matches) == len(code):
                # invalid id found
                # print(concatenated_matches, code)
                # 222222 can be added multiple times. avoid it.
                if id not in invalid_codes:
                    invalid_code_count += 1
                    invalid_codes.append(id)

    return invalid_codes, invalid_code_count

def main():
    fname = 'Day_02\inputs.txt'
    # fname = 'Day_02\sample_inputs.txt'

    lines = load_data_set(data_file=fname, delimiter=',')
    # print(lines)

    invalid_total = 0
    for line in lines:
        invalid_codes, count = find_invalid_product_codes_2(code_range=line)
        print(count, invalid_codes)

        if count > 0:
            for code in invalid_codes:
                invalid_total += code
            #invalid_total = [invalid_total + x for x in invalid_codes][0]

    print(f'Sum of invalid codes: {invalid_total}')


if __name__ == '__main__':
    main()