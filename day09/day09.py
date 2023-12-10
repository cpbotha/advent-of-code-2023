# part 1:

# late night thanks to year end function, brain had great difficulty recursing
# this morning, but somehow I just pushed through. happiness at working with the
# test data was soon dashed when it failed on the full set.
# ... after much gnashing of teeth, discovered my check for only last delta 0
# instead of all of them!

# part 2:
# fortunately a simple reverse of the list

# %%
import time
from pathlib import Path

import numpy as np

start_ns = time.perf_counter_ns()
fn = Path(__file__).parent / "input.txt"

lines = fn.read_text().strip().split("\n")


def calc_delta(nums):
    # calculate deltas between subsequent numbers
    deltas = np.diff(nums, axis=0)
    print(deltas)

    # if deltas[-1] == 0: # <---- fails on full data doh
    if np.all(deltas == 0):
        # this means nums (current sequence) is constant, so just repeat!
        return 0
    else:
        # current sequence is not constant, we have to go deeper
        return deltas[-1] + calc_delta(deltas)


tot = 0
rev_tot = 0
next_nums = []
for line in lines:
    nums = np.array([int(e) for e in line.strip().split()])

    # part 1
    next_num = nums[-1] + calc_delta(nums)
    tot += next_num

    # part 2
    rev_nums = nums[::-1]
    rev_tot += rev_nums[-1] + calc_delta(rev_nums)


# 1743490461 too high ARGH
# 1743490457
print(tot)
# 1053
print(rev_tot)
