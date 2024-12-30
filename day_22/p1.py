from typing import List


def parse(fname: str) -> List[int]:
    with open(fname, 'r') as f:
        return [int(line) for line in f.read().splitlines()]

def mix(a: int, b: int) -> int:
    return a ^ b

def prune(a: int) -> int:
    return a % 16777216

def evolve(secret: int) -> int:
    secret = mix(secret*64, secret)
    secret = prune(secret)

    secret = mix(int(secret  / 32), secret)
    secret = prune(secret)

    secret = mix(secret * 2048, secret)
    secret = prune(secret)

    return secret

def main():
    secrets = parse("input.txt")

    results = []
    for secret in secrets:
        for i in range(2000):
            secret = evolve(secret)
        results.append(secret)

    print(sum(results))

if __name__ == "__main__":
    main()
