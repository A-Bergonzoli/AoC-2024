#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>

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

std::vector<ints> generate_mutations(const ints& record)
{
    std::vector<ints> mutations;
    for (std::size_t i = 0; i < record.size(); ++i) {
        ints mutation;
        std::ranges::copy_if(record, std::back_inserter(mutation), [i, j = 0](int) mutable { return j++ != i; });
        mutations.push_back(std::move(mutation));
    }
    mutations.push_back(record); // original
    return mutations;
}

int Compute(const std::vector<ints>& records)
{
    int sum { 0 };

    for (const auto& record : records)
        if (std::ranges::any_of(generate_mutations(record), [](const ints& list) { return IsSafeByOrderAndDifference(list); }))
            sum++;

    return sum;
}

int main()
{
    auto records = ParseInput("input.txt");
    std::cout << Compute(records) << std::endl;

    return 0;
}
