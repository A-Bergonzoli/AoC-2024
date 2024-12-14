#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <Eigen/Dense>
#include <iostream>
#include <unordered_map>

using namespace std;
using Config = unordered_map<string, pair<int, int>>;
using Configs = vector<Config>;

Configs Parse(const string& fname)
{
    Configs configs {};
    auto lines = pypp::splitFileLines(fname);

    for (int i { 0 }; i < lines.size(); i += 3) {
        Config config {};
        auto ax_s = pypp::splitThenGetAt(lines[i], ' ', 2);
        auto ay_s = pypp::splitThenGetAt(lines[i], ' ', 3);
        erase_if(ax_s, [](char ch) { return !isdigit(ch); });
        erase_if(ay_s, [](char ch) { return !isdigit(ch); });
        config["A"] = make_pair(stoi(ax_s), stoi(ay_s));

        auto bx_s = pypp::splitThenGetAt(lines[i + 1], ' ', 2);
        auto by_s = pypp::splitThenGetAt(lines[i + 1], ' ', 3);
        erase_if(bx_s, [](char ch) { return !isdigit(ch); });
        erase_if(by_s, [](char ch) { return !isdigit(ch); });
        config["B"] = make_pair(stoi(bx_s), stoi(by_s));

        auto px_s = pypp::splitThenGetAt(lines[i + 2], ' ', 1);
        auto py_s = pypp::splitThenGetAt(lines[i + 2], ' ', 2);
        erase_if(px_s, [](char ch) { return !isdigit(ch); });
        erase_if(py_s, [](char ch) { return !isdigit(ch); });
        config["prize"] = make_pair(stoi(px_s), stoi(py_s));
        configs.push_back(config);
    }

    return configs;
}

int Compute(const Configs& configs)
{
    vector<int> prices;

    for (const auto& config : configs) {
        Eigen::Matrix2i coef_mat;
        coef_mat << config.at("A").first, config.at("B").first,
                    config.at("A").second, config.at("B").second;

        Eigen::Vector2i knowns;
        knowns << config.at("prize").first, config.at("prize").second;

        Eigen::Vector2f unknowns = coef_mat.cast<float>().inverse() * knowns.cast<float>();
        int cntA = std::round(unknowns[0]);
        int cntB = std::round(unknowns[1]);

        if (config.at("A").first * cntA + config.at("B").first * cntB == config.at("prize").first &&
            config.at("A").second * cntA + config.at("B").second * cntB == config.at("prize").second) {
            prices.push_back(3 * cntA + cntB);
        }
    }

    int total = 0;
    for (auto price : prices)
        total += price;

    return total;
}

int main()
{
    const auto configs = Parse("input.txt");
    cout << Compute(configs) << endl;
    return 0;
}
