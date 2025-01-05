#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>

constexpr auto TARGET_COST { 105508 };

struct Move {
    int dx;
    int dy;
    grid::Direction hdg;
};

strings Parse(const std::string& fname)
{
    return pypp::splitFileLines(fname);
}

std::array<std::pair<Move, int>, 4U> Generator(grid::Direction hdg)
{
    std::array<std::pair<Move, int>, 4U> moves;
    const Move standard_moves[] = {
        { -1, 0, grid::Direction::UP },
        { 1, 0, grid::Direction::DOWN },
        { 0, 1, grid::Direction::RIGHT },
        { 0, -1, grid::Direction::LEFT }
    };

    for (std::size_t i { 0U }; i < moves.size(); ++i) {
        auto candidate = standard_moves[i];
        auto cost = 1;
        if (hdg != standard_moves[i].hdg) {
            candidate.dx = 0;
            candidate.dy = 0;
            cost = 1000;
        }
        moves[i] = std::make_pair(candidate, cost);
    }

    return moves;
}

int Compute(const strings& grid)
{
    int n = grid.size(), m = grid[0].length();
    grid::LocationWithHeading start(0, 0, grid::Direction::RIGHT);
    grid::Location end(0, 0);

    for (std::size_t i { 0U }; i < n; ++i) {
        for (std::size_t j { 0U }; j < m; ++j) {
            if (grid[i][j] == 'S')
                start = std::make_tuple(i, j, grid::Direction::RIGHT);
            else if (grid[i][j] == 'E')
                end = std::make_pair(i, j);
        }
    }

    auto [min_score, visited, best_paths] = algorithms::dijkstra_extended(grid, start, end, Generator, TARGET_COST);

    std::unordered_set<grid::Location, collections::TupleHash> unique_tiles {};
    for (auto path : best_paths) {
        for (auto elem : path)
            unique_tiles.insert({ std::get<0>(elem), std::get<1>(elem) });
    }

    return unique_tiles.size();
}

int main()
{
    const auto grid = Parse("input.txt");
    std::cout << Compute(grid) << std::endl;

    return 0;
}
