from typing import List


def parse(fname: str) -> List[int]:
    line = []
    with open(fname, 'r') as f:
        line = f.read().split()
    
    return list(map(int, line))

def compute(stones: List[int]) -> List[int]:
    cnt = 0

    for i, stone in enumerate(stones[:]):  # copy
        if (stone == 0):
            stones[i+cnt] = 1

        elif (len(str(stone)) % 2 == 0):
            stone_str = str(stone)
            first, second = stone_str[:len(str(stone))//2], stone_str[len(str(stone))//2:]
            stones[i+cnt] = int(first)
            stones.insert(i+cnt+1, int(second))
            cnt += 1
        
        else:
            stones[i+cnt] *= 2024
    
    return stones


def main():
    stones = parse("input.txt")

    for i in range(25):
        stones = compute(stones)
    
    print(len(stones))
    
if __name__ == "__main__":
    main()
