#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>
#include <numeric>

using ints = std::vector<int>;

std::pair<ints, ints> ParseInput(const std::string& fname)
{
    const auto lines = pypp::splitFileLines(fname);

    ints first_ids {};
    ints second_ids {};
    first_ids.reserve(lines.size());
    second_ids.reserve(lines.size());

    for (const auto& line : lines) {
        first_ids.push_back(std::stoi(pypp::splitThenGetAt(line, ' ', 0)));
        second_ids.push_back(std::stoi(pypp::splitThenGetAt(line, ' ', 1)));
    }

    return { first_ids, second_ids };
}

ints ComputeDistances(ints list_a, ints list_b)
{
    ints result {};
    std::ranges::sort(list_a);
    std::ranges::sort(list_b);

    for (int i { 0 }; i < list_a.size(); ++i)
        result.push_back(std::abs(list_a.at(i) - list_b.at(i)));

    return result;
}

int main()
{
    auto [ids_1, ids_2] = ParseInput("input.txt");

    const auto distances { ComputeDistances(ids_1, ids_2) };
    std::cout << std::accumulate(std::begin(distances), std::end(distances), 0) << std::endl;

    return 0;
}
