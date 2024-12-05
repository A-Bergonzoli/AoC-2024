from typing import Dict, Generator, List, Tuple


def parse(fname: str) -> Tuple[Dict[str, List[str]], List[List[str]]]:
    lines = []
    rules: Dict[str, List[str]] = {"-1" : []}
    updates = []

    with open(fname, 'r') as f:
        lines = f.read().splitlines()
    
    for line in lines:
        if '|' in line:
            # rule
            first, second = line.split('|')
            if first in rules.keys():
                rules[first].extend([second])
            else:
                rules[first] = [second]
        elif ',' in line:
            #update
            updates.append(line.split(','))
    
    for v in rules.values():
        v.sort()
    
    return rules, updates

def gen(lst: str, idx: int) -> Generator[str, None, None]:
    yield lst[len(lst) - idx:]
    
def compute(rules: Dict[str, List[str]], updates: List[str]) -> int:
    bad_updates = set()
    good_updates = set()

    for update in updates:
        for i, page in enumerate(update[::-1][1:]):
            i += 1
            # for each page, check that none of the following ones should come first
            for elem in gen(update, i):
                for e in elem:
                    if e in rules.keys() and page in rules[e]:
                        bad_updates.add(tuple(update))
                    else:
                        good_updates.add(tuple(update))
    
    good_updates = {tuple(update) for update in updates} - bad_updates

    return sum (int(good[len(good) // 2]) for good in good_updates)

def main():
    rules, updates = parse("input.txt")
    print(compute(rules, updates))

if __name__ == "__main__":
    main()
