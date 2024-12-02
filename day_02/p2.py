from typing import Generator, List


def parse_input(fname: str) -> List[List[int]]:
    lines = []
    with open(fname, 'r') as f:
        lines = f.read().splitlines()
    
    return [list(map(int, line.split())) for line in lines]

def is_safe_by_order_and_difference(record: List[int]) -> bool:
    
    diffs = [a-b for (a, b) in zip(record, record[1:])]

    return all(1 <= diff <= 3 for diff in diffs) or \
           all(-3 <= diff <= -1 for diff in diffs)

def generate_mutations(record: List[int]) -> Generator[List[int]]:
    """
    Generate sub-lists of the given list, excluding one element at a time,
    followed by the whole list.
    
    Args:
       record : The list to generate sub-lists from.
    
    Yields:
       A sublist of the original list with one element excluded at a time,
       and finally the original list.
       
    Example:
        [1, 2, 3, 4, 5] generates:
        - [2, 3, 4, 5]
        - [1, 3, 4, 5]
        - [1, 2, 4, 5]
        - [1, 2, 3, 5]
        - [1, 2, 3, 4, 5]], i.e. the original list
    """
    for i in range(len(record)):
        yield record[:i] + record[i+1:]
    
    yield record # original

def compute(records: List[List[int]]) -> int:
    return sum(
        any(is_safe_by_order_and_difference(modified)
            for modified in generate_mutations(record))  
        for record in records)

def main():
    records = parse_input("input.txt")
    print(compute(records))

if __name__ == "__main__":
    main()
