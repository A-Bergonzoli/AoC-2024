#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>

using int_pair = std::pair<int, int>;

strings Parse(const std::string& fname)
{
    return pypp::splitFileLines(fname);
}

std::vector<int_pair> GetTrailheads(const strings& grid)
{
    std::vector<int_pair> trailheads {};

    for (int row { 0 }; row < grid.size(); ++row)
        for (int col { 0 }; col < grid[0].length(); ++col)
            if (grid[row][col] == '0')
                trailheads.push_back(std::make_pair(row, col));

    return trailheads;
}

bool IsInBounds(const strings& grid, int coord_x, int coord_y)
{
    return 0 <= coord_x && coord_x < grid.size() && 0 <= coord_y && coord_y < grid[0].length();
}

std::vector<int_pair> GiveMoves(int x, int y)
{
    std::vector<int_pair> moves {};
    moves.emplace_back(x, y + 1); // Up
    moves.emplace_back(x, y - 1); // Down
    moves.emplace_back(x - 1, y); // Left
    moves.emplace_back(x + 1, y); // Right
    return moves;
}

int dp(const strings& grid, int row, int col, int current)
{
    // affirmative base case
    if (grid[row][col] == '9')
        return 1;

    auto result { 0 };
    current = static_cast<int>(grid[row][col]);

    for (auto [nrow, ncol] : GiveMoves(row, col))
        if (IsInBounds(grid, nrow, ncol))
            if (static_cast<int>(grid[nrow][ncol]) == current + 1)
                result += dp(grid, nrow, ncol, current);

    return result;
}

int Compute(const strings& grid)
{
    auto score { 0 };
    auto trailheads = GetTrailheads(grid);

    for (auto head : trailheads) {
        score += dp(grid, std::get<0>(head), std::get<1>(head), 0);
    }

    return score;
}

int main()
{
    auto grid = Parse("input.txt");
    std::cout << Compute(grid) << std::endl;

    return 0;
}
