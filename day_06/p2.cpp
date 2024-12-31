#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>
#include <set>
#include <tuple>
#include <vector>

std::vector<std::vector<char>> Parse(const std::string& fname)
{
    std::vector<std::vector<char>> grid {};
    auto lines = pypp::splitFileLines(fname);

    for (auto& line : lines) {
        std::vector<char> tmp(line.begin(), line.end());
        grid.push_back(tmp);
    }

    return grid;
}

char RotateRight(const char guard)
{
    if (guard == '^')
        return '>';
    else if (guard == '>')
        return 'v';
    else if (guard == 'v')
        return '<';
    else if (guard == '<')
        return '^';
}

bool IsDone(const std::vector<std::vector<char>>& grid, int x, int y)
{
    auto upper_bound { 0 };
    auto left_bound { 0 };
    auto lower_bound = grid.size() - 1;
    auto right_bound = grid[0].size() - 1;

    auto x_allowed = upper_bound <= x && x <= lower_bound;
    auto y_allowed = left_bound <= y && y <= right_bound;

    if (!x_allowed || !y_allowed)
        return true;

    return (x == upper_bound || x == lower_bound || y == left_bound || y == right_bound) && grid[x][y] != '#';
}

bool InRange(const std::vector<std::vector<char>>& grid, int x, int y)
{
    auto n = grid.size();
    auto m = grid[0].size();

    return 0 <= x && x < n && 0 <= y && y < m;
}

int Compute(std::vector<std::vector<char>>& grid)
{
    std::set<char> possibilities { '^', '>', 'v', '<' };
    auto guard_x { 0 };
    auto guard_y { 0 };
    auto prev_x { 0 };
    auto prev_y { 0 };
    auto guard_hdg { '^' };
    auto cnt { 0 };

    for (int i { 0 }; i < grid.size(); ++i)
        for (int j { 0 }; j < grid[0].size(); ++j)
            if (possibilities.find(grid[i][j]) != possibilities.end()) {
                guard_x = i;
                guard_y = j;
                break;
            }

    for (int ox { 0 }; ox < grid.size(); ++ox) {
        std::cout << "Currently on line :" << ox << "\n";
        for (int oy { 0 }; oy < grid[0].size(); ++oy) {
            if (grid[ox][oy] == '#' || grid[ox][oy] == '^')
                continue;

            grid[ox][oy] = '#';
            auto cx = guard_x;
            auto cy = guard_y;
            auto dir = grid[cx][cy];
            std::set<std::tuple<int, int, char>> seen {};

            while (InRange(grid, cx, cy) && seen.find(std::make_tuple(cx, cy, dir)) == seen.end()) {
                seen.insert(std::make_tuple(cx, cy, dir));

                while (true) {
                    auto nx = cx;
                    auto ny = cy;
                    if (dir == '^')
                        nx -= 1;
                    if (dir == '>')
                        ny += 1;
                    if (dir == 'v')
                        nx += 1;
                    if (dir == '<')
                        ny -= 1;

                    if (InRange(grid, nx, ny) && grid[nx][ny] == '#')
                        dir = RotateRight(dir);
                    else {
                        cx = nx;
                        cy = ny;
                        break;
                    }
                }
            }

            if (seen.find(std::make_tuple(cx, cy, dir)) != seen.end())
                cnt += 1;

            grid[ox][oy] = '.';
        }
    }

    return cnt;
}

int main()
{
    auto grid = Parse("input.txt");
    std::cout << Compute(grid) << std::endl;

    return 0;
}
