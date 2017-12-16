#include <assert.h>
#include <stdint.h>
#include <stdio.h>

int p1(uint32_t a, uint32_t b) {
    int matches = 0;
    for (int i = 0; i < 40000000; i++) {
        a = 16807ul*a % 0x7FFFFFFF;
        b = 48271ul*b % 0x7FFFFFFF;
        matches += (a&0xFFFF) == (b&0xFFFF);
    }
    return matches;
}

int main() {
    assert(p1(65, 8921) == 588);
    printf("Part 1: %d\n", p1(618, 814));
    return 0;
}
