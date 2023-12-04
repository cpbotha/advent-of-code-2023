# https://adventofcode.com/2023/day/2 - Sat, Dec 2, 2023
# just parsing. was nice to have numpy for any() and max!
# took me 40 minutes in total, from laptop in bed

# %%
from pathlib import Path

import numpy as np

fn = Path(__file__).parent / "input.txt"

lines = fn.read_text().strip().split("\n")

lut = {"red": 0, "green": 1, "blue": 2}

#%%

# total balls available
bag_rgb = np.array((12, 13, 14))
possible_sum = 0
for idx, line in enumerate(lines):
    possible = True
    game_num = idx + 1
    sets = line.split(": ")[1].split(";")
    # each set is e.g. "3 blue, 4 red"
    # if we find an impossible set, we continue to the next for iteration
    # if not, we add game_num to possible
    s_rgb = np.array((0, 0, 0))
    for set_ in sets:
        for nc in set_.split(","):
            n,c = nc.strip().split(" ")
            # finally, we should have r,g,b in a numpy array
            s_rgb[lut[c]] = int(n)

        if np.any(s_rgb > bag_rgb):
            possible = False
            break        

    if possible:
        possible_sum += game_num

# 2237
print(possible_sum)

# %%

possible_sum = 0
total_power = 0
for idx, line in enumerate(lines):
    game_num = idx + 1
    sets = line.split(": ")[1].split(";")
    # the max of all the sets is the minimum numbers of balls needed for this game
    s_rgb_max = np.array((0, 0, 0))
    for set_ in sets:
        for nc in set_.split(","):
            n,c = nc.strip().split(" ")
            # finally, we should have r,g,b in a numpy array
            s_rgb = np.array((0, 0, 0))
            s_rgb[lut[c]] = int(n)
            s_rgb_max = np.maximum(s_rgb_max, s_rgb)

    #total_power += s_rgb_max[0] * s_rgb_max[1] * s_rgb_max[2]
    total_power += s_rgb_max.prod()

# 66681
print(total_power)