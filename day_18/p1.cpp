#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>

constexpr auto NROWS { 71 };
constexpr auto NCOLS { 71 };

struct Move {
    int dx;
    int dy;
    grid::Direction hdg;
};

std::vector<std::pair<int, int>> Parse(const std::string& fname)
{
    std::vector<std::pair<int, int>> coordinates {};
    auto lines = pypp::splitFileLines(fname);

    for (auto line : lines) {
        const auto y = pypp::splitThenGetAt(line, ',', 0);
        const auto x = pypp::splitThenGetAt(line, ',', 1);
        coordinates.push_back({ std::stoi(x), std::stoi(y) });
    }

    return coordinates;
}

std::array<std::pair<Move, int>, 4U> Generator(grid::Direction hdg)
{
    return {
        std::make_pair(Move { -1, 0, grid::Direction::NONE }, 1),
        std::make_pair(Move { +1, 0, grid::Direction::NONE }, 1),
        std::make_pair(Move { 0, +1, grid::Direction::NONE }, 1),
        std::make_pair(Move { 0, -1, grid::Direction::NONE }, 1)
    };
}

int Compute(const std::vector<std::pair<int, int>>& coords, int num_bytes)
{
    strings grid(NROWS, std::string(NCOLS, '.'));

    std::unordered_set<std::pair<int, int>, collections::TupleHash> coords_to_consider {};
    for (int i { 0 }; i < num_bytes; ++i)
        coords_to_consider.insert({ coords[i].first, coords[i].second });

    for (std::size_t i { 0U }; i < NROWS; ++i)
        for (std::size_t j { 0U }; j < NCOLS; ++j)
            if (coords_to_consider.contains({ i, j }))
                grid[i][j] = '#';

    const auto start = std::make_tuple(0, 0, grid::Direction::RIGHT);
    const auto end = std::make_pair(NROWS - 1, NCOLS - 1);

    auto [min_score, _] = algorithms::dijkstra(grid, start, end, Generator);
    return min_score;
}

int main()
{
    const auto coords = Parse("input.txt");
    std::cout << Compute(coords, 1024) << std::endl;

    return 0;
}
