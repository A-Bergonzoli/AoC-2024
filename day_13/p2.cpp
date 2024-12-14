#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <Eigen/Dense>
#include <gmpxx.h>
#include <iostream>
#include <unordered_map>

using namespace std;
using Config = unordered_map<string, pair<mpz_class, mpz_class>>;
using Configs = vector<Config>;

typedef Eigen::Matrix<mpf_class, 2, 2> Matrix2_128;
typedef Eigen::Matrix<mpf_class, 2, 1> Vector2_128;

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
        config["A"] = make_pair(mpz_class(ax_s), mpz_class(ay_s));

        auto bx_s = pypp::splitThenGetAt(lines[i + 1], ' ', 2);
        auto by_s = pypp::splitThenGetAt(lines[i + 1], ' ', 3);
        erase_if(bx_s, [](char ch) { return !isdigit(ch); });
        erase_if(by_s, [](char ch) { return !isdigit(ch); });
        config["B"] = make_pair(mpz_class(bx_s), mpz_class(by_s));

        auto px_s = pypp::splitThenGetAt(lines[i + 2], ' ', 1);
        auto py_s = pypp::splitThenGetAt(lines[i + 2], ' ', 2);
        erase_if(px_s, [](char ch) { return !isdigit(ch); });
        erase_if(py_s, [](char ch) { return !isdigit(ch); });
        config["prize"] = make_pair(mpz_class(px_s), mpz_class(py_s));
        config["prize"].first += 10000000000000UL;
        config["prize"].second += 10000000000000UL;
        configs.push_back(config);
    }

    return configs;
}

mpz_class Compute(const Configs& configs)
{
    vector<mpz_class> prices;

    for (const auto& config : configs) {
        Matrix2_128 coef_mat;
        coef_mat << config.at("A").first, config.at("B").first,
                    config.at("A").second, config.at("B").second;

        Vector2_128 knowns;
        knowns << config.at("prize").first, config.at("prize").second;

        Vector2_128 unknowns = coef_mat.inverse() * knowns;
        uint64_t cntA = round(unknowns[0].get_d());
        uint64_t cntB = round(unknowns[1].get_d());

        if (config.at("A").first * cntA + config.at("B").first * cntB == config.at("prize").first &&
            config.at("A").second * cntA + config.at("B").second * cntB == config.at("prize").second) {
            prices.push_back(3 * cntA + cntB);
        }
    }

    mpz_class total = 0;
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
