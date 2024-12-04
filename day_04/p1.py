import re

def parse(fname: str):
    lines = []
    with open(fname, 'r') as f:
        lines = f.read().splitlines()
    
    return lines

def compute(word_search):
    cnt_horizontal = 0
    cnt_vertical = 0
    cnt_diagonal = 0

    def _find_all(pattern, in_text):
        return len(re.findall(f"(?={pattern}|{pattern[::-1]})", in_text))

    cnt_horizontal = sum(_find_all("XMAS", row) for row in word_search)
    cnt_vertical = sum(_find_all("XMAS", "".join(col)) for col in zip(*word_search))

    # diagonal downwards
    for i, line in enumerate(word_search[:-3]):
        for j in range(len(line[:-3])):
            word = word_search[i][j] + word_search[i+1][j+1] + word_search[i+2][j+2] + word_search[i+3][j+3]
            if word == "XMAS" or word == "SAMX":
                cnt_diagonal += 1

    # diagonal upwards
    for i, line in enumerate(word_search[3:]):
        i += 3
        for j in range(len(line[:-3])):
            word = word_search[i][j] + word_search[i-1][j+1] + word_search[i-2][j+2] + word_search[i-3][j+3]
            if word == "XMAS" or word == "SAMX":
                cnt_diagonal += 1
    
    return cnt_horizontal + cnt_vertical + cnt_diagonal

def main():
    word_search = parse("input.txt")
    print(compute(word_search))

if __name__ == "__main__":
    main()
