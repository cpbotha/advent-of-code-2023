# could only start at 8:10 after school run (as per usual)
# part 1 went smoothly probably aboutt 10 minutes
# part 2 went surprisingly smoothly thanks to my counter idea

# %%
from collections import Counter
from pathlib import Path
import time

start_ns = time.perf_counter_ns()
fn = Path(__file__).parent / "input.txt"

lines = fn.read_text().strip().split("\n")

# %% part 1
sum_pow = 0
for line in lines:
    win_min = line.split(":")[1].split("|")
    win_min[0] = [int(e.strip()) for e in win_min[0].strip().split()]
    win_min[1] = [int(e.strip()) for e in win_min[1].strip().split()]
    winning = [e for e in win_min[1] if e in win_min[0]]
    if len(winning) > 0:
        sum_pow += pow(2, len(winning) - 1)

# 25174
print(sum_pow)


# %% part 2

counter = Counter()
for idx, line in enumerate(lines):
    # we count this card
    counter[idx] += 1
    win, mine = line.split(":")[1].split("|")
    win = [int(e.strip()) for e in win.strip().split()]
    mine = [int(e.strip()) for e in mine.strip().split()]
    winning = [e for e in mine if e in win]
    for i in range(len(winning)):
        # for each of the winning numbers, we get and record a copy of the corresponding subsequent card idx+i+1
        # however, this happens for all copies of the current card we currently have hence += counter[idx]
        counter[idx+i+1] += counter[idx] 

# 6420979
print(sum(counter.values()))

end_ns = time.perf_counter_ns()
print(f"Took {(end_ns-start_ns)/1e6} milli-seconds")