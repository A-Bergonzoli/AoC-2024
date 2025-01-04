#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>
#include <regex>

using Locations = std::vector<grid::Location>;
using Grid = std::vector<std::vector<char>>;

constexpr auto N { 103 };
constexpr auto M { 101 };
constexpr auto HALF_N { N / 2 };
constexpr auto HALF_M { M / 2 };

std::pair<Locations, Locations> Parse(const std::string& fname)
{
    Locations positions {};
    Locations velocities {};
    std::regex pattern("p=([-+]?\\d+),([-+]?\\d+) v=([-+]?\\d+),([-+]?\\d+)");
    std::smatch match {};

    const auto lines = pypp::splitFileLines(fname);
    for (const auto& line : lines) {
        if (std::regex_search(line, match, pattern)) {
            positions.emplace_back(std::stoi(match[2]), std::stoi(match[1]));
            velocities.emplace_back(std::stoi(match[4]), std::stoi(match[3]));
        }
    }

    return { positions, velocities };
}

grid::Location UpdateRobotsWithWrap(const grid::Location& pos, const grid::Location& vel)
{
    auto [cx, cy] = pos;
    auto [vx, vy] = vel;

    int nx = (cx + vx + N) % N;
    int ny = (cy + vy + M) % M;

    return { nx, ny };
}

Locations UpdateRobots(Locations& positions, const Locations& velocities)
{
    for (size_t i = 0; i < velocities.size(); ++i)
        positions[i] = UpdateRobotsWithWrap(positions[i], velocities[i]);

    return positions;
}

Grid Quadrant(const Grid& grid, int srow, int erow, int scol, int ecol)
{
    Grid quadrant {};

    for (int i = srow; i < erow; ++i)
        quadrant.push_back(std::vector<char>(grid[i].begin() + scol, grid[i].begin() + ecol));

    return quadrant;
};

long CountRobots(const Grid& quadrant)
{
    long cnt = 0;

    for (const auto& row : quadrant)
        for (const auto& col : row)
            if (col != '.')
                cnt += col - '0';

    return cnt;
}

int Compute(Locations positions, const Locations& velocities, int num_seconds)
{
    // empty grid
    Grid grid(N, std::vector<char>(M, '.'));

    // update robots
    for (int i = 0; i < num_seconds; ++i)
        UpdateRobots(positions, velocities);

    // update grid
    for (const auto& [i, j] : positions) {
        int count = std::count(positions.begin(), positions.end(), std::make_pair(i, j));
        if (count)
            grid[i][j] = '0' + count;
    }

    // get quadrants
    auto first = Quadrant(grid, 0, HALF_N, 0, HALF_M);
    auto second = Quadrant(grid, 0, HALF_N, HALF_M + 1, M);
    auto third = Quadrant(grid, HALF_N + 1, N, 0, HALF_M);
    auto fourth = Quadrant(grid, HALF_N + 1, N, HALF_M + 1, M);

    // compute safety factor
    int safety_factor = 1;
    for (const auto& quadrant : { first, second, third, fourth })
        safety_factor *= CountRobots(quadrant);

    return safety_factor;
}

int main()
{
    auto [positions, velocities] = Parse("input.txt");
    std::cout << Compute(positions, velocities, 100) << std::endl;

    return 0;
}
