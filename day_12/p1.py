from typing import Dict, Generator, List, Tuple

def parse(fname: str) -> List[str]:
    with open(fname, 'r') as f:
        return f.read().splitlines()

def move_gen(x: int, y: int) -> Generator[Tuple[int, int], None, None]:
    yield (x - 1, y)  # up
    yield (x + 1, y)  # down
    yield (x, y + 1)  # left
    yield (x, y - 1)  # right

def is_in_bounds(grid: List[str], x: int, y: int) -> bool:
    return x in range(len(grid)) and y in range(len(grid[0]))

def how_many_borders(i: int, j: int, grid: List[str]) -> int:
    count = 0
    for ni, nj in move_gen(i, j):
        if is_in_bounds(grid, ni, nj):
            if grid[ni][nj] != grid[i][j]:
                count += 1
        else:
            count += 1

    return count

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
                current_label = grid[i][j]
                lot = dfs(current_label, i, j)
                if lot:
                    regions.setdefault(current_label, []).append(lot)

    return regions

def prices_of(regions: Dict[str, List[List[Tuple[int, int]]]], grid: List[str]) -> int:
    price = 0
    for _, lots_list in regions.items():
        for lots in lots_list:
            area = len(lots)
            perimeter = 0
            for lot in lots:
                perimeter += how_many_borders(lot[0], lot[1], grid)
            price += area * perimeter

    return price

def compute(grid: List[str]) -> int:
    regions = regions_from(grid)
    return prices_of(regions, grid)

def main() -> None:
    grid = parse("input.txt")
    print(compute(grid))


if __name__ == "__main__":
    main()
