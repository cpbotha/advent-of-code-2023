# started late because work
# banged out solution in a few minutes, adapted to part 2 with extended regex, but answer too high
# had to check reddit to read about the overlap issue, and then figure out how to get finditer
# to work with overlapping matches (?= positive lookahead)

# %%
from pathlib import Path

import re

fn = Path(__file__).parent / "input.txt"

lines = fn.read_text().strip().split("\n")

# %%

tot = 0
for line in lines:
    first = int(re.search("(\d)", line).group(1))
    # re search from end by reversing the string
    last = int(re.search("(\d)", line[::-1]).group(1))
    tot += int(f"{first}{last}")

# 54927
print(tot)

# %%
bleh = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

tot = 0
for line in lines:
    first = None
    # problem is that you can have e.g. eightwo or eighthree so without
    # lookahead ?= you'll detect eight but not the two or the three for the last
    # number
    # also see https://stackoverflow.com/a/20104639 for a slightly cleaner way to get first / last from iterator
    for m in re.finditer("(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line):
        if first is None:
            first = m.group(1)

    last = m.group(1)

    try:
        first_n = int(first)
    except ValueError:
        first_n = bleh.index(first) + 1

    try:
        last_n = int(last)
    except ValueError:
        last_n = bleh.index(last) + 1

    tot += int(f"{first_n}{last_n}")

# without taking into account overlap this was 54607
# correct answer is 54581
print(tot)

# %%
# https://stackoverflow.com/a/5616910

s = "eightwo"
matches = re.finditer(r"(?=(two|eight))", s)
results = [match.group(1) for match in matches]
print(results)

s = "123456789123456789"
matches = re.finditer(r'(?=(\d{10}))', s)
results = [int(match.group(1)) for match in matches]
print(results)
