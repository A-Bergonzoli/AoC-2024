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
        return 1
    
    num = 0
    for t in towels:
        if target.startswith(t):
            num += dp(target[len(t):], towels, memo)

    memo[target] = num
    return num

def compute(towels, designs):
    count = 0
    for d in designs:
        memo = {}
        count += dp(d, towels, memo)
    
    return count

def main():
    towels, designs = parse("input.txt")
    print(compute(towels, designs))


if __name__ == "__main__":
    main()
