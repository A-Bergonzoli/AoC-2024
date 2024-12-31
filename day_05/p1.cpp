#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>
#include <unordered_map>

using strings = std::vector<std::string>;
using ints = std::vector<int>;
using mmap = std::unordered_map<std::string, ints>;

std::pair<mmap, std::vector<ints>> Parse(const std::string& fname)
{
    mmap rules {};
    std::vector<ints> updates {};
    const auto lines = pypp::splitFileLines(fname);

    for (const auto& line : lines) {
        if (line.find('|') != std::string::npos) { // rule
            const auto first = pypp::splitThenGetAt(line, '|', 0);
            const auto second = pypp::splitThenGetAt(line, '|', 1);
            rules[first].push_back(std::stoi(second));
        } else if (line.find(',') != std::string::npos) { // update
            auto updates_strings = pypp::split(line, ',');
            ints update {};
            std::ranges::transform(updates_strings,
                std::back_inserter(update),
                [](const std::string& s) { return std::stoi(s); });
            updates.push_back(update);
        }
    }

    return std::make_pair(rules, updates);
}

ints gen(const ints& lst, int idx)
{
    return ints(lst.end() - idx, lst.end());
}

int Compute(mmap& rules, std::vector<ints>& updates_list)
{
    std::set<ints> bad_updates {};
    std::set<ints> good_updates {};

    for (const auto& updates : updates_list) {
        for (std::size_t i { 0U }; i < updates.size(); ++i) {
            auto page = updates[updates.size() - 2 - i];
            auto elem = gen(updates, i + 1);

            for (const auto& e : elem) {
                auto it = rules.find(std::to_string(e));
                if (it != rules.end() && std::find(it->second.begin(), it->second.end(), page) != it->second.end())
                    bad_updates.insert(updates);
                else
                    good_updates.insert(updates);
            }
        }
    }

    for (const auto& updates : updates_list)
        good_updates.insert(updates);

    for (const auto& bad_update : bad_updates)
        good_updates.erase(bad_update);

    int sum = 0;
    for (const auto& good : good_updates)
        sum += good[good.size() / 2];

    return sum;
}

int main()
{
    auto [rules, updates] = Parse("input.txt");
    std::cout << Compute(rules, updates) << std::endl;

    return 0;
}
