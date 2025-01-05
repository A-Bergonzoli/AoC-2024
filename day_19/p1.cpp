#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>

std::pair<strings, strings> Parse(const std::string& fname)
{
    strings towels {};
    strings designs {};
    auto lines = pypp::splitFileLines(fname);

    for (int i { 0 }; i < lines.size(); ++i) {
        if (i == 0)
            towels = pypp::split(lines[i], ',');
        else
            designs.push_back(lines[i]);
    }

    for (auto& t : towels)
        t = pypp::strip(t, [](unsigned char ch) { return std::isspace(ch); });

    return { towels, designs };
}

bool dp(const std::string& target, const strings& towels, std::unordered_map<std::string, bool>& memo)
{
    if (memo.contains(target))
        return memo[target];

    if (target.length() == 0)
        return true;

    for (auto t : towels) {
        if (target.find(t) == 0) {
            if (dp(target.substr(t.length()), towels, memo)) {
                memo[target] = true;
                return true;
            }
        }
    }

    memo[target] = false;
    return false;
}

int Compute(const strings& towels, const strings& designs)
{
    auto count { 0 };

    for (auto d : designs) {
        std::unordered_map<std::string, bool> memo {};
        if (dp(d, towels, memo))
            count++;
    }

    return count;
}

int main()
{
    const auto [towels, designs] = Parse("input.txt");
    std::cout << Compute(towels, designs) << std::endl;

    return 0;
}
