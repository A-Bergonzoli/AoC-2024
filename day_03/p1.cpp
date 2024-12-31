#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>
#include <numeric>
#include <regex>

using Tuples = std::vector<std::pair<long, long>>;

std::string Parse(const std::string& fname)
{
    return pypp::splitFileLines(fname)[0];
}

long Compute(const std::string& input)
{
    std::regex operator_pattern(R"(mul\([0-9]{1,3},[0-9]{1,3}\))");
    std::regex operands_pattern(R"(mul\((\d+),(\d+)\))");

    std::sregex_iterator it(input.begin(), input.end(), operator_pattern);
    std::sregex_iterator end {};

    Tuples tuples {};

    while (it != end) {
        std::smatch match;
        auto match_str = it->str();
        std::regex_match(match_str, match, operands_pattern);
        tuples.emplace_back(std::stol(match[1].str()), std::stol(match[2].str()));
        ++it;
    }

    return std::accumulate(tuples.begin(), tuples.end(), 0,
        [](long sum, const std::pair<long, long>& p) { return sum + p.first * p.second; });
}

int main()
{
    auto input = Parse("input.txt");
    std::cout << Compute(input) << std::endl;

    return 0;
}
