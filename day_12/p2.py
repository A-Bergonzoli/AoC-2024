from enum import Enum
from typing import Dict, Generator, List, Tuple


def parse(fname: str) -> List[str]:
    with open(fname, 'r') as f:
        return f.read().splitlines()

def move_gen(x: int, y: int) -> Generator[Tuple[int, int], None, None]:
    yield (x - 1, y)
    yield (x + 1, y)
    yield (x, y + 1)
    yield (x, y - 1)

def is_in_bounds(grid: List[str], x: int, y: int) -> bool:
    return x in range(len(grid)) and y in range(len(grid[0]))

def regions_from(grid: List[str]) -> Dict[str, List[List[Tuple[int, int]]]]:
    n, m = len(grid), len(grid[0])
    seen = set()

    def dfs(label, i, j):
        lot = []
        stack = [(i, j)]

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) not in seen and grid[cx][cy] == label:
                seen.add((cx, cy))
                lot.append((cx, cy))

                for nx, ny in move_gen(cx, cy):
                    if is_in_bounds(grid, nx, ny) and (nx, ny) not in seen:
                        stack.append((nx, ny))

        return lot

    regions: Dict[str, List[List[Tuple[int, int]]]] = {}
    for i in range(n):
        for j in range(m):
            if (i, j) not in seen:
                clabel = grid[i][j]
                lot = dfs(clabel, i, j)
                if lot:
                    regions.setdefault(clabel, []).append(lot)

    return regions

class DIR(Enum):
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4,

def move(x: int, y: int) -> Generator[Tuple[Tuple[int, int], DIR], None, None]:
    yield (x - 1, y), DIR.UP
    yield (x + 1, y), DIR.DOWN
    yield (x, y + 1), DIR.RIGHT
    yield (x, y - 1), DIR.LEFT

def how_many_corners(i: int, j: int, grid: List[str]):
    adjacency = []
    for (ni, nj), where in move(i, j):
        if is_in_bounds(grid, ni, nj):
            if grid[ni][nj] == grid[i][j]:
                adjacency.append(where)


    # region 1: if one (u, d, l, r) then 2
    if len(adjacency) == 1:
        return 2

    if len(adjacency) == 2:
        # region 2: if opposite (u/d l/r) then 0
        if DIR.UP in adjacency and DIR.DOWN in adjacency or \
           DIR.LEFT in adjacency and DIR.RIGHT in adjacency:
            return 0

        # region 2: if angled (u/l u/r d/l d/r) at least 1, if no diag then 2
        if DIR.UP in adjacency and DIR.LEFT in adjacency:
            nx, ny = i-1, j-1
            if is_in_bounds(grid, nx, ny) and grid[nx][ny] != grid[i][j]:  # always in bound
                return 2
            return 1
        if DIR.UP in adjacency and DIR.RIGHT in adjacency:
            nx, ny = i-1, j+1
            if is_in_bounds(grid, nx, ny) and grid[nx][ny] != grid[i][j]:  # always in bound
                return 2
            return 1
        if  DIR.DOWN in adjacency and DIR.LEFT in adjacency:
            nx, ny = i+1, j-1
            if is_in_bounds(grid, nx, ny) and grid[nx][ny] != grid[i][j]:  # always in bound
                return 2
            return 1
        if  DIR.DOWN in adjacency and DIR.RIGHT in adjacency:
            nx, ny = i+1, j+1
            if is_in_bounds(grid, nx, ny) and grid[nx][ny] != grid[i][j]:  # always in bound
                return 2
            return 1

    # region 3: if T-shaped (u/l/r d/l/r) between 0 and 2 if both no diag 
    if len(adjacency) == 3:
        if DIR.UP in adjacency and DIR.LEFT in adjacency and DIR.RIGHT in adjacency:
            nx1, ny1 = i-1, j-1
            nx2, ny2 = i-1, j+1
            corners = 0
            if is_in_bounds(grid, nx1, ny1) and grid[nx1][ny1] != grid[i][j]:
                corners += 1
            if is_in_bounds(grid, nx2, ny2) and grid[nx2][ny2] != grid[i][j]:
                corners += 1
            return corners
        if DIR.DOWN in adjacency and DIR.LEFT in adjacency and DIR.RIGHT in adjacency:
            nx1, ny1 = i+1, j-1
            nx2, ny2 = i+1, j+1
            corners = 0
            if is_in_bounds(grid, nx1, ny1) and grid[nx1][ny1] != grid[i][j]:
                corners += 1
            if is_in_bounds(grid, nx2, ny2) and grid[nx2][ny2] != grid[i][j]:
                corners += 1
            return corners
        if DIR.LEFT in adjacency and DIR.UP in adjacency and DIR.DOWN in adjacency:
            nx1, ny1 = i-1, j-1
            nx2, ny2 = i+1, j-1
            corners = 0
            if is_in_bounds(grid, nx1, ny1) and grid[nx1][ny1] != grid[i][j]:
                corners += 1
            if is_in_bounds(grid, nx2, ny2) and grid[nx2][ny2] != grid[i][j]:
                corners += 1
            return corners
        if DIR.RIGHT in adjacency and DIR.UP in adjacency and DIR.DOWN in adjacency:
            nx1, ny1 = i-1, j+1
            nx2, ny2 = i+1, j+1
            corners = 0
            if is_in_bounds(grid, nx1, ny1) and grid[nx1][ny1] != grid[i][j]:
                corners += 1
            if is_in_bounds(grid, nx2, ny2) and grid[nx2][ny2] != grid[i][j]:
                corners += 1
            return corners
    
    # region 4: if +-shaped (u/d/l/r) between 0 and 4 if all no diag
    if len(adjacency) == 4:
        nx1, ny1 = i-1, j-1
        nx2, ny2 = i-1, j+1
        nx3, ny3 = i+1, j-1
        nx4, ny4 = i+1, j+1
        corners = 0
        if is_in_bounds(grid, nx1, ny1) and  grid[nx1][ny1] != grid[i][j]:
            corners += 1
        if is_in_bounds(grid, nx2, ny2) and grid[nx2][ny2] != grid[i][j]:
            corners += 1
        if is_in_bounds(grid, nx3, ny3) and grid[nx3][ny3] != grid[i][j]:
            corners += 1
        if is_in_bounds(grid, nx4, ny4) and  grid[nx4][ny4] != grid[i][j]:
            corners += 1
        return corners

    return 4

def prices_of(regions: Dict[str, List[List[Tuple[int, int]]]], grid: List[str]) -> int:
    price = 0
    for group, lots in regions.items():
        for lot in lots:
            area = len(lot)
            perimeter = 0
            for spot in lot:
                perimeter += how_many_corners(spot[0], spot[1], grid)
            price += area * perimeter

    return price

def compute(grid: List[str]) -> int:
    regions = regions_from(grid)
    return prices_of(regions, grid)

def main() -> None:
    grid = parse("toy_input.txt")
    print(compute(grid))


if __name__ == "__main__":
    main()
