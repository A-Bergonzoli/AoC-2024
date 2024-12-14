from collections import defaultdict
from typing import List, Tuple
import re

def parse(fname: str) -> Tuple[List[Tuple[int, int ]], List[Tuple[int, int]]]:
    lines = []
    positions = []
    velocities = []

    with open(fname, 'r') as f:
        lines = [line for line in f.read().splitlines()]

    pattern = r"p=([-+]?\d+),([-+]?\d+) v=([-+]?\d+),([-+]?\d+)"
    for line in lines:
        match = re.search(pattern, line)

        # assume always a match
        positions.append((int(match.group(2)), int(match.group(1))))
        velocities.append((int(match.group(4)), int(match.group(3))))
        
    return positions, velocities

def update_with_wrap(pos: Tuple[int, int],
                     vel: Tuple[int, int],
                     n: int,
                     m: int
    ) -> Tuple[int, int]: 
    cx, cy = pos
    vx, vy = vel
    nx = cx + vx
    ny = cy + vy

    if nx not in range(n):
        nx = nx - n if nx > 0 else nx + n
    if ny not in range(m):
        ny = ny - m if ny > 0 else ny + m
    
    return (nx, ny)

def update_positions(positions: List[Tuple[int, int]],
                     with_velocities: List[Tuple[int, int]],
                     n:int,
                     m:int
    ) -> List[Tuple[int, int]]:
    for i in range(len(with_velocities)):
        nx, ny = update_with_wrap(positions[i], with_velocities[i], n, m)
        positions[i] = (nx, ny)
        
    return positions

def check_adjacency_along_xaxis(positions: List[Tuple[int, int]], n: int):
    x_dict = defaultdict(list)
    
    for x, y in positions:
        x_dict[x].append(y)
    
    for y_list in x_dict.values():
        if len(y_list) > n:
            y_list.sort()
            count = 1
            for i in range(1, len(y_list)):
                if y_list[i] - y_list[i-1] <= 1:
                    count += 1
                else:
                    count = 1
                if count > n:
                    return True
    return False

def compute(positions: List[Tuple[int, int]],
            velocities: List[Tuple[int, int]]
    ) -> int:
    n = 103
    half_n = n // 2
    m = 101
    half_m = m // 2

    # empty grid
    grid = []
    for i in range(n):
        grid.append( list(''.join(['.' for _ in range(m)])) )
    
    # hacky search for easter egg
    for k in range(1, 15000):
        positions = update_positions(positions, velocities, n, m)
    
        # clear grid
        t_grid = []
        for i in range(n):
            t_grid.append( list(''.join(['.' for _ in range(m)])) )
        
        # fill grid
        for i in range(n):
            for j in range(m):
                count = positions.count((i, j))
                if count:
                    t_grid[i][j] = str(count)

        # hacky check for easter egg
        if check_adjacency_along_xaxis(positions, 10):
            for row in t_grid:
                print(row)
            seconds = k
            break

    return seconds

def main():
    poss, vels = parse("input.txt")
    print(compute(poss, vels))

if __name__ == "__main__":
    main()
