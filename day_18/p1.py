from typing import Dict, Generator, List, Tuple
from collections import deque

NROWS = 71
NCOLS = 71


def parse(fname: str) -> List[Tuple[int, ...]]:
    lines = []

    with open(fname, 'r') as f:
        lines = [tuple(map(int, line.split(',')[::-1]))
                for line in f.read().splitlines()]
    
    '''
    Each byte position is given as an X,Y coordinate, where
    - X is the distance from the left edge of your memory space
    - Y is the distance from the top edge of your memory space.

    Feels more natural the other way around, hence I flipped Xs and Ys
    '''
    
    return lines

def move_gen(cx: int, cy: int) -> Generator[Tuple[int, int], None, None]:
    yield -1,  0
    yield  1,  0
    yield  0,  1
    yield  0, -1

def dijkstra(grid: List[List[str]],
             start: Tuple[int, int],
             end: Tuple[int, int],
) -> int:
    x, y = start
    visited: Dict[Tuple[int, int], int] = {}
    steps = []
    step = 0
    
    q = deque([( (start), step) ])
    while q:
        (cx, cy), step = q.popleft()

        if (cx, cy) == end:
            print("here")
            steps.append(step)
            continue

        state = (cx, cy)
        if state in visited:
            continue
        visited[state] = step
        
        for dx, dy in move_gen(cx, cy):
            nx = cx + dx
            ny = cy + dy
            if nx in range(NROWS) and ny in range(NCOLS) and grid[nx][ny] != '#':
                q.append(( (nx, ny), step + 1 ))

    return min(steps)

def compute(coords: List[Tuple[int]], nbytes: int) -> int:
    grid: List[List[str]] = []
    for i in range(NROWS):
        grid.append([])

        for j in range(NCOLS):
            if (i, j) not in set(coords[:nbytes]):
                grid[i].append('.')
            else:
                grid[i].append('#')

    return dijkstra(grid, (0, 0), (NROWS-1, NCOLS-1))

def main():
    coordinates = parse("input.txt")
    print(compute(coordinates, 1024))


if __name__ == "__main__":
    main()
