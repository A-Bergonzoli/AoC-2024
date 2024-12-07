#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>

using namespace std;
using longs = vector<long long>;

pair<longs, vector<longs>> parse(const string& fname)
{
    longs values {};
    vector<longs> operands {};
    const auto lines = pypp::splitFileLines(fname);

    for (const auto& line : lines) {
        values.push_back(stoll(pypp::splitThenGetAt(line, ':', 0)));
        auto rest = pypp::splitThenGetAt(line, ':', 1);

        longs tmp {};
        for (const auto elem : pypp::split(rest, ' '))
            tmp.push_back(stoi(elem));

        operands.push_back(tmp);
    }

    return make_pair(values, operands);
}

long long perform(long long op1, string op, long long op2)
{
    if (op == "+")
        return op1 + op2;
    if (op == "*")
        return op1 * op2;
    if (op == "||")
        return stoll(to_string(op1) + to_string(op2));
}

bool dp(long long target, longs& operands, string op)
{
    // base case
    if (operands.size() == 1)
        return operands.front() == target;

    for (auto operand : operands) {
        vector<long long> new_operands {};
        if (op != "") {
            auto new_operand = perform(operands.at(0), op, operands.at(1));
            new_operands = vector<long long>(operands.begin() + 1, operands.end());
            new_operands.at(0) = new_operand;
        } else
            new_operands = operands;

        return dp(target, new_operands, "+") || dp(target, new_operands, "*") || dp(target, new_operands, "||");
    }

    return false;
}

long long compute(longs values, vector<longs>& operands)
{
    long long result { 0 };
    unordered_set<int> valid_indexes {};

    for (int i { 0 }; i < values.size(); ++i)
        if (dp(values[i], operands[i], ""))
            valid_indexes.insert(i);

    for (auto idx : valid_indexes)
        result += values.at(idx);

    return result;
}

int main()
{
    auto [values, operands] = parse("input.txt");
    std::cout << compute(values, operands);

    return 0;
}
