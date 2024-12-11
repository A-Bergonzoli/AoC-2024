#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>
#include <unordered_map>

using Memo = std::unordered_map<std::tuple<uint64_t, int>, uint64_t, collections::TupleHash>;

std::vector<uint64_t> Parse(const std::string& fname)
{
    auto line = pypp::split(pypp::splitFileLines(fname)[0], ' ');

    std::vector<uint64_t> line_longlong(line.size());
    std::ranges::transform(line.begin(),
        line.end(),
        line_longlong.begin(),
        [](const std::string& str) { return std::stoll(str); });

    return line_longlong;
}

uint64_t dp(uint64_t stone, int num_calls, Memo& memo)
{
    const auto key = std::make_tuple(stone, num_calls);
    if (memo.find(key) != memo.end())
        return memo[key];

    if (num_calls == 0)
        return 1;

    uint64_t result { 0 };

    if (stone == 0)
        result = dp(1, num_calls - 1, memo);

    else if ((std::to_string(stone)).length() % 2 == 0) {
        const auto stone_s = std::to_string(stone);
        const auto half = static_cast<int>(stone_s.length() / 2);
        const auto first = std::stoll(stone_s.substr(0, half));
        const auto second = std::stoll(stone_s.substr(half));
        result = dp(first, num_calls - 1, memo) + dp(second, num_calls - 1, memo);
    }

    else
        result = dp(stone * 2024, num_calls - 1, memo);

    memo[key] = result;
    return result;
}

int main()
{
    auto stones = Parse("input.txt");

    uint64_t result {};
    for (auto stone : stones) {
        Memo memo {};
        result += dp(stone, 25, memo);
    }

    std::cout << result << std::endl;

    return 0;
}
