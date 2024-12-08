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
    p1 = pair[0]
    p2 = pair[1]

    # unit vector lying on vector going from P1 to P2
    dist = euclidean_dist(p1, p2)
    ux = (p2[0] - p1[0]) / dist
    uy = (p2[1] - p1[1]) / dist

    antinode1 = (round(p1[0] - dist * ux, 2), round(p1[1] - dist * uy, 2))  # dist away from P1, in opposite direction wrt u={ux, uy}
    antinode2 = (round(p2[0] + dist * ux, 2), round(p2[1] + dist * uy, 2))  # dist away from P2, in same          "     "      "

    antinode1 = antinode1 if is_within_boundaries(antinode1) else None
    antinode2 = antinode2 if is_within_boundaries(antinode2) else None

    return antinode1, antinode2

def compute(antennas):
    c = Counter()

    for ant_v in antennas.values():
        if len(ant_v) < 2:
            continue

        ant_pairs = list(itertools.combinations(ant_v, 2))
        for pair in ant_pairs:
            antinode_1, antinode_2 = get_antinodes(pair)

            if antinode_1 is not None:
                c[antinode_1] += 1
            if antinode_2 is not None:
                c[antinode_2] += 1

    return sum(1 for elem in c if c[elem] > 0)

def main():
    dicts = parse("input.txt")
    print(compute(dicts))


if __name__ == "__main__":
    main()
