from typing import Dict, Generator, KeysView, List, Optional, Tuple
from collections import deque

def parse(fname: str) -> List[str]:
    lines = []
    with open(fname, 'r') as f:
        lines = f.read().splitlines()
    
    return lines

def move_gen(cx: int, cy: int) -> Generator[Tuple[int, int], None, None]:
    yield -1,  0
    yield  1,  0
    yield  0,  1
    yield  0, -1

def move_gen2(cx: int, cy: int) -> Generator[Tuple[int, int], None, None]:
    yield -2,  0
    yield  2,  0
    yield  0,  2
    yield  0, -2

def dijkstra(grid: List[List[str]],
             start: Tuple[int, int],
             end: Tuple[int, int],
) -> Tuple[int, Dict[Tuple[int, int], int]]:
    n = len(grid)
    m = len(grid[0])
    visited: Dict[Tuple[int, int], int] = {}
    steps = []
    step = 0
    
    q = deque([( (start), step) ])
    while q:
        (cx, cy), step = q.popleft()
        
        state = (cx, cy)
        if state in visited:
            continue
        visited[state] = step

        if (cx, cy) == end:
            steps.append(step)
            continue
        
        for dx, dy in move_gen(cx, cy):
            nx = cx + dx
            ny = cy + dy
            if nx in range(n) and ny in range(m) and grid[nx][ny] != '#':
                q.append(( (nx, ny), step + 1 ))

    return min(steps), visited

def maybe_get_locations_after_cheat(grid: List[List[str]],
                                    x: int,
                                    y: int,
                                    path: KeysView[Tuple[int, int]]
) -> Generator[Optional[Tuple[int, int]], None, None]:
    for (dx, dy), (dx2, dy2) in zip(move_gen(x, y), move_gen2(x,y)): 
        nx, ny = x + dx, y + dy
        nx2, ny2 = x + dx2, y + dy2
        if (nx2, ny2) in path and grid[nx][ny] == '#':
            yield nx2, ny2

    return None

def compute(grid: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> None:
    no_cheat_time, path = dijkstra(grid, start, end)

    cnt = 0
    result = []
    for location, _ in path.items():
        cx, cy = location
        so_far = len(list(path.values())[:cnt])

        maybe_locations = maybe_get_locations_after_cheat(grid, cx, cy, path.keys())
        for maybe_location in maybe_locations:
            if maybe_location is not None:
                saved_picoseconds = path[maybe_location] - so_far - 2  # it takes two moves to do the cheat
                if saved_picoseconds > 0:
                    result.append(saved_picoseconds)
        
        cnt += 1

    print(sum([1 for r in result if r > 99]))

def main():
    grid = parse("input.txt")
    n, m = len(grid), len(grid[0])

    start = ()
    end = ()
    for i in range(n):    
        for j in range(m):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'E':
                end = (i, j)

    compute(grid, start, end)


if __name__ == "__main__":
    main()
