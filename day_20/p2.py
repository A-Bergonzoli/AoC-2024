from typing import Dict, Generator, KeysView, List, Optional, Tuple
from collections import deque, Counter

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

def diamond_gen(cx: int, cy: int, n: int, m: int) -> Generator[Tuple[int, int], None, None]:
    side_len = 41
    half_diag = side_len // 2
    for i in range(cx - half_diag, cx + half_diag + 1):
        for j in range(cy - half_diag, cy + half_diag + 1):
            if abs(cx - i) + abs(cy - j) <= half_diag and i in range(n) and j in range(m):
                yield (i, j)

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
    n, m = len(grid), len(grid[0])
    for nx, ny in diamond_gen(x, y, n, m):
        if (nx, ny) in path:
            yield nx, ny

    return None

def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)

def compute(grid: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> None:
    no_cheat_time, path = dijkstra(grid, start, end)

    cnt = 0
    result = []
    for location, _ in path.items():
        cx, cy = location
        so_far = len(list(path.values())[:cnt])

        seen = set()
        maybe_locations = maybe_get_locations_after_cheat(grid, cx, cy, path.keys())
        for maybe_location in maybe_locations:
            if maybe_location is not None:
                saved = path[maybe_location] - so_far \
                        - manhattan_distance(maybe_location[0], maybe_location[1], cx, cy)  # it takes 'manhattan_distance' moves to do the cheat
                if saved > 0:
                    result.append(saved)
                seen.add(_)

        cnt += 1

    c = Counter(sorted([r for r in result if r > 99]))
    print(c.total())

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
