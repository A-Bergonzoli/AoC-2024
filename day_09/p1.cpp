#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>
#include <optional>

std::vector<std::optional<int>> Parse(const std::string& fname)
{
    std::vector<std::optional<int>> memory {};
    auto line = pypp::splitFileLines(fname)[0];

    for (std::size_t i = 0U; i < line.size(); i += 2) {
        int ch_1 = line[i] - '0';
        int ch_2 = (i + 1 < line.size()) ? line[i + 1] - '0' : 0;

        memory.insert(memory.end(), ch_1, i / 2);
        memory.insert(memory.end(), ch_2, std::nullopt);
    }

    return memory;
}

std::optional<int> Pop(std::vector<std::optional<int>>& memory, size_t idx)
{
    if (memory.empty())
        return 0;

    auto last_space = memory.back();
    memory.pop_back();

    while (!last_space.has_value()) {
        if (memory.size() <= idx)
            return 0;

        last_space = memory.back();
        memory.pop_back();
    }

    return last_space;
}

std::uint64_t Compute(std::vector<std::optional<int>>& memory)
{
    std::uint64_t checksum = 0U;

    for (std::size_t i = 0U; i < memory.size(); ++i) {
        if (!memory[i].has_value())
            memory[i] = Pop(memory, i);

        checksum += i * memory[i].value_or(0);
    }

    return checksum;
}

int main()
{
    auto mem = Parse("input.txt");
    std::cout << Compute(mem) << std::endl;
    return 0;
}
