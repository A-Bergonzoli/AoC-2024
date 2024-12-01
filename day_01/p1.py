def parse_input(fname: str):
    lines = []
    with open(fname, 'r') as f:
        lines = f.read().splitlines()
    
    pairs = [map(int, line.split()) for line in lines]
    return list(zip(*pairs))

def compute_distance(a, b):
    a = sorted(a)
    b = sorted(b)

    return [abs(elem[0]-elem[1]) for elem in zip(a,b)]
    
def main():
    input = parse_input("input.txt")
    first = input[0]
    second = input[1]
    
    print(sum(compute_distance(first, second)))

if __name__ == "__main__":
    main()
