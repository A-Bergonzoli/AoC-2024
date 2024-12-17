from collections import deque
from enum import Enum
from typing import Dict, Generator, List, Tuple
import functools

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
    results = []
    
    q = deque([ ((x, y, hdg, [(x,y)]), score) ])
    while q:
        (cx, cy, hdg, history), score = q.popleft()

        if (cx, cy) == end:
            results.append({score : history})
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
                    nhistory = history + [(nx, ny)]
                    q.append(( (nx, ny, hdg, nhistory), score + 1 ))
                else:
                    nhistory = history + []
                    q.append(( (cx, cy, direction, nhistory), score + 1000))
    
    unique_tiles = set()
    for result in results:
        for score, history in result.items():
            if score == min(key for result in results for key in result.keys()):
                unique_tiles.update(history)

    return len(unique_tiles)
    
def compute(grid: List[str]) -> int:
    n, m = len(grid), len(grid[0])
    start_x = start_y = 0

    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'S':
                start = (i, j, DIR.EAST)
            elif grid[i][j] == 'E':
                end = (i, j)

    score = dijkstra(grid, start, end, 0)
    return score

def main() -> None:
    grid = parse("input.txt")
    print(compute(grid))


if __name__ == "__main__":
    main()
