import re

def parse_input(fname: str) -> str:
    content = ''
    with open(fname, 'r') as f:
        content = f.read().rstrip()
    
    return content

def is_enabled(match_start, controls) -> bool:
    enabled = True
    
    for control in controls:  # loop to find the most recent
        if control.start() < match_start:
            enabled = True if control.group() == "do()" else False

    return enabled

def compute(content: str) -> int:
    op_pattern = r"mul\([0-9]{1,3},[0-9]{1,3}\)"
    operands_pattern= r"mul\((\d+),(\d+)\)"
    control_pattern = r"(do\(\)|don't\(\))"

    matched_instructions = re.findall(op_pattern, content)
    controls = list(re.finditer(control_pattern, content))

    enabled_instructions = [m for m in matched_instructions \
                            if is_enabled(content.find(m), controls)]

    operands = [re.match(operands_pattern, op) for op in enabled_instructions]
    tuples = [( int(match.group(1)), int(match.group(2)) ) for match in operands]

    return sum(pair[0] * pair[1] for pair in tuples)

    return _sum

def main():
    input = parse_input("input.txt")
    print(compute(input))

if __name__ == "__main__":
    main()
