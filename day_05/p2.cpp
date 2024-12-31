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

ints ReorderByRule(const mmap& rules, ints update)
{
    if (update.size() == 1)
        return update;

    for (size_t i = 0; i < update.size() - 1; ++i) {
        auto key = std::to_string(update[i]);
        auto value = std::to_string(update[i + 1]);
        if (rules.find(key) != rules.end() && std::find(rules.at(key).begin(), rules.at(key).end(), update[i + 1]) != rules.at(key).end()) {
            std::swap(update[i], update[i + 1]);
            return ReorderByRule(rules, update);
        }
    }

    return update;
}

int Compute(const mmap& rules, const std::vector<ints>& updates)
{
    std::set<ints> bad_updates;

    for (const auto& update : updates) {
        for (std::size_t i { 1U }; i < update.size(); ++i) {
            auto page = update[update.size() - 1 - i];
            auto elem = gen(update, i);
            for (const auto& e : elem) {
                auto it = rules.find(std::to_string(e));
                if (it != rules.end() && std::find(it->second.begin(), it->second.end(), page) != it->second.end()) {
                    bad_updates.insert(update);
                }
            }
        }
    }

    std::vector<ints> bad_updates_list(bad_updates.begin(), bad_updates.end());

    for (auto& bad : bad_updates_list)
        bad = ReorderByRule(rules, bad);

    int sum = 0;
    for (const auto& bad : bad_updates_list)
        sum += bad[bad.size() / 2];

    return sum;
}

int main()
{
    auto [rules, updates] = Parse("input.txt");
    std::cout << Compute(rules, updates) << std::endl;

    return 0;
}
