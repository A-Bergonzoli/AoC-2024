from typing import Generator, List, Set, Tuple


def parse(fname: str) -> List[str]:
    lines = []
    with open(fname, 'r') as f:
        lines = f.read().splitlines()
    
    return lines

def get_trail_heads(grid: List[str]) -> List[Tuple[int, int]]:
    trailheads = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '0':
                trailheads.append((row, col))
    
    return trailheads

def is_in_bounds(grid: List[str], coord_x: int, coord_y: int) -> bool:
    return coord_x in range(len(grid)) and coord_y in range(len(grid[0]))

def move_gen(x: int, y: int) -> Generator[Tuple[int, int], None, None]:
    yield (x, y + 1)  # Up
    yield (x, y - 1)  # Down
    yield (x - 1, y)  # Left
    yield (x + 1, y)  # Right

def dp(grid: List[str], row: int, col: int, current: int, memo: Set[Tuple[int, int]]) -> int:
    # negative base case
    if (row, col) in memo:
        return 0
    memo.add((row, col))    
    
    # affirmative base case
    if grid[row][col] == '9':
        return 1

    result = 0
    current = int(grid[row][col])
    for nrow, ncol in move_gen(row, col):
        if is_in_bounds(grid, nrow, ncol):
            if (int(grid[nrow][ncol]) == current + 1):
                result += dp(grid, nrow, ncol, current, memo)
    
    return result

def compute(grid: List[str]) -> int:
    score = 0
    trailheads = get_trail_heads(grid)
    
    for head in trailheads:
        memo: Set[Tuple[int, int]] = set()
        score += dp(grid, head[0], head[1], 0, memo)

    return score

def main() -> None:
    grid = parse("input.txt")
    print(compute(grid))

if __name__ == "__main__":
    main()
