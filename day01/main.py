import logging
import argparse
import re


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


def part_one(input_data: list[str], args) -> None:
    calibration_values = []
    for line in input_data:
        digits = ''
        for char in line:
            if char.isdigit(): digits += char
        if digits == '': logging.error(f"Line '{line}' has no recognizable digits")
        else: calibration_values.append(int(digits[0] + digits[-1])) 
    logging.info(f"Part One: {sum(calibration_values)}")

NUMBERS = {
    0: 'zero',
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine'
}

def part_two(input_data: list[str], args) -> None:
    calibration_values = []
    for line in input_data:
        found = []
        for number, word in NUMBERS.items():
            numbers = [(number, m.start()) for m in re.finditer(str(number), line)]
            words = [(number, m.start()) for m in re.finditer(word, line)]
            found.extend(numbers)
            found.extend(words)
        sorted_found = sorted(found, key=lambda value: value[1])
        # logging.debug(f"{line}: {sorted_found}")
        calibration_values.append(int(f"{sorted_found[0][0]}{sorted_found[-1][0]}"))
    logging.debug(f"{calibration_values}")
    logging.info(f"Part Two: {sum(calibration_values)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', default=None, required=True)
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]
    if args.part == 1: part_one(input_data, args)
    elif args.part == 2: part_two(input_data, args)
