# Read the problem, clear I just need to write down the equations:

# given:
# race_time = TOTAL_TIME - charge_time
# dist = race_time * charge_time
# dist > DIST

# thus:
# (TOTAL_TIME - charge_time) * charge_time > DIST
# - charge_time^2 + TOTAL_TIME * charge_time > DIST
# -x^2 + TOTAL_TIME*x > DIST 
# -x^2 + TOTAL_TIME*x - DIST > 0 <---- parabola, so find x where it's zero, bit in the middle = solutions
# a = -1, b = TOTAL_TIME, c=-DIST
# (-b +- sqrt(b^2 -4ac)) / 2a

# ... that was the whole thing done and dusted in <50 minutes thanks to the power of math! 


# %%
from pathlib import Path
import math
import time

start_ns = time.perf_counter_ns()
fn = Path(__file__).parent / "input.txt"

lines = fn.read_text().strip().split("\n")

times = [int(t) for t in lines[0].split(":")[1].strip().split()]
dists = [int(d) for d in lines[1].split(":")[1].strip().split()]

a = -1
def num_sols(t, d):
    b = t
    c = -d
    sqrt = math.sqrt(b*b - 4 * a * c)
    # these are the two roots; all integers between them will beat the race
    min = (-b + sqrt)/2*a
    max = (-b - sqrt)/2*a 
    # epsilon is to exclude the root if it's an integer
    num_sols = math.floor(max-0.0001) - math.ceil(min+0.0001) + 1
    return num_sols
 

mult_num_sols = 1
for t,d in zip(times,dists):
    mult_num_sols *= num_sols(t,d)

print(mult_num_sols)

# %% part 2


time_ = int("".join(lines[0].split(":")[1].strip().split()))
dist = int("".join(lines[1].split(":")[1].strip().split()))
print(num_sols(time_, dist))

end_ns = time.perf_counter_ns()
print(f"Loading and both solutions: {(end_ns - start_ns)/10e6} ms")