from typing import Dict, List, Tuple


def parse(fname: str) -> List[int]:
    line = []
    with open(fname, 'r') as f:
        line = f.read().split()
    
    return list(map(int, line))

def dp(stone: int, num_calls: int, memo: Dict[Tuple[int, int], int]) -> int:
    key = (stone, num_calls)
    if key in memo:
        return memo[key]
    
    # affirmative base case
    if num_calls == 0:
        return 1
    
    result = 0
    if stone == 0:
        result = dp(1, num_calls - 1, memo)

    elif (len(str(stone)) % 2 == 0):
        stone_str = str(stone)
        half = len(stone_str) // 2
        first, second = int(stone_str[:half]), int(stone_str[half:])
        result = dp(first, num_calls-1, memo) + dp(second, num_calls-1, memo)

    else:
        result = dp(stone * 2024, num_calls - 1, memo)
    
    memo[key] = result
    return result
    
def main():
    stones = parse("input.txt")

    res = 0
    for i, stone in enumerate(stones):
        memo = {}
        res += dp(int(stone), 75, memo)
    
    print(res)
    
if __name__ == "__main__":
    main()
