from collections import Counter

def parse_input(fname: str):
    lines = []
    with open(fname, 'r') as f:
        lines = f.read().splitlines()
    
    pairs = [map(int, line.split()) for line in lines]
    return list(zip(*pairs))

def compute_similarity_score(a, b):
    appearance_counter = Counter()

    for number_a in a: 
        for number_b in b:
            if (number_a == number_b):
                appearance_counter[number_a] += 1
    
    a_no_duplicates = list(dict.fromkeys(a))

    return sum([number_a * appearance_counter[number_a]
                if appearance_counter[number_a] > 0
                else 0
                for number_a in a_no_duplicates])
    
def main():
    input = parse_input("input.txt")
    first = input[0]
    second = input[1]
    
    print(compute_similarity_score(first, second))

if __name__ == "__main__":
    main()
