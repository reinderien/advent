#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int N = 100;

int main() {
    const int
        memsize = sizeof(char)*((N+2)*(N+2)+1),
        ptrsize = sizeof(char*)*(N+2);
    char *block = (char*)malloc(memsize),
        *block2 = (char*)malloc(memsize),
        **state = (char**)malloc(ptrsize),
        **state2 = (char**)malloc(ptrsize);

    for (int y = 0; y < N+2; y++) {
        state[y] = block + (N+2)*y;
        state2[y] = block2 + (N+2)*y;
    }

    assert(block && block2 && state && state2);
    memset(block, 0, memsize);
    memset(block2, 0, memsize);

    FILE *fin = fopen("18.in", "r");
    assert(fin);
    for (int y = 1; y <= N; y++) {
        assert(fgets(state[y]+1, N+1, fin));
        char consume_newline[2];
        fgets(consume_newline, 2, fin);
        for (int x = 1; x <= N; x++)
            state[y][x] = state[y][x] == '#';
    }
    fclose(fin);

    for (int n = 0; n < 100; n++) {
        for (int y = 1; y <= N; y++) {
            for (int x = 1; x <= N; x++) {
                int n_others =
                    state[y-1][x-1] +
                    state[y-1][x  ] +
                    state[y-1][x+1] +
                    state[y  ][x-1] +
                    state[y  ][x+1] +
                    state[y+1][x-1] +
                    state[y+1][x  ] +
                    state[y+1][x+1];
                if (state[y][x])
                    state2[y][x] = n_others >= 2 && n_others <= 3;
                else state2[y][x] = n_others == 3;
            }
        }
        char **swap = state2;
        state2 = state;
        state = swap;
    }

    free(state2);
    free(block2);

    int total = 0;
    for (int y = 1; y <= N; y++)
        for (int x = 1; x <= N; x++)
            total += state[y][x];
    printf("%d\n", total);

    free(state);
    free(block);

    return 0;
}
