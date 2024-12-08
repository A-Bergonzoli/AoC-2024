from collections import Counter
import itertools
import math

def parse(fname: str):
    d = {}
    with open(fname, 'r') as f:
        lines = f.read().splitlines()
        for x in range(len(lines)):
            for y in range(len(lines[0])):
                if lines[x][y] != '.':
                    d.setdefault(lines[x][y], set()).update({(x, y)})

    return d

def euclidean_dist(p1, p2):
    return math.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def is_within_boundaries(pos):
    return pos[0] in range(50) and pos[1] in range(50)

def get_antinodes(pair):
    antinodes = []
    p1 = pair[0]
    p2 = pair[1]

    # unit vector lying on vector going from P1 to P2
    dist = euclidean_dist(p1, p2)
    ux = (p2[0] - p1[0]) / dist
    uy = (p2[1] - p1[1]) / dist

    for i in range(150): # lazy because it's sunday
        an_opposite = (round(p1[0] - i * dist * ux, 2), round(p1[1] - i * dist * uy, 2))
        if is_within_boundaries(an_opposite):
            antinodes.append(an_opposite)
        an_same = (round(p2[0] + i * dist * ux, 2), round(p2[1] + i * dist * uy, 2))
        if is_within_boundaries(an_same):
            antinodes.append(an_same)
        
    return antinodes

def compute(antennas):
    c = Counter()

    for ant_v in antennas.values():
        if len(ant_v) < 2:
            continue

        ant_pairs = list(itertools.combinations(ant_v, 2))
        for pair in ant_pairs:
            antinodes = get_antinodes(pair)
            for a in antinodes:
                c[a] += 1
    
    return sum(1 for elem in c if c[elem] > 0)

def main():
    dicts = parse("input.txt")
    print(compute(dicts))


if __name__ == "__main__":
    main()
