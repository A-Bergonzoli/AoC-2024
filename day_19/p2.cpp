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

long dp(const std::string& target, const strings& towels, std::unordered_map<std::string, long>& memo)
{
    if (memo.contains(target))
        return memo[target];

    if (target.length() == 0)
        return 1;

    long num { 0L };
    for (auto t : towels)
        if (target.find(t) == 0)
            num += dp(target.substr(t.length()), towels, memo);

    memo[target] = num;
    return num;
}

long Compute(const strings& towels, const strings& designs)
{
    long count { 0 };

    for (auto d : designs) {
        std::unordered_map<std::string, long> memo;
        count += dp(d, towels, memo);
    }

    return count;
}

int main()
{
    const auto [towels, designs] = Parse("input.txt");
    std::cout << Compute(towels, designs) << std::endl;

    return 0;
}
