from typing import Dict, List, Set, Tuple


def parse(fname: str) -> List[Tuple[str, ...]]:
    with open(fname, 'r') as f:
        return [tuple(line.split('-')) for line in f.read().splitlines()]

def compute(connections_list: List[Tuple[str, str]]) -> int:
    d: Dict[str, Set[str]] = {}
    res = 0
    for pc1, pc2 in connections_list:
        if pc1 not in d:
            d[pc1] = set()
        if pc2 not in d:
            d[pc2] = set()
        
        d[pc1].add(pc2)
        d[pc2].add(pc1)
    
    seen = set()
    for pc1 in d.keys():
        for pc2 in d.keys():
            
            if pc2 not in d[pc1]:
                continue
                
            possibles = d[pc1] & d[pc2]
            for pc3 in possibles:
                if pc1.startswith('t') or pc2.startswith('t') or pc3.startswith('t'):
                    triplet = tuple(sorted([pc1, pc2, pc3]))
                    if triplet not in seen:
                        seen.add(triplet)
                        print(pc1, pc2, pc3)
                        res += 1
    return res

def main():
    connections = parse("input.txt")
    print(compute(connections))

if __name__ == "__main__":
    main()

