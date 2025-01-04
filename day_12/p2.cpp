#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>
#include <unordered_set>

strings Parse(const std::string& fname)
{
    return pypp::splitFileLines(fname);
}

int CountCorners(const strings& grid, int x, int y)
{
    std::unordered_set<grid::Direction> adj {};

    for (const auto& [delta, dir] : grid::moveWithDIR()) {
        const auto [dx, dy] = delta;
        const auto nx = x + dx;
        const auto ny = y + dy;

        if (grid::inBounds(grid, nx, ny))
            if (grid[nx][ny] == grid[x][y])
                adj.insert(dir);
    }

    // clang-format off
    if (adj.size() == 1)
        return 2;

    if (adj.size() == 2) {
        // opposite ud or lp
        if ((adj.contains(grid::Direction::UP) && adj.contains(grid::Direction::DOWN)) ||
            (adj.contains(grid::Direction::LEFT) && adj.contains(grid::Direction::RIGHT)))
            return 0;

        // corner ul, ur, dl or dr
        if (adj.contains(grid::Direction::UP) && adj.contains(grid::Direction::LEFT)) {
            int nx =  x - 1, ny =  y - 1;
            if (grid::inBounds(grid, nx, ny) && grid[nx][ny] != grid[x][y])
                return 2;
            return 1;
        }
        else if (adj.contains(grid::Direction::UP) && adj.contains(grid::Direction::RIGHT)) {
            int nx =  x - 1, ny =  y + 1;
            if (grid::inBounds(grid, nx, ny) && grid[nx][ny] != grid[x][y])
                return 2;
            return 1;
        }
        else if (adj.contains(grid::Direction::DOWN) && adj.contains(grid::Direction::LEFT)) {
            int nx =  x + 1, ny =  y - 1;
            if (grid::inBounds(grid, nx, ny) && grid[nx][ny] != grid[x][y])
                return 2;
            return 1;
        }
        else if (adj.contains(grid::Direction::DOWN) && adj.contains(grid::Direction::RIGHT)) {
            int nx =  x + 1, ny =  y + 1;
            if (grid::inBounds(grid, nx, ny) && grid[nx][ny] != grid[x][y])
                return 2;
            return 1;
        }
    }

    if (adj.size() == 3) {
        // T-shapes ulr, dlr, uld, urd
        if (adj.contains(grid::Direction::UP) && adj.contains(grid::Direction::LEFT) && adj.contains(grid::Direction::RIGHT)) {
            int nx1 = x - 1, ny1 =  y - 1;
            int nx2 = x - 1, ny2 =  y + 1;
            auto num_corners{0};
            if (grid::inBounds(grid, nx1, ny1) && grid[nx1][ny1] != grid[x][y])
                num_corners++;
            if (grid::inBounds(grid, nx2, ny2) && grid[nx2][ny2] != grid[x][y])
                num_corners++;
            return num_corners;
        }
        if (adj.contains(grid::Direction::DOWN) && adj.contains(grid::Direction::LEFT) && adj.contains(grid::Direction::RIGHT)) {
            int nx1 = x + 1, ny1 =  y - 1;
            int nx2 = x + 1, ny2 =  y + 1;
            auto num_corners{0};
            if (grid::inBounds(grid, nx1, ny1) && grid[nx1][ny1] != grid[x][y])
                num_corners++;
            if (grid::inBounds(grid, nx2, ny2) && grid[nx2][ny2] != grid[x][y])
                num_corners++;
            return num_corners;
        }
        if (adj.contains(grid::Direction::LEFT) && adj.contains(grid::Direction::UP) && adj.contains(grid::Direction::DOWN)) {
            int nx1 = x - 1, ny1 =  y - 1;
            int nx2 = x + 1, ny2 =  y - 1;
            auto num_corners{0};
            if (grid::inBounds(grid, nx1, ny1) && grid[nx1][ny1] != grid[x][y])
                num_corners++;
            if (grid::inBounds(grid, nx2, ny2) && grid[nx2][ny2] != grid[x][y])
                num_corners++;
            return num_corners;
        }
        if (adj.contains(grid::Direction::RIGHT) && adj.contains(grid::Direction::UP) && adj.contains(grid::Direction::DOWN)) {
            int nx1 = x - 1, ny1 =  y + 1;
            int nx2 = x + 1, ny2 =  y + 1;
            auto num_corners{0};
            if (grid::inBounds(grid, nx1, ny1) && grid[nx1][ny1] != grid[x][y])
                num_corners++;
            if (grid::inBounds(grid, nx2, ny2) && grid[nx2][ny2] != grid[x][y])
                num_corners++;
            return num_corners;
        }
    }
    
    if (adj.size() == 4) {
        int nx1 =  x - 1, ny1 =  y - 1;
        int nx2 =  x - 1, ny2 =  y + 1;
        int nx3 =  x + 1, ny3 =  y - 1;
        int nx4 =  x + 1, ny4 =  y + 1;
        auto num_corners{0};

        if (grid::inBounds(grid, nx1, ny1) && grid[nx1][ny1] != grid[x][y])
            num_corners++;
        if (grid::inBounds(grid, nx2, ny2) && grid[nx2][ny2] != grid[x][y])
            num_corners++;
        if (grid::inBounds(grid, nx3, ny3) && grid[nx3][ny3] != grid[x][y])
            num_corners++;
        if (grid::inBounds(grid, nx4, ny4) && grid[nx4][ny4] != grid[x][y])
            num_corners++;

        return num_corners;
    }

    // clang-format on

    return 4;
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
                perimeter += CountCorners(grid, x, y);
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
    const auto grid = Parse("toy_input.txt");
    std::cout << Compute(grid) << std::endl;

    return 0;
}
