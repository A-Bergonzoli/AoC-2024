from typing import Dict, List, Tuple
import numpy as np


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

        configs.append({'A' : (ax, ay), 'B' : (bx, by), 'prize' : (px+10000000000000, py+10000000000000)})
    
    return configs

def compute(configs: List[Dict[str, Tuple[int, int]]]) -> int:
    prices = []
    for i, config in enumerate(configs):
        coef_mat = np.matrix([config['A'], config['B']]).T
        knowns = np.matrix([[config['prize'][0]], [config['prize'][1]]])

        unknowns = np.linalg.solve(coef_mat, knowns)
        cntA, cntB = round(unknowns[0,0]), round(unknowns[1,0])

        if config['A'][0] * cntA + config['B'][0] * cntB == config['prize'][0] and \
            config['A'][1] * cntA + config['B'][1] * cntB == config['prize'][1]:
            prices.append(3 * cntA + cntB)

    return sum(prices)

def main():
    configs = parse("input.txt")
    print(compute(configs))


if __name__ == "__main__":
    main()
