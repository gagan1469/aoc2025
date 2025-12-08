K_ROLL = '@'
# read the inputs
def load_data_set(data_file: str, delimiter: str = '\n') -> list:
    with open(data_file, 'r') as f:
        lines = f.read().split(delimiter)

    return lines

def get_fresh_ingredient_id_ranges(lines: list) -> list:
    K_INGREDIENT_DELIMITER = '-'
    fresh_ingredient_ranges = []
    for line in lines:
        # print(line)
        ingredient_range = line.strip().split(K_INGREDIENT_DELIMITER)
        start = int(ingredient_range[0])
        end = int(ingredient_range[1])
        fresh_ingredient_ranges.append((start, end))
    
    return fresh_ingredient_ranges

def get_blank_line_number(lines: list) -> int:
    for i, line in enumerate(lines):
        data = line.strip()
        if len(data) == 0:
            break

    return i

def count_fresh(all_ingredients: list, fresh_ingredient_ranges: list) -> int:
    fresh_count = 0
    for id in all_ingredients:
        for fresh_ingredient_range in fresh_ingredient_ranges:
            item = int(id)
            if item >= fresh_ingredient_range[0] and item <= fresh_ingredient_range[1]:
                fresh_count += 1
                break

    return fresh_count

def merge_ranges(fresh_ingredient_ranges: list) -> int:
    merged_list = []
    total_items = len(fresh_ingredient_ranges)
    for i, item in enumerate(fresh_ingredient_ranges):
        print(f'Processing: {i} of {total_items} {item}')
        for i in range(item[0], item[1] + 1):
            if i not in merged_list:
                merged_list.append(i)

    return len(merged_list)

def main():
    fname = 'Day_05\inputs.txt'
    # fname = 'Day_05\sample_inputs.txt'

    lines = load_data_set(data_file=fname)
    blank_line_num = get_blank_line_number(lines=lines)
    fresh_ingredient_ranges = get_fresh_ingredient_id_ranges(lines=lines[:blank_line_num])
    # print(fresh_ingredient_ids)
    ingredient_ids = lines[blank_line_num + 1:]

    count = count_fresh(all_ingredients=ingredient_ids, fresh_ingredient_ranges=fresh_ingredient_ranges)
    print(count)

    # Part 2 count of fresh ingredient ids
    count = merge_ranges(fresh_ingredient_ranges=fresh_ingredient_ranges)
    print(count)
if __name__ == '__main__':
    main()
