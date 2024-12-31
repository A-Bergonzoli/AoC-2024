from typing import List

def parse(fname: str) -> List[List[str]]:
    with open(fname, 'r') as f:
        return [list(line) for line in f.read().splitlines()]

def rotate_right(guard: str) -> str:
    if (guard == '^'):
        return '>'
    if (guard == '>'):
        return 'v'
    if (guard == 'v'):
        return '<'
    if (guard == '<'):
        return '^'
    
    return ''

def is_done(grid: List[List[str]], x: int, y: int) -> bool:
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

def compute(grid: List[List[str]]) -> int:
    cnt = 0
    guard_x = 0
    guard_y = 0

    # find start
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] in "^>v<":
                guard_x = i
                guard_y = j
                break

    for ox in range(len(grid)):
        print(f"Currently on line {ox}...")
        for oy in range(len(grid[0])):
            if grid[ox][oy] == '#' or grid[ox][oy] == '^':
                continue  # skip

            grid[ox][oy] = "#"
            cx, cy = guard_x, guard_y 
            dir = grid[cx][cy]
            seen = set()

            while cx in range(len(grid)) and cy in range(len(grid[0])) and (cx, cy, dir) not in seen:
                seen.add((cx, cy, dir))
                while True:
                    nx, ny = cx, cy
                    if (dir == '^'):
                        nx -= 1
                    if (dir == '>'):
                        ny += 1
                    if (dir == 'v'):
                        nx += 1
                    if (dir == '<'):
                        ny -= 1

                    if nx in range(len(grid)) and ny in range(len(grid[0])) and grid[nx][ny] == '#':
                        dir = rotate_right(dir)
                    else:
                        cx, cy = nx, ny
                        break

            if (cx, cy, dir) in seen:
                cnt += 1

            grid[ox][oy] = '.'

    return cnt

def main():
    grid = parse("toy_input.txt")
    print(compute(grid))


if __name__ == "__main__":
    main()
