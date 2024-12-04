#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>

/* This code sucks */

using strings = std::vector<std::string>;

strings ParseInput(const std::string& fname)
{
    return pypp::splitFileLines(fname);
}

int GetSubstrCount(const std::string& substr, const std::string& in_str)
{
    auto count { 0 };
    auto it = in_str.find(substr, 0);
    while (it != std::string::npos) {
        count++;
        it = in_str.find(substr, it + 1);
    }

    return count;
}

strings Transpose(const strings& matrix)
{
    strings transposed { matrix[0].length(), std::string(matrix.size(), ' ') };

    for (size_t i = 0; i < matrix.size(); ++i)
        for (size_t j = 0; j < matrix[0].length(); ++j)
            transposed[j][i] = matrix[i][j];

    return transposed;
}

int Compute(const strings& ws)
{
    auto total_count { 0 };

    for (const auto row : ws) {
        total_count += GetSubstrCount("XMAS", row);
        total_count += GetSubstrCount("SAMX", row);
    }

    const auto t_ws = Transpose(ws);
    for (const auto col : t_ws) {
        total_count += GetSubstrCount("XMAS", col);
        total_count += GetSubstrCount("SAMX", col);
    }

    for (int i { 0 }; i < ws.size() - 3; ++i) {
        for (int j { 0 }; j < ws[0].length() - 3; ++j) {
            const std::string word { ws[i][j], ws[i + 1][j + 1], ws[i + 2][j + 2], ws[i + 3][j + 3] };
            if (word == "XMAS" || word == "SAMX")
                total_count++;
        }
    }

    for (int i { 3 }; i < ws.size(); ++i) {
        for (int j { 0 }; j < ws[0].length() - 3; ++j) {
            const std::string word { ws[i][j], ws[i - 1][j + 1], ws[i - 2][j + 2], ws[i - 3][j + 3] };
            if (word == "XMAS" || word == "SAMX")
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
