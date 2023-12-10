# when I get that fastmarching feeling, it usually means it's Dijkstra time
# part 1: looked at my 2022 day 12 solution, but this year the pipe constraint
#         means we have to go about it differently. Used some of my old code,
#         but changed to build up the unvisited set as we go along
# part 2: What I *wanted* to do, was have a nice relaxing Sunday with my family.
#         If that was not possible, because my brain was stuck in this problem, I
#         would have preferred to walk the loop in one direction, and then consistently label
#         e.g. left negative and right positive. When done, Dijkstra the negative
#         and then the positive, figure out which one hits the exterior, so the other
#         is interior! However, instead I installed shapely, and just used it to
#         do a bunch of point-in-polygon tests. (walking the loop would have taken
#         me much longer, because also need to work out left and right based on previous
#         step.)

# %%
import sys
import time
from enum import Enum
from pathlib import Path

import numpy as np
import shapely

start_ns = time.perf_counter_ns()

# input.txt: S = L
# test_input2.txt and test_input1.txt: S = F
# test_input3.txt same as 2, but non-loop tiles! should also give 8
# test_input4.txt S = 7 - with 10 interior tiles
fn = Path(__file__).parent / "input.txt"
# s_shape = "F"
s_shape = "L"
# s_shape = "7"

lines = fn.read_text().strip().split("\n")

rows = len(lines)
cols = len(lines[0])

for r, line in enumerate(lines):
    if line.find("S") != -1:
        scoord = (r, line.find("S"))
        break


class Dir(Enum):
    N = (-1, 0)
    E = (0, 1)
    S = (1, 0)
    W = (0, -1)


pipe_to_dirs = {
    "|": [Dir.N, Dir.S],
    "-": [Dir.E, Dir.W],
    "L": [Dir.N, Dir.E],
    "J": [Dir.N, Dir.W],
    "7": [Dir.S, Dir.W],
    "F": [Dir.S, Dir.E],
}

# given the pipe, in what direction is inside/outside
# this looks like the 4-connected topological complement of pipe_to_dirs
# this is what I was planning to use to initialise left / right of the loop
pipe_to_io = {
    "|": [Dir.E, Dir.W],
    "-": [Dir.N, Dir.S],
    "L": [Dir.S, Dir.W],
    "J": [Dir.S, Dir.E],
    "7": [Dir.N, Dir.E],
    "F": [Dir.N, Dir.W],
}


def calc_dist(scoord):
    # unvisited = {(r, c): sys.maxsize for r in range(rows) for c in range(cols) if lines[r][c] != "."}
    # we'll build up invisited with the neighbours as we go through the pipe
    unvisited = {}
    unvisited[scoord] = 0
    visited = {}

    # figure out S's pipe-shape manually
    # store it in the LUT
    pipe_to_dirs["S"] = pipe_to_dirs[s_shape]
    max_dist = 0
    while unvisited:
        # find the smallest distance in unvisited, and set as next cur
        cur = min(unvisited, key=unvisited.get)
        cur_dist = unvisited[cur]

        # visit my two neighbours
        cur_pipe = lines[cur[0]][cur[1]]
        nbr_dirs = pipe_to_dirs[cur_pipe]
        dest_dist = cur_dist + 1
        for nbr_dir in nbr_dirs:
            nbr = (cur[0] + nbr_dir.value[0], cur[1] + nbr_dir.value[1])
            # obviously if we've handled nbr, we must not do it again
            if nbr in visited:
                continue

            # could be that the other side of the loop was here
            if dest_dist < unvisited.get(nbr, sys.maxsize):
                unvisited[nbr] = dest_dist

        # we are done with cur, move it to visited
        visited[cur] = unvisited[cur]
        del unvisited[cur]
        # keep track of the maximum distance
        if visited[cur] > max_dist:
            max_dist = visited[cur]

    return max_dist, visited


max_dist, visited = calc_dist(scoord)

# part 1: 6974
print(f"part1: {max_dist}")


# %% part 2

# visited has all the pipes
interior_unvisited = {}
interior_visited = {}

pipe_to_dirs["S"] = pipe_to_dirs[s_shape]
# walk from scoord until we're back at scoord to build up polygon


cur = scoord
# do one step "back" (arbitrarily the seond direction of the two)
dir_to_prev = pipe_to_dirs[lines[cur[0]][cur[1]]][1]
prev = (cur[0] + dir_to_prev.value[0], cur[1] + dir_to_prev.value[1])

# walk the loop in one direction by keeping track of previous step
# this will give us polygon coordinates
loop_coords = {}
while True:
    cur_pipe = lines[cur[0]][cur[1]]
    loop_coords[cur] = cur_pipe
    dirs_to_next = pipe_to_dirs[cur_pipe]
    nexts = [(cur[0] + d.value[0], cur[1] + d.value[1]) for d in dirs_to_next]
    new_cur = nexts[0] if nexts[0] != prev else nexts[1]
    prev = cur
    cur = new_cur

    if cur == scoord:
        break

poly = shapely.Polygon(loop_coords.keys())

non_loop_coords = {(r, c): True for r in range(rows) for c in range(cols) if (r, c) not in loop_coords}

inside = 0
for coord in non_loop_coords:
    if poly.contains(shapely.geometry.Point(coord)):
        inside += 1

# 273
print(inside)
