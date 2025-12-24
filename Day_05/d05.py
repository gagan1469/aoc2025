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

def brute_force_merge_ranges(fresh_ingredient_ranges: list) -> int:
    merged_list = []
    total_items = len(fresh_ingredient_ranges)
    for i, item in enumerate(fresh_ingredient_ranges):
        print(f'Processing: {i} of {total_items} {item}')
        for i in range(item[0], item[1] + 1):
            if i not in merged_list:
                merged_list.append(i)

    return len(merged_list)

def range_overlap_check(range1: tuple[int, int], range2: tuple[int, int]) -> bool:
    overlap = True

    # no overlap conditions
    # range1[0] > range2[1] or range1[1] < range2[0]
    if range1[0] > range2[1] or range1[1] <  range2[0]:
        overlap = False
    
    return overlap    

def merge_ranges(range1: tuple[int, int], range2: tuple[int, int]) -> tuple[int, int]:
    # the ranges are overlapping. Merge them into a single range
    # take the minimum of lower limit and maximum of upper limit
    lower_value = min(range1[0], range2[0])
    upper_value = max(range1[1], range2[1])
    return (lower_value, upper_value)

def get_nonoverlapping_ranges(fresh_ingredient_ranges: list) -> list:
    merged_ranges = list(fresh_ingredient_ranges)

    # it is possible that in the first iteration no overlaps are detected because only neighbors are compared.
    min_iterations = len(merged_ranges)
    iteration_overlap_count = 0
    iteration_count = 0
    current_index = 0
    compare_index = 0

    while current_index < len(merged_ranges):
        overlap = False
        # compare_index = 0
        if current_index != compare_index:
            overlap = range_overlap_check(merged_ranges[current_index], merged_ranges[compare_index])
            # print(f'Processing: {iteration_count} {current_index}: {merged_ranges[current_index]} and {compare_index}: {merged_ranges[compare_index]}:: overlap {overlap} overlap count {iteration_overlap_count}')

        if overlap:
            iteration_overlap_count += 1
            new_range = merge_ranges(merged_ranges[current_index], merged_ranges[compare_index])
            print(f'Processing: New range: {new_range}')
            print(f'Processing: {iteration_count} {current_index}: {merged_ranges[current_index]} and {compare_index}: {merged_ranges[compare_index]}:: overlap {overlap} overlap count {iteration_overlap_count}')
            range1 = merged_ranges[current_index]
            range2 = merged_ranges[compare_index]
            # pop the current range
            merged_ranges.remove(range1)
            merged_ranges.remove(range2)
            merged_ranges.append(new_range)
            # print(f'Updated ranges: {merged_ranges}')
            # current index needs to be reset. at minimum move it one back
            current_index = current_index - 1 if current_index > 0 else 0
            # but if compare index is less than current index, move one more back
            if compare_index <=  current_index:
                current_index = current_index - 1 if current_index > 0 else 0
        
        # advance compare pointer or reset to beginning
        compare_index = compare_index + 1 if compare_index < len(merged_ranges) - 1 else 0
    
        # advance the current index if compare index has looped around
        if compare_index == 0:
            current_index += 1
            iteration_count += 1
            iteration_overlap_count = 0
            print(f'Iteration count {iteration_count}')
                            
    return merged_ranges

def count_fresh_ingredient_ids(fresh_ingredient_ranges: list) -> int:
    total_count = 0
    for item in fresh_ingredient_ranges:
        ingredient_count = item[1] - item[0] + 1
        total_count += ingredient_count

    return total_count

def main():
    fname = r'Day_05\inputs.txt'
    # fname = r'Day_05\sample_inputs.txt'

    lines = load_data_set(data_file=fname)
    blank_line_num = get_blank_line_number(lines=lines)
    fresh_ingredient_ranges = get_fresh_ingredient_id_ranges(lines=lines[:blank_line_num])
    # print(fresh_ingredient_ids)
    ingredient_ids = lines[blank_line_num + 1:]

    count = count_fresh(all_ingredients=ingredient_ids, fresh_ingredient_ranges=fresh_ingredient_ranges)
    print(count)

    # Part 2 count of fresh ingredient ids
    merged_ranges = get_nonoverlapping_ranges(fresh_ingredient_ranges=fresh_ingredient_ranges)
    count = count_fresh_ingredient_ids(fresh_ingredient_ranges=merged_ranges)
    print(count)
if __name__ == '__main__':
    main()
