from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class Stuff:
    cntA: int
    cntB: int
    config: Dict[str, Tuple[int, int]]

def parse(fname: str) -> List[Dict[str, Tuple[int, int]]]:
    lines = []
    with open(fname, 'r') as f:
        lines = [line for line in f.read().splitlines() if line]
    
    configs = []
    for i in range(0, len(lines), 3):
        ax, ay = int(''.join([char for char in lines[i].split()[-2:][0] if char.isdigit()])), \
                 int(''.join([char for char in lines[i].split()[-2:][1] if char.isdigit()]))

        bx, by = int(''.join([char for char in lines[i+1].split()[-2:][0] if char.isdigit()])), \
                 int(''.join([char for char in lines[i+1].split()[-2:][1] if char.isdigit()]))
        
        px, py = int(''.join([char for char in lines[i+2].split()[-2:][0] if char.isdigit()])), \
                 int(''.join([char for char in lines[i+2].split()[-2:][1] if char.isdigit()]))

        configs.append({'A' : (ax, ay), 'B' : (bx, by), 'prize' : (px, py)})
    
    return configs

def dp2(target: Tuple[int, int], current: Tuple[int, int], stuff: Stuff, visited: Set[Tuple[int, int, int, int]]) -> Optional[Tuple[int, int]]:
    tx, ty = target
    cx, cy = current

    state = (cx, cy, stuff.cntA, stuff.cntB)
    if state in visited:
        return None
    visited.add(state)

    if stuff.cntA > 100 or stuff.cntB > 100:
        return None

    if cx > tx or cy > ty:
        return None
    
    if cx == tx and cy == ty:
        return (stuff.cntA, stuff.cntB)

    # Move A
    cxa = cx + stuff.config['A'][0]
    cya = cy + stuff.config['A'][1]
    stuffA = Stuff(stuff.cntA + 1, stuff.cntB, stuff.config)

    # Move B
    cxb = cx + stuff.config['B'][0]
    cyb = cy + stuff.config['B'][1]
    stuffB = Stuff(stuff.cntA, stuff.cntB + 1, stuff.config)

    resultA = dp2(target, (cxa, cya), stuffA, visited)
    if resultA is not None:
        return resultA
    
    resultB = dp2(target, (cxb, cyb), stuffB, visited)
    if resultB is not None:
       return resultB
    
    return None  # mypy

def compute(configs: List[Dict[str, Tuple[int, int]]]) -> int:
    prices = []
    for config in configs:
        visited: Set[Tuple[int, int, int, int]] = set()
        stuff = Stuff(0, 0, config)
        if dp2(config['prize'], (0, 0), stuff, visited) is not None:
            visited = set()
            cntA, cntB = dp2(config['prize'], (0, 0), stuff, visited)
            prices.append(3*cntA + cntB)
    
    return sum(prices)

def main():
    configs = parse("input.txt")
    print(compute(configs))


if __name__ == "__main__":
    main()
