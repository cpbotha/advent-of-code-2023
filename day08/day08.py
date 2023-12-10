# %%
from itertools import cycle
from pathlib import Path
import math
import re
import time

start_ns = time.perf_counter_ns()
fn = Path(__file__).parent / "input.txt"

lines = fn.read_text().strip().split("\n")

lut = {}
for line in lines[2:]:
    mo = re.match("([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)", line)
    if mo.group(1) in lut:
        print("DUPLICATE!")
    # these days, python dicts maintain order
    lut[mo.group(1)] = (mo.group(2), mo.group(3))

bleh = {"R": 1, "L": 0}
path = [bleh[c] for c in lines[0]]

# %% part 1
# Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
# in the test data, AAA and ZZZ are first and last, but not in the actual data
cur = "AAA"
dest = "ZZZ"

path_idx = 0
num_steps = 0
while cur != dest:
    cur = lut[cur][path[path_idx]]
    num_steps += 1
    path_idx += 1
    if path_idx == len(path):
        path_idx = 0

# 11309
print(num_steps)

# %% part 2 brute force won't work on full data

cur_nodes = [k for k in lut if k.endswith("A")]

path_idx = 0
num_steps = 0
while any(((not cur.endswith("Z")) for cur in cur_nodes)):
    for i, cur in enumerate(cur_nodes):
        cur_nodes[i] = lut[cur][path[path_idx]]
    num_steps += 1
    path_idx += 1
    if path_idx == len(path):
        path_idx = 0

    if num_steps % 1000 == 0:
        print(num_steps, cur_nodes)

# %% part 2 I peeked; would have spoiled my work day if I had struggled on with a small chance of discovering solution
# the insight I was missing is this:
# - BECAUSE the path is repeating
# - each cur_node will cycle through its Zs over and over, at its own frequency, as we repeat the path
# - the total num_steps, where all nodes are at their Zs simultaneously, must be the lowest common multiple of each of their respective steps-to-Z
# - I will submit this solution only by this evening so as not to skew my position on any private leaderboards

cur_nodes = [k for k in lut if k.endswith("A")]
stepss = []
for cur_node in cur_nodes:
    num_steps = 0
    for dir in cycle(path):
        cur_node = lut[cur_node][dir]
        num_steps += 1
        if cur_node.endswith("Z"):
            break

    stepss.append(num_steps)

num_steps = math.lcm(*stepss)

# 13_740_108_158_591
print(num_steps)
