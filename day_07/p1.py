from typing import List, Tuple

def parse(fname: str) -> Tuple[ List[int], List[List[int]]]:
    lines: List[str] = []
    values = []
    operands = []

    with open(fname, 'r') as f:
        for line in f.read().splitlines():
            first, rest = line.split(':') 
            values.append(int(first))
            operands.append([int(op) for op in rest.split()])

    return values, operands

def perform(op1: int, op: str, op2: int) -> int:
    return op1 + op2 if op == '+' else op1 * op2

def dp(target: int, operands: List[int], operator: str) -> bool:
    # base case
    if len(operands) == 1:
        return operands[0] == target

    for operand in operands:
        new_operand = perform(operands[0], operator, operands[1])
        new_operands = operands[1:]
        new_operands[0] = new_operand
        operators = dp(target, new_operands, '+') or \
                    dp(target, new_operands, '*') 

        return operators
    
    return False

def compute(values: List[int], operands: List[List[int]]) -> int:
    valid_eq_if_start_with_plus = set()
    valid_eq_if_start_with_mul = set()

    for i, val in enumerate(values):
        if dp(val, operands[i], '+',):
            valid_eq_if_start_with_plus.add(i)
        if dp(val, operands[i], '*',):
            valid_eq_if_start_with_mul.add(i)

    valid = valid_eq_if_start_with_plus.union(valid_eq_if_start_with_mul)
    return sum(values[idx] for idx in valid)

def main():
    values, operands = parse("input.txt")
    print(compute(values, operands))


if __name__ == "__main__":
    main()
