import logging
import argparse
from collections import deque, defaultdict


def configure_logging(verbose, output_file):
    log_level = logging.DEBUG if verbose else logging.INFO
    if output_file is None:
        logging.basicConfig(
            format='%(message)s',
            level=log_level
        )
    else:
        logging.basicConfig(
            format='%(message)s',
            level=log_level,
            filename=output_file,
            filemode='w'
        )


def char_at(line_index, char_index, input_data):
    if line_index >= 0 and line_index < len(input_data) and char_index >= 0 and char_index < len(input_data[0]):
        return input_data[line_index][char_index]
    return '.'


def populate_group(element, schematic, input_data):
    to_check = deque([element])
    group = {}
    adjacent_symbol = ''
    while len(to_check) > 0:
        e = to_check.popleft()
        if not e[2].isdigit(): adjacent_symbol = e[2]
        for l_mod in [-1, 0, 1]:
            for c_mod in [-1, 0, 1]:
                if (l_mod, c_mod) == (0, 0): continue
                l = e[0] + l_mod
                c = e[1] + c_mod
                if (l, c) in group: continue
                group[(e[0], e[1])] = e[2]
                if ((char := char_at(l, c, input_data)) != '.'):
                    schematic.add((l, c, char))
                    to_check.append((l, c, char))
    return (group, adjacent_symbol)


# What is the sum of all of the part numbers in the engine schematic?
# A number is a part number if it's adjacent (including diagonally) to a symbol (any non-number except period)
def part_one(input_data: list[str], args) -> int:
    schematic = set()
    groups = []
    for line_index,line in enumerate(input_data):
        for char_index,char in enumerate(line):
            if char == '.': continue
            element = (line_index, char_index, char)
            if element in schematic: continue
            schematic.add(element)
            (group, symbol) = populate_group(element, schematic, input_data)
            if symbol != '' and len(group) > 0: groups.append(group)

    parts_sum = 0
    for group in groups:
        lines = defaultdict(list)
        for position,char in group.items():
            if char.isdigit(): lines[position[0]].append((position[1], char))
        for line in lines.values():
            value = ''
            last_x = None
            for x,c in sorted(line, key=lambda x: x[0]):
                if last_x is None:
                    value = c
                elif x == last_x + 1:
                    value += c
                else:
                    parts_sum += int(value)
                    value = c
                last_x = x
            parts_sum += int(value)
    return parts_sum

# A gear is any * symbol that is adjacent to exactly two part numbers.
# Its gear ratio is the result of multiplying those two numbers together.
# What is the sum of all of the gear ratios in your engine schematic?
def part_two(input_data: list[str], args) -> None:
    schematic = set()
    groups = []
    for line_index,line in enumerate(input_data):
        for char_index,char in enumerate(line):
            if char == '.': continue
            element = (line_index, char_index, char)
            if element in schematic: continue
            schematic.add(element)
            (group, symbol) = populate_group(element, schematic, input_data)
            if symbol == '*' and len(group) > 0: groups.append(group)

    gear_ratios = 0
    for group in groups:
        lines = defaultdict(list)
        for position,char in group.items():
            if char.isdigit(): lines[position[0]].append((position[1], char))
        values = []
        for line in lines.values():
            value = ''
            last_x = None
            for x,c in sorted(line, key=lambda x: x[0]):
                if last_x is None:
                    value = c
                elif x == last_x + 1:
                    value += c
                else:
                    values.append(int(value))
                    value = c
                last_x = x
            values.append(int(value))
        if (l:=len(values)) != 2: continue
        gear_ratio = values[0] * values[1]
        gear_ratios += gear_ratio
    return gear_ratios



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', default=None)
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]
    if args.part == 1:
        logging.info(f"Part 1 (test: 4361): {part_one(input_data, args)}")
    elif args.part == 2:
        logging.info(f"Part 2 (test: 467835): {part_two(input_data, args)}")
