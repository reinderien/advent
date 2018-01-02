#include <stdio.h>

int main() {
    int h = 0;

    for (int b = 106700; b != 123700; b += 17) {
        for (int d = 2; d != b; d++) {
            for (int e = 2; e != b; e++) {
                if (d*e == b) {
                    h++;
                    goto cont;
                }
            }
        }
        cont:
    }

    printf("b=%d h=%d\n", b, h);
    return 0;
}
