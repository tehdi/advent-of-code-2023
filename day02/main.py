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


reds_pattern = re.compile("(\d+) red")
greens_pattern = re.compile("(\d+) green")
blues_pattern = re.compile("(\d+) blue")


def find_max(pattern, line):
    return max((int(m.group(1)) for m in pattern.finditer(line)), default=0)


# Determine which games would have been possible if the bag had been loaded with only
# 12 red cubes, 13 green cubes, and 14 blue cubes.
# What is the sum of the IDs of those games?
def part_one(input_data: list[str], args) -> None:
    max_reds = 12
    max_greens = 13
    max_blues = 14
    game_pattern = re.compile("Game (\d+):")

    valid_games = []
    for line in input_data:
        seen_reds = find_max(reds_pattern, line)
        seen_greens = find_max(greens_pattern, line)
        seen_blues = find_max(blues_pattern, line)
        if seen_reds <= max_reds and seen_greens <= max_greens and seen_blues <= max_blues:
            game_id = int(game_pattern.match(line).group(1))
            valid_games.append(game_id)
            logging.debug(f"Game {game_id} is valid with {seen_reds} reds, {seen_greens} greens, and {seen_blues} blues")
    logging.info(f"Part One: {sum(valid_games)}")


# The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
# For each game, find the minimum set of cubes that must have been present.
# What is the sum of the power of these sets?
def part_two(input_data: list[str], args) -> None:
    powers = []
    for line in input_data:
        seen_reds = find_max(reds_pattern, line)
        seen_greens = find_max(greens_pattern, line)
        seen_blues = find_max(blues_pattern, line)
        power = seen_reds * seen_greens * seen_blues
        powers.append(power)
    logging.info(f"Part Two: {sum(powers)}")


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
    if args.part == 1: part_one(input_data, args)
    elif args.part == 2: part_two(input_data, args)
