# - only started at 16:32 on Sunday because mom's birthday party!
# - due to super stupid mistake on my part (range(1,10) instead of range(0,10)
#   to get the digits ARGH) only finished p1 at 17:23
#   - lesson for next time: look carefully at the pos_to_symbols dict!
# - part 2 was done at 17:35

# %%
from pathlib import Path
import re

fn = Path(__file__).parent / "input.txt"

lines = fn.read_text().strip().split("\n")

# %% part 1
# scan to build up lut with symbols
pos_to_symbol = {}
digits = [str(i) for i in range(0, 10)]
for r, line in enumerate(lines):
    for c, char in enumerate(line):
        if char == ".":
            continue
        if char not in digits:
            pos_to_symbol[(r, c)] = char


def number_has_symbol(row, start, end):
    # find *any* adjacent symbol for this number to count
    # I'm lazy so I'll check the whole patch around the number
    for r in range(row - 1, row + 2):
        for c in range(start - 1, end + 1):
            if pos_to_symbol.get((r, c), False):
                return True

    return False


# now go through again and find numbers with a neighbouring symbol
part_numbers = []

for r, line in enumerate(lines):
    for mo in re.finditer(r"(\d+)", line):
        # mo.end() is one past the index, just like python range
        if number_has_symbol(r, mo.start(), mo.end()):
            part_numbers.append(int(mo.group()))

# 556110 too high: added up all part numbers
# 543867 just right when I started recognising 0 as a digit ARGH
# 340560 too low: added up only unique part numbers
# add up all numbers in the set
print(sum(part_numbers))


# %% part 2
def find_gear_for_part(row, start, end):
    """
    Parameters
    ----------
    row
        row containing number
    start
        first column of number
    end
        column just after last column of number

    Returns
    -------
    (row, col) of gear if found, else None
    """
    # I'm lazy so I'll check the whole patch around the number
    for r in range(row - 1, row + 2):
        for c in range(start - 1, end + 1):
            if pos_to_symbol.get((r, c), False) == "*":
                return (r, c)

    return None


gear_coord_to_parts = {}
# find all * that are adjacent to two numbers
for r, line in enumerate(lines):
    for mo in re.finditer(r"(\d+)", line):
        # mo.end() is one past the index, just like python range
        gear_rc = find_gear_for_part(r, mo.start(), mo.end())
        if gear_rc is not None:
            if gear_rc not in gear_coord_to_parts:
                gear_coord_to_parts[gear_rc] = [int(mo.group())]
            else:
                gear_coord_to_parts[gear_rc].append(int(mo.group()))

sum_ratios = 0
for gear, parts in gear_coord_to_parts.items():
    if len(parts) == 2:
        ratio = parts[0] * parts[1]
        sum_ratios += ratio

print(sum_ratios)

# oneliner for fun
print(sum([parts[0] * parts[1] for parts in gear_coord_to_parts.values() if len(parts) == 2]))
