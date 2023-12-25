import logging
import argparse
import re
from collections import defaultdict


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


def scratch_card(line, line_pattern):
    m = line_pattern.match(line)
    card_id = int(m.group(1))
    winning_numbers = m.group(2).strip().split()
    have_numbers = m.group(3).strip().split()
    matches = len([n for n in winning_numbers if n in have_numbers])
    return (card_id, matches)


# two lists of numbers separated by a vertical bar (|):
#   a list of winning numbers
#   a list of numbers you have
# The first match makes the card worth one point
# each match after the first doubles the point value of that card
# => points = 2^(matches-1)
def part_one(input_data: list[str], args) -> int:
    line_pattern = re.compile("Card\s+(\d+):(.*) \| (.*)")
    total_points = 0
    for line in input_data:
        (card_id, matches) = scratch_card(line, line_pattern)
        points = 2**(matches-1) if matches > 0 else 0
        total_points += points
    return total_points


# Instead of points, you win more cards.
# Eg: card 6 has 2 matching numbers => you win another copy of card 7 and card 8
# Eg: card 11 has 4 matching numbers => you win cards 12, 13, 14, 15
# Cards you win can win you more cards.
def part_two(input_data: list[str], args) -> int:
    line_pattern = re.compile("Card\s+(\d+):(.*) \| (.*)")
    card_counts = defaultdict(int)
    for line in input_data:
        (card_id, matches) = scratch_card(line, line_pattern)
        card_counts[card_id] += 1
        for i in range(matches):
            card_counts[card_id + i + 1] += card_counts[card_id]
        logging.debug(f"Card {card_id} won {matches} new cards => {card_counts}")
    return sum(v for v in card_counts.values())


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
        logging.info(f"Part 1 (test: 13): {part_one(input_data, args)}")
    elif args.part == 2:
        logging.info(f"Part 2 (test: 30): {part_two(input_data, args)}")
