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

ints ComputeSimilarityScores(ints list_a, ints list_b)
{
    ints result {};
    collections::Counter<int> appearance_counter {};

    for (int i { 0 }; i < list_a.size(); ++i)
        for (int j { 0 }; j < list_b.size(); ++j)
            if (list_a.at(i) == list_b.at(j))
                appearance_counter[list_a[i]] += 1;

    // remove duplicates from 'list_a'
    std::ranges::sort(list_a);
    auto last = std::ranges::unique(list_a);
    list_a.erase(std::begin(last), std::end(last));

    for (auto elem : list_a) {
        elem *= (appearance_counter[elem] > 0) ? appearance_counter[elem] : 0;
        result.push_back(elem);
    }

    return result;
}

int main()
{
    auto [ids_1, ids_2] = ParseInput("input.txt");

    auto similarity_scores = ComputeSimilarityScores(ids_1, ids_2);
    std::cout << std::accumulate(std::begin(similarity_scores), std::end(similarity_scores), 0) << std::endl;

    return 0;
}
