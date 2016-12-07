#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void parse(char *buffer, int *x0, int *y0, int *x1, int *y1) {
    char *rest;
    for (rest = buffer; *rest < '0' || *rest > '9'; rest++);
    rest[-1] = '\0';
    assert(4 == sscanf(rest, "%d,%d through %d,%d", x0,y0,x1,y1));
}

// 377891
static int p1(FILE *f) {
    bool **lights = (bool**)malloc(1000*sizeof(bool*)),
        *lightblock = (bool*)malloc(1000*1000*sizeof(bool));
    memset(lightblock, false, 1000*1000*sizeof(bool));
    for (int y = 0; y < 1000; y++)
        lights[y] = lightblock + y*1000;

    char buffer[64];
    while (fgets(buffer, sizeof(buffer), f)) {
        const char *action = buffer;
        int x0,y0,x1,y1;
        parse(buffer, &x0, &y0, &x1, &y1);

        if (!strcmp(action, "turn on"))
            for (int y = y0; y <= y1; y++)
                memset(lights[y]+x0, true, x1-x0+1);
        else if (!strcmp(action, "turn off"))
            for (int y = y0; y <= y1; y++)
                memset(lights[y]+x0, false, x1-x0+1);
        else for (int y = y0; y <= y1; y++)
            for (int x = x0; x <= x1; x++)
                lights[y][x] ^= 1;
    }

    int count = 0;
    for (int y = 0; y < 1000; y++)
        for (int x = 0; x < 1000; x++)
            count += lights[y][x];

    free(lightblock);
    free(lights);
    return count;
}

// 14110788
static int p2(FILE *f) {
    int **lights = (int**)malloc(1000*sizeof(int*)),
        *lightblock = (int*)malloc(1000*1000*sizeof(int));
    memset(lightblock, 0, 1000*1000*sizeof(int));
    for (int y = 0; y < 1000; y++)
        lights[y] = lightblock + y*1000;

    char buffer[64];
    while (fgets(buffer, sizeof(buffer), f)) {
        const char *action = buffer;
        int x0,y0,x1,y1;
        parse(buffer, &x0, &y0, &x1, &y1);

        if (!strcmp(action, "turn on"))
            for (int y = y0; y <= y1; y++)
                for (int x = x0; x <= x1; x++)
                    lights[y][x]++;
        else if (!strcmp(action, "turn off")) {
            for (int y = y0; y <= y1; y++) {
                for (int x = x0; x <= x1; x++) {
                    int l = lights[y][x];
                    l--;
                    if (l < 0) l = 0;
                    lights[y][x] = l;
                }
            }
        }
        else for (int y = y0; y <= y1; y++)
            for (int x = x0; x <= x1; x++)
                lights[y][x] += 2;
    }

    int count = 0;
    for (int y = 0; y < 1000; y++)
        for (int x = 0; x < 1000; x++)
            count += lights[y][x];

    free(lightblock);
    free(lights);
    return count;
}

int main() {
    FILE *f = fopen("6.in", "r");
    assert(f);

    printf("%d\n", p2(f));

    assert(!fclose(f));

    return 0;
}
