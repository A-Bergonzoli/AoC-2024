#include "pypp.hpp" // https://github.com/A-Bergonzoli/pypp/tree/main

#include <iostream>

using Pi = std::pair<int, int>;

std::pair<std::unordered_map<int, Pi>, std::deque<Pi>> Parse(const std::string& fname)
{
    std::unordered_map<int, Pi> files {};
    std::deque<Pi> free_spaces {};

    auto line = pypp::splitFileLines(fname)[0];

    int f_id = 0;
    int mem_idx = 0;
    for (size_t idx = 0; idx < line.size(); ++idx) {
        char ch = line[idx];
        int length = ch - '0';

        if (idx % 2 && ch != '0') { // free space
            free_spaces.emplace_back(mem_idx, length);
        } else if (ch != '0') { // file
            files[f_id] = std::make_pair(mem_idx, length);
            f_id++;
        }
        mem_idx += length;
    }

    return { files, free_spaces };
}

std::uint64_t Compute(std::unordered_map<int, Pi>& files, std::deque<Pi>& free_spaces)
{
    for (int f_id = files.size() - 1; f_id >= 0; --f_id) {
        auto [f_start, f_len] = files[f_id];

        for (size_t fs_id = 0; fs_id < free_spaces.size(); ++fs_id) {
            auto [fs_start, fs_len] = free_spaces[fs_id];
            if (fs_start >= f_start) {
                break;
            } else if (fs_len >= f_len) {
                files[f_id] = std::make_pair(fs_start, f_len);

                if (fs_len == f_len) {
                    free_spaces.erase(free_spaces.begin() + fs_id);
                } else {
                    free_spaces[fs_id] = std::make_pair(fs_start + f_len, fs_len - f_len);
                }
                break;
            }
        }
    }

    std::uint64_t checksum = 0;
    for (const auto& [f_id, pos_len] : files) {
        auto [f_start, f_len] = pos_len;
        for (int j = 0; j < f_len; ++j)
            checksum += (f_start + j) * f_id;
    }

    return checksum;
}

int main()
{
    auto [files, free_spaces] = Parse("input.txt");
    std::cout << Compute(files, free_spaces) << std::endl;
    return 0;
}
