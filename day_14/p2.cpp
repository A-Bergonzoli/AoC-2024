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

long CountRobots(const Grid& quadrant)
{
    long cnt = 0;

    for (const auto& row : quadrant)
        for (const auto& col : row)
            if (col != '.')
                cnt += col - '0';

    return cnt;
}

bool CheckAdjacencyAlongXAxis(Locations positions, int how_many)
{
    std::unordered_map<int, std::vector<int>> x_map {};

    for (const auto& [x, y] : positions)
        x_map[x].push_back(y);

    for (auto& [x, ys] : x_map) {
        if (ys.size() > how_many) {
            std::sort(ys.begin(), ys.end());

            auto count { 1 };
            for (std::size_t i { 1U }; i < ys.size(); ++i) {
                if (ys[i] - ys[i - 1] < 2)
                    count++;
                else
                    count = 1; // reset

                if (count > how_many)
                    return true;
            }
        }
    }

    return false;
}

int Compute(Locations positions, const Locations& velocities)
{
    auto num_seconds { 0 };

    // hacky search for easter egg
    for (std::size_t k { 1U }; k < 15000; ++k) {
        // update robots
        UpdateRobots(positions, velocities);

        // clear
        Grid tmp_grid(N, std::vector<char>(M, '.'));

        // update grid
        for (const auto& [i, j] : positions) {
            int count = std::count(positions.begin(), positions.end(), std::make_pair(i, j));
            if (count)
                tmp_grid[i][j] = '0' + count;
        }

        // hack
        if (CheckAdjacencyAlongXAxis(positions, 10)) {
            num_seconds = k;
            break;
        }
    }

    return num_seconds;
}

int main()
{
    auto [positions, velocities] = Parse("input.txt");
    std::cout << Compute(positions, velocities) << std::endl;

    return 0;
}
