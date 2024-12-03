import re

def parse_input(fname: str) -> str:
    content = ''
    with open(fname, 'r') as f:
        content = f.read().rstrip()
    
    return content

def compute(content: str) -> int:
    op_pattern = r"mul\([0-9]{1,3},[0-9]{1,3}\)"
    operands_pattern= r"mul\((\d+),(\d+)\)"

    matched_instructions  = re.findall(op_pattern, content)

    operands = [re.match(operands_pattern, op) for op in matched_instructions]
    tuples = [( int(match.group(1)), int(match.group(2)) ) for match in operands]

    return sum(pair[0] * pair[1] for pair in tuples)

def main():
    input = parse_input("input.txt")
    print(compute(input))

if __name__ == "__main__":
    main()
