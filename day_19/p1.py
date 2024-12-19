def parse(fname: str):
    lines = []
    with open(fname, 'r') as f:
        lines = [line for line in f.read().splitlines() if line]
    
    towels = lines[0].split(', ')
    designs = lines[1:]
    
    return towels, designs

def dp(target, towels, memo):
    if target in memo.keys():
        return memo[target]

    if len(target) == 0:
        return True
    
    for t in towels:
        if target.startswith(t):
            can_compose = dp(target[len(t):], towels, memo)
            if can_compose:
                memo[target] = True
                return True

    memo[target] = False
    return memo[target]

def compute(towels, designs):
    count = 0
    for d in designs:
        memo = {}
        if dp(d, towels, memo):
            count += 1
    
    return count

def main():
    towels, designs = parse("input.txt")
    print(compute(towels, designs))


if __name__ == "__main__":
    main()
