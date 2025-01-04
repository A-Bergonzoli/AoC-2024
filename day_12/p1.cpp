#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>
#include <unordered_set>

strings Parse(const std::string& fname)
{
    return pypp::splitFileLines(fname);
}

int CountBorders(const strings& grid, int x, int y)
{
    auto count { 0 };

    for (const auto& [dx, dy] : grid::move()) {
        const auto nx = x + dx;
        const auto ny = y + dy;

        if (grid::inBounds(grid, nx, ny)) {
            if (grid[nx][ny] != grid[x][y])
                count++;
        } else
            count++;
    }

    return count;
}

std::unordered_map<char, std::vector<std::vector<grid::Location>>> RegionsOf(const strings& grid)
{
    const auto n = grid.size();
    const auto m = grid[0].length();

    std::unordered_map<char, std::vector<std::vector<grid::Location>>> regions_map {};
    std::unordered_set<grid::Location, collections::TupleHash> visited {};
    for (std::size_t i { 0U }; i < n; ++i) {
        for (std::size_t j { 0U }; j < m; ++j) {
            if (visited.find({ i, j }) == visited.end()) {
                const auto label = grid[i][j];
                const grid::Location start = { i, j };
                auto condition = [&label](const char ch) { return ch == label; };
                const auto locations = algorithms::dfs(grid, start, condition, visited);
                regions_map[label];
                if (!locations.empty())
                    regions_map[label].push_back(locations);
            }
        }
    }

    return regions_map;
}

long Price(const strings& grid, const std::unordered_map<char, std::vector<std::vector<grid::Location>>>& regions_map)
{
    auto price { 0 };

    for (const auto [label, locations_list] : regions_map) {
        for (const auto locations : locations_list) {
            const auto area = locations.size();
            auto perimeter { 0 };
            for (const auto [x, y] : locations)
                perimeter += CountBorders(grid, x, y);
            price += area * perimeter;
        }
    }

    return price;
}

long Compute(const strings& grid)
{
    const auto regions_map = RegionsOf(grid);
    return Price(grid, regions_map);
}

int main()
{
    const auto grid = Parse("input.txt");
    std::cout << Compute(grid) << std::endl;

    return 0;
}
