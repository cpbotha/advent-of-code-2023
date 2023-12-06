# started at 7:45 *right* after school run
# part 1 done fairly quickly, then obviously bonked into part 2
# super busy day with headache, finally got my range-based solution correctly submitted on first attempt

# %%
from pathlib import Path
import time

fn = Path(__file__).parent / "input.txt"

sections = fn.read_text().strip().split("\n\n")

# %% part 1

seeds = [int(seed) for seed in sections[0].split()[1:]]

# for each subsequent section, store all luts
maps_luts = []

# sections[0] was seeds, sections[1] is the first map
for map in sections[1:]:
    luts = []
    for map_line in map.strip().split("\n")[1:]:
        nums = [int(e) for e in map_line.split()]
        # store source_start, source_end (past end), dest_start
        luts.append((int(nums[1]), int(nums[1]+nums[2]), int(nums[0])))

    maps_luts.append(luts)

min_loc = None
for seed in seeds:
    # each map_lut takes us from domain to domain, e.g. seed -> soil
    for map_lut in maps_luts:
        for ml_line in map_lut:
            if ml_line[0] <= seed < ml_line[1]:
                seed = ml_line[2] + (seed - ml_line[0])
                # break out of line loop
                # which will take us to the next mapping
                break

    # seed is now location
    if min_loc is None or seed < min_loc:
        min_loc = seed


print(min_loc)

# %% part 2

start_ns = time.perf_counter_ns()
# start, num, start, num, ...
seeds = [int(seed) for seed in sections[0].split()[1:]]
seed_ranges = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]

# for each subsequent section, store all luts
maps_luts = []

# sections[0] was seeds, sections[1] is the first map
for map in sections[1:]:
    luts = []
    for map_line in map.strip().split("\n")[1:]:
        nums = [int(e) for e in map_line.split()]
        # source_start, len, dest_start
        luts.append((int(nums[1]), int(nums[2]), int(nums[0])))

    maps_luts.append(luts)


min_loc = None
# initially, range is contiguous
for range_ in seed_ranges:
    ranges = [range_]
    # each map_lut takes us from domain to domain, e.g. seed -> soil
    # ranges -> output_ranges
    for map_lut in maps_luts:
        output_ranges = []
        # keep on going until we've sent all ranges through THIS map
        while len(ranges) > 0:
            rng = ranges.pop()
            for ml_line in map_lut:
                # just past the end
                ml_end = ml_line[0] + ml_line[1]
                if ml_line[0] <= rng[0] < ml_end:
                    # at least first part of rng is in ml_line
                    # split range, pass through the left part, put right part back on queue
                    # left: rng[0], 
                    r_end = rng[0] + rng[1]
                    if r_end > ml_end:
                        # right part (falls out of range) exists and needs to be handled by stuffing into queue
                        ranges.append((ml_end, r_end - ml_end))
                        r_end = ml_end

                    # left part is now r[0],r_end
                    output_ranges.append((ml_line[2] + (rng[0] - ml_line[0]), r_end - rng[0]))
                    # indicate that rng has been handled
                    rng = None
                    # stop the ml_line search
                    break

            # we've gone through all of the ml_lines, if there's still rng it has to go through as is
            if rng is not None:
                output_ranges.append(rng)

        # preprare for next transformation
        ranges = output_ranges

    # at this point, output_ranges should be the location ranges corresponding to range_
    # each range_ endhs up as one ore more location ranges (loc, num)
    for e in output_ranges:
        if min_loc is None or e[0] < min_loc:
            min_loc = e[0]

# 24261545
print(min_loc)

end_ns = time.perf_counter_ns()
print(f"{(end_ns - start_ns) / 1e6} ms")