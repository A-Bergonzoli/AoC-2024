from collections import Counter
from typing import List

def parse(fname: str) -> List[str]:
    with open(fname, 'r') as f:
        return f.read().splitlines()
    
def rotate_right(guard: str) -> str:
    if (guard == '^'):
        return '>'
    elif (guard == '>'):
        return 'v'
    elif (guard == 'v'):
        return '<'
    elif (guard == '<'):
        return '^'
    
    return ''

def is_done(grid: List[str], x: int, y: int):
    upper_bound = 0
    lower_bound = len(grid) - 1
    left_bound = 0
    right_bound = len(grid[0]) - 1

    is_x_allowed = upper_bound <= x <= lower_bound
    is_y_allowed = left_bound <= y <= right_bound

    if not is_x_allowed or not is_y_allowed:
        return True

    return (x == upper_bound or x == lower_bound or \
           y == left_bound or y == right_bound) and  \
           grid[x][y] != '#'

def compute(grid: List[str]) -> int:
    possible_pos = {'^', '>', 'v', '<'}
    guard_x = prev_x = 0
    guard_y = prev_y = 0
    guard_hdg = '^'

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] in possible_pos:
                guard_x = i
                guard_y = j
                break

    c = Counter({(guard_x, guard_y) : 1})

    while not is_done(grid, guard_x, guard_y):

        if grid[guard_x][guard_y] == '#':
            guard_hdg = rotate_right(guard_hdg)
            c[(guard_x, guard_y)] -= 1
            guard_x = prev_x
            guard_y = prev_y

        prev_x = guard_x
        prev_y = guard_y

        if (guard_hdg == '^'):
            guard_x -= 1
        if (guard_hdg == '>'):
            guard_y += 1
        if (guard_hdg == 'v'):
            guard_x += 1
        if (guard_hdg == '<'):
            guard_y -= 1

        c[(guard_x, guard_y)] += 1

    return sum(1 for count in c.values() if count > 0)

def main() -> None:
    grid = parse("input.txt")
    print(compute(grid))

if __name__ == "__main__":
    main()
