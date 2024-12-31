#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>
#include <set>

strings Parse(const std::string& fname)
{
    return pypp::splitFileLines(fname);
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

bool IsDone(const strings& grid, int x, int y)
{
    auto upper_bound { 0 };
    auto left_bound { 0 };
    auto lower_bound = grid.size() - 1;
    auto right_bound = grid[0].length() - 1;

    auto x_allowed = upper_bound <= x && x <= lower_bound;
    auto y_allowed = left_bound <= y && y <= right_bound;

    if (!x_allowed || !y_allowed)
        return true;

    return (x == upper_bound || x == lower_bound || y == left_bound || y == right_bound) && grid[x][y] != '#';
}

int Compute(const strings& grid)
{
    std::set<char> possibilities { '^', '>', 'v', '<' };
    auto guard_x { 0 };
    auto guard_y { 0 };
    auto prev_x { 0 };
    auto prev_y { 0 };
    auto guard_hdg { '^' };

    for (int i { 0 }; i < grid.size(); ++i)
        for (int j { 0 }; j < grid[0].length(); ++j)
            if (possibilities.find(grid[i][j]) != possibilities.end()) {
                guard_x = i;
                guard_y = j;
                break;
            }

    collections::Counter<std::pair<int, int>, collections::TupleHash> c {};
    c[std::make_pair(guard_x, guard_y)] = 1;

    while (!IsDone(grid, guard_x, guard_y)) {

        if (grid[guard_x][guard_y] == '#') {
            guard_hdg = RotateRight(guard_hdg);
            c[std::make_pair(guard_x, guard_y)] -= 1;
            guard_x = prev_x;
            guard_y = prev_y;
        }

        prev_x = guard_x;
        prev_y = guard_y;

        if (guard_hdg == '^')
            guard_x -= 1;
        if (guard_hdg == '>')
            guard_y += 1;
        if (guard_hdg == 'v')
            guard_x += 1;
        if (guard_hdg == '<')
            guard_y -= 1;

        c[std::make_pair(guard_x, guard_y)] += 1;
    }

    auto sum { 0 };
    auto [first, last] = c.values();
    for (; first != last; ++first)
        if (*first > 0)
            sum++;

    return sum;
}

int main()
{
    auto grid = Parse("input.txt");
    std::cout << Compute(grid) << std::endl;

    return 0;
}
