#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>
#include <numeric>

using ints = std::vector<int>;

std::vector<ints> ParseInput(const std::string& fname)
{
    std::vector<ints> records {};
    const auto lines = pypp::splitFileLines(fname);

    for (const auto& line : lines) {
        ints record {};
        auto record_str = pypp::split(line, ' ');

        std::ranges::transform(record_str,
            std::back_inserter(record),
            [](const std::string& s) { return std::stoi(s); });

        records.push_back(record);
    }

    return records;
}

bool IsSafeByOrderAndDifference(const ints& record)
{
    ints diffs {};

    for (const auto& tuple : pypp::zip(record.begin() + 1, record.end(), record.begin()))
        diffs.push_back(std::get<1>(tuple) - std::get<0>(tuple));

    return std::ranges::all_of(diffs, [](const int diff) { return 1 <= diff && diff <= 3; })
        || std::ranges::all_of(diffs, [](const int diff) { return -3 <= diff && diff <= -1; });
}

int Compute(const std::vector<ints>& records)
{
    return std::accumulate(
        records.begin(),
        records.end(),
        0,
        [](int sum, const ints& record) { return sum + IsSafeByOrderAndDifference(record); });
}

int main()
{
    auto records = ParseInput("input.txt");
    std::cout << Compute(records) << std::endl;

    return 0;
}
