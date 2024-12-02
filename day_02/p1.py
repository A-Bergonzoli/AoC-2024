from typing import List


def parse_input(fname: str) -> List[List[int]]:
    lines = []
    with open(fname, 'r') as f:
        lines = f.read().splitlines()
    
    return [list(map(int, line.split())) for line in lines]

def is_safe_by_order_and_difference(record: List[int]) -> bool:
    
    diffs = [a-b for (a, b) in zip(record, record[1:])]

    return all(1 <= diff <= 3 for diff in diffs) or \
           all(-3 <= diff <= -1 for diff in diffs)

def compute(records: List[List[int]]) -> int:
    return sum(is_safe_by_order_and_difference(record) for record in records)

def main():
    records = parse_input("input.txt")
    print(compute(records))

if __name__ == "__main__":
    main()
