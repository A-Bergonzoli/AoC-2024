from collections import deque
from enum import Enum
from typing import Dict, Generator, List, Optional, Tuple
import functools
import sys

class DIR(Enum):
    NORTH = 0,
    SOUTH = 1,
    EAST = 2,
    WEST = 3

def parse(fname: str) -> List[str]:
    lines = []
    with open(fname, 'r') as f:
        lines = f.read().splitlines()

    return lines

def move_fwd(cx: int, cy: int, hdg: DIR) -> Tuple[int, int]:
    '''unused'''
    if hdg == DIR.NORTH: 
        return cx - 1, cy + 0
    if hdg == DIR.SOUTH: 
        return cx + 1, cy + 0
    if hdg == DIR.EAST: 
        return cx + 0, cy + 1
    if hdg == DIR.WEST: 
        return cx + 0, cy - 1

def rotate(hdg: DIR, is_clockwise: bool) -> DIR:
    '''unused'''
    if hdg == DIR.NORTH: 
        return DIR.EAST if is_clockwise else DIR.WEST
    if hdg == DIR.SOUTH: 
        return DIR.WEST if is_clockwise else DIR.EAST
    if hdg == DIR.EAST: 
        return DIR.SOUTH if is_clockwise else DIR.NORTH
    if hdg == DIR.WEST: 
        return DIR.NORTH if is_clockwise else DIR.SOUTH

def dp(grid: List[str],
       cx: int,
       cy: int,
       hdg: DIR,
       score: int,
       visited: Dict[Tuple[int, int, DIR], int]
) -> Optional[int]:
    '''
    unused, only works for toy examples >:(]
    '''
    state = (cx, cy, hdg)
    if state in visited and visited[state] <= score:
        return None
    visited[state] = score
    
    if cx not in range(len(grid)) or cy not in range(len(grid[0])):
        return None

    if score > 1000000:
        return None

    if grid[cx][cy] == '#':
        return None

    if grid[cx][cy] == 'E':
        return score

    hdg1 = rotate(hdg, True)
    hdg2 = rotate(hdg, False)

    fx, fy = move_fwd(cx, cy, hdg)

    advance = dp(grid, fx, fy, hdg, score+1, visited)
    rotate_cw = dp(grid, cx, cy, hdg1, score+1000, visited)
    rotate_ccw = dp(grid, cx, cy, hdg2, score+1000, visited)

    results = [result for result in [advance, rotate_cw, rotate_ccw] if result is not None]
    return min( results, default=None )

def move_gen(cx: int, cy: int) -> Generator[Tuple[int, int, DIR], None, None]:
    yield -1,  0, DIR.NORTH
    yield  1,  0, DIR.SOUTH
    yield  0,  1, DIR.EAST
    yield  0, -1, DIR.WEST

def dijkstra(grid: List[str],
             start: Tuple[int, int, DIR],
             end: Tuple[int, int],
             score: int,
) -> int:
    x, y, hdg = start
    visited: Dict[Tuple[int, int, DIR], int] = {}
    scores = []
    
    q = deque([( (x, y, hdg), score) ])
    while q:
        (cx, cy, hdg), score = q.popleft()

        if (cx, cy) == end:
            scores.append(score)
            continue

        state = (cx, cy, hdg)
        if state in visited and visited[state] < score:
            continue
        visited[state] = score
        
        for dx, dy, direction in move_gen(cx, cy):
            nx = cx + dx
            ny = cy + dy
            if nx in range(len(grid)) and ny in range(len(grid[0])) and grid[nx][ny] != '#':
                if (direction == hdg):
                    q.append(( (nx, ny, hdg), score + 1 ))
                else:
                    q.append(( (cx, cy, direction), score + 1000))

    return min(scores) 
    
def compute(grid: List[str]) -> int:
    n, m = len(grid), len(grid[0])
    start_x = start_y = 0

    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'S':
                start = (i, j, DIR.EAST)
            elif grid[i][j] == 'E':
                end = (i, j)
    
    min_score = dijkstra(grid, start, end, 0)
    return min_score

def main() -> None:
    grid = parse("input.txt")
    print(compute(grid))


if __name__ == "__main__":
    main()
