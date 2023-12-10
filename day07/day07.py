# part 1: Counter is again super useful, and I'm happy with the lexicographic sorting trick
# part 2: URGH, but got it done after a few Joker to Joker conversion issues

# did the grouping, then within group sorting
# could also just have created a single key with e.g. (group, within_group)

# %%
import copy
from collections import Counter
from functools import cmp_to_key
from pathlib import Path
import math
import time

start_ns = time.perf_counter_ns()
fn = Path(__file__).parent / "input.txt"

lines = fn.read_text().strip().split("\n")

hands = []
for line in lines:
    hand, bid = line.split()
    c = Counter(hand)
    hands.append((c, int(bid), hand))


# %% part 1
# go through all hands, throw in 7 groups according to type
groups = [[] for _ in range(7)]
for hand in hands:
    vals = hand[0].values()
    if any((v==5 for v in vals)):    
        # five of a kind
        groups[0].append(hand)
    elif any((v==4 for v in vals)):
        # four of a kind
        groups[1].append(hand)
    elif any((v==3 for v in vals)):
        if any((v==2 for v in vals)):
            # full house
            groups[2].append(hand)
        else:
            # three of a kind
            groups[3].append(hand)
    elif any((v==2 for v in vals)):
        if len([v for v in vals if v == 2]) == 2:
            # two pair
            groups[4].append(hand)
        else:
            # one pair
            groups[5].append(hand)
    else:
        # high card
        groups[6].append(hand)
    

# now go through each group and sort it

s = "AKQJT98765432" 

# by the power of lexicographical sorting!
# iow just transform the hand strings into arrays that will be correctly sorted by rank
def skey(hand):
    # ord('a') = 97
    return [97 + s.index(lab) for lab in hand[2]]


for group in groups:
    group.sort(key=skey)

unrolled = []
for group in groups:
    unrolled.extend(group)

tot = 0
for idx, hand in enumerate(unrolled):
    rank = len(unrolled) - idx
    tot += hand[1] * rank

# 250120186
print(tot)


# %% part 2

# go through all hands, throw in 7 groups according to type
groups = [[] for _ in range(7)]
for hand in hands:
    # if we have jokers, upgrade the hand as far as possible
    if 'J' in hand[0] and hand[2] != "JJJJJ":
        proxy_counter = copy.deepcopy(hand[0]) 
        # find the single most common label and its freq
        # first do the two most common
        mc2 = proxy_counter.most_common(2)
        # because we need to skip the joker
        mci = 1 if mc2[0][0] == 'J' else 0
        mcl, mcv = mc2[mci]
        # convert jokers to that label
        proxy_counter[mcl] += proxy_counter['J']
        # remove jokers
        del proxy_counter['J']
        # whoops: this showed me that I was also transforming most common J into J
        print(f"{hand[2]}: {mcl} from {mcv} to {proxy_counter[mcl]} ")
    else:
        proxy_counter = hand[0]

    vals = proxy_counter.values()
    if any((v==5 for v in vals)):    
        # five of a kind
        groups[0].append(hand)
    elif any((v==4 for v in vals)):
        # four of a kind
        groups[1].append(hand)
    elif any((v==3 for v in vals)):
        if any((v==2 for v in vals)):
            # full house
            groups[2].append(hand)
        else:
            # three of a kind
            groups[3].append(hand)
    elif any((v==2 for v in vals)):
        if len([v for v in vals if v == 2]) == 2:
            # two pair
            groups[4].append(hand)
        else:
            # one pair
            groups[5].append(hand)
    else:
        # high card
        groups[6].append(hand)
    

# now go through each group and sort it

s_j = "AKQT98765432J" 

# by the power of lexicographical sorting!
# iow just transform the hand strings into arrays that will be correctly sorted by rank
def skey(hand):
    # ord('a') = 97
    return [97 + s_j.index(lab) for lab in hand[2]]


for group in groups:
    group.sort(key=skey)

unrolled = []
for group in groups:
    unrolled.extend(group)

tot = 0
for idx, hand in enumerate(unrolled):
    rank = len(unrolled) - idx
    tot += hand[1] * rank

# sub 1: 250917984 too high. Worked for my test_data where I only increased the max label with jokers
# sub 2: 250665248 CORRECT. Some logging prints showed that I was upgrading Jokers to more Jokers
print(tot)


# %% part 2