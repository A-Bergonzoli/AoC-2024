#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>

using strings = std::vector<std::string>;

strings ParseInput(const std::string& fname)
{
    return pypp::splitFileLines(fname);
}

int Compute(const strings& ws)
{
    auto total_count { 0 };

    for (int i { 1 }; i < ws.size() - 1; ++i) {
        for (int j { 1 }; j < ws[0].length() - 1; ++j) {
            if (ws[i][j] != 'A')
                continue;
            else if (std::string { ws[i - 1][j - 1], ws[i - 1][j + 1], ws[i + 1][j - 1], ws[i + 1][j + 1] } == "MSMS")
                total_count++;
            else if (std::string { ws[i - 1][j - 1], ws[i - 1][j + 1], ws[i + 1][j - 1], ws[i + 1][j + 1] } == "SSMM")
                total_count++;
            else if (std::string { ws[i - 1][j - 1], ws[i - 1][j + 1], ws[i + 1][j - 1], ws[i + 1][j + 1] } == "MMSS")
                total_count++;
            else if (std::string { ws[i - 1][j - 1], ws[i - 1][j + 1], ws[i + 1][j - 1], ws[i + 1][j + 1] } == "SMSM")
                total_count++;
        }
    }

    return total_count;
}

int main()
{
    auto word_search = ParseInput("input.txt");
    std::cout << Compute(word_search) << std::endl;

    return 0;
}
