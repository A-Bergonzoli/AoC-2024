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

def count_robots_in(quadrant: List[List[str]]) -> int:
    cnt = 0
    for row in quadrant:
        for col in row:
            if col != '.':
                cnt += int(col)
    
    return cnt

def compute(positions: List[Tuple[int, int]],
            velocities: List[Tuple[int, int]],
            seconds: int
    ) -> int:
    n = 103
    half_n = n // 2
    m = 101
    half_m = m // 2

    # empty grid
    grid = []
    for i in range(n):
        grid.append( list(''.join(['.' for _ in range(m)])) )
    
    # update robot positions
    for _ in range(seconds):
        positions = update_positions(positions, velocities, n, m)

    # update grid w/ robot positions
    for i in range(n):
        for j in range(m):
            count = positions.count((i, j))
            if count:
                grid[i][j] = str(count)

    # extrapolate quadrants
    first = [row[:half_m] for row in grid[:half_n]]
    second = [row[half_m+1:] for row in grid[:half_n]]
    third = [row[:half_m] for row in grid[half_n+1:]]
    fourth = [row[half_m+1:] for row in grid[half_n+1:]]
    
    # compute safety factor
    safety_factor = 1
    for quadrant in [first, second, third, fourth]:
        safety_factor *= count_robots_in(quadrant)
    
    return safety_factor
    
def main():
    poss, vels = parse("input.txt")
    print(compute(poss, vels, 100))

if __name__ == "__main__":
    main()
