def parse(fname: str):
    lines = []
    with open(fname, 'r') as f:
        lines = f.read().splitlines()
    
    return lines

def compute(word_search):
    cnt = 0
    for i, line in enumerate(word_search[1:-1]):
        i += 1
        for j in range(len(line[1:-1])):
            j += 1
            if word_search[i][j] != 'A':
                continue
            elif (word_search[i-1][j-1] == 'M' and word_search[i-1][j+1] == 'S') and (word_search[i+1][j-1] == 'M' and word_search[i+1][j+1] == 'S'):
                cnt += 1
            elif (word_search[i-1][j-1] == 'S' and word_search[i-1][j+1] == 'S') and (word_search[i+1][j-1] == 'M' and word_search[i+1][j+1] == 'M'):
                cnt += 1
            elif (word_search[i-1][j-1] == 'M' and word_search[i-1][j+1] == 'M') and (word_search[i+1][j-1] == 'S' and word_search[i+1][j+1] == 'S'):
                cnt += 1
            elif (word_search[i-1][j-1] == 'S' and word_search[i-1][j+1] == 'M') and (word_search[i+1][j-1] == 'S' and word_search[i+1][j+1] == 'M'):
                cnt += 1
    return cnt

def main():
    word_search = parse("input.txt")
    print(compute(word_search))

if __name__ == "__main__":
    main()
