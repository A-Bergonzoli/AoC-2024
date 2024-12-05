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

    for update in updates:
        for i, page in enumerate(update[::-1][1:]):
            i += 1
            # for each page, check that none of the following ones should come first
            for elem in gen(update, i):
                for e in elem:
                    if e in rules.keys() and page in rules[e]:
                        bad_updates.add(tuple(update))
    
    bad_updates_list = [list(bad) for bad in bad_updates]

    for bad in bad_updates_list:
        new_bad = reorder_with_rule(rules, bad)
    
    return sum (int(bad[len(bad) // 2]) for bad in bad_updates_list)

def reorder_with_rule(rules: Dict[str, List[str]], update: List[str]) -> List[str]:
    if len(update) == 1:
        return update
    
    for i in range(0, len(update) - 1):
        if update[i] in rules.keys() and update[i+1] in rules[update[i]]:
            update[i+1], update[i] = update[i], update[i+1]
            return reorder_with_rule(rules, update)

    return update 

def main():
    rules, updates = parse("input.txt")
    print(compute(rules, updates))

if __name__ == "__main__":
    main()
