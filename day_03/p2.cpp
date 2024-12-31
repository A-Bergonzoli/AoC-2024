#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>
#include <numeric>
#include <regex>

using Tuples = std::vector<std::pair<long, long>>;

std::string Parse(const std::string& fname)
{
    return pypp::splitFileLines(fname)[0];
}

bool IsEnabled(size_t match_start, const std::vector<std::smatch>& controls)
{
    auto is_enabled { true };

    for (const auto& control : controls)
        if (control.position(0) < match_start)
            is_enabled = (control.str(0) == "do()") ? true : false;

    return is_enabled;
}

long Compute(const std::string& input)
{
    std::regex operator_pattern(R"(mul\([0-9]{1,3},[0-9]{1,3}\))");
    std::regex operands_pattern(R"(mul\((\d+),(\d+)\))");
    std::regex control_pattern(R"(do\(\)|don't\(\))");

    std::sregex_iterator it(input.begin(), input.end(), operator_pattern);
    std::sregex_iterator end {};

    strings matched_instructions {};
    while (it != end) {
        matched_instructions.push_back(it->str());
        ++it;
    }

    std::sregex_iterator control_it(input.begin(), input.end(), control_pattern);
    std::vector<std::smatch> controls;
    while (control_it != end) {
        controls.push_back(*control_it);
        ++control_it;
    }

    strings enabled_instructions;
    for (const auto& instr : matched_instructions) {
        if (IsEnabled(input.find(instr), controls)) {
            enabled_instructions.push_back(instr);
        }
    }

    Tuples tuples {};
    for (const auto& instr : enabled_instructions) {
        std::smatch match;
        if (std::regex_match(instr, match, operands_pattern))
            tuples.emplace_back(std::stoi(match[1].str()), std::stoi(match[2].str()));
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
