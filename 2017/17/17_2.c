#include <stdio.h>

int main() {
    /*
    It's a circular buffer, so when an insertion occurs at n, does it actually go on the end or
    does it get inserted before the beginning? Always the end. This in turn means that element 0
    will always be first, and we don't need to track any of the list contents.
    */
    const int pitch = 369;
    int pos=0, second;
    for (int value = 0; value <= 50000000; value++) {
        if (!pos)
            second = value;
        pos = (pos + pitch + 1) % (value + 1);
    }
    printf("Part 2: %d\n", second);  // 31154878
    return 0;
}
