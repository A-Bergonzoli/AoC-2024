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
    step = 0
    
    q = deque([( (start), step) ])
    while q:
        (cx, cy), step = q.popleft()

        if (cx, cy) == end:
            return True

        state = (cx, cy)
        if state in visited:
            continue
        visited[state] = step
        
        for dx, dy in move_gen(cx, cy):
            nx = cx + dx
            ny = cy + dy
            if nx in range(NROWS) and ny in range(NCOLS) and grid[nx][ny] != '#':
                q.append(( (nx, ny), step + 1 ))

    return False

def get_grid(coords: List[Tuple[int, ...]], nbytes: int) -> List[List[str]]:
    grid: List[List[str]] = []
    for i in range(NROWS):
        grid.append([])

        for j in range(NCOLS):
            if (i, j) not in set(coords[:nbytes]):
                grid[i].append('.')
            else:
                grid[i].append('#')
    
    return grid

def compute(coords: List[Tuple[int, ...]]) -> Tuple[int, ...]:
    for i in range(len(coords)):
        grid = get_grid(coords, i+1024)
        if not dijkstra(grid, (0, 0), (NROWS-1, NCOLS-1)):
            return coords[i+1024 - 1][::-1]

    return (-1, -1)

def main():
    coordinates = parse("input.txt")
    print(compute(coordinates))


if __name__ == "__main__":
    main()
