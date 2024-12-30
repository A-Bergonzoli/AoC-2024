from typing import Dict, List, Tuple


def parse(fname: str) -> Tuple[Dict[str, str], List[str]]:
    with open(fname, 'r') as f:
        first, second = f.read().split('\n\n')
        first_, instructions_ = first.splitlines(), second.splitlines()

        wires = {}
        for elem in first_:
            k, v = elem.split(": ")
            wires[k] = v

    return wires, instructions_

def compute(wires: Dict[str, str], instructions: List[str]):
    
    for i in range(1000):
        for instruction in instructions:
            k1, op, k2, _, res = instruction.split(' ')

            if k1 not in wires.keys() or k2 not in wires.keys():
                continue

            if op == "AND":
                wires[res] = str(int(wires[k1]) & int(wires[k2]))
            elif op == "XOR":
                wires[res] = str(int(wires[k1]) ^ int(wires[k2]))
            elif op == "OR":
                wires[res] = str(int(wires[k1]) | int(wires[k2]))

    res = ""
    for k in sorted(wires.keys()):
        if k.startswith('z'):
            res += wires[k]
    
    return int(res[::-1], 2)

def main():
    w, i = parse("input.txt")
    print(compute(w, i))


if __name__ == "__main__":
    main()
