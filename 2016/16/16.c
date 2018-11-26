#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define DISK_BITS 272
#define DISK_QUADS (DISK_BITS/64 + 1)


typedef struct
{
    unsigned len;
    uint64_t data[DISK_QUADS];
} Fill;

static void init_fill(Fill *restrict f, const char *restrict input)
{
    const char *c = input;
    for (uint64_t *data = f->data;; data++)
    {
        *data = 0;
        for (uint64_t b = 1; b; b <<= 1)
        {
            if (!*c)
                return;
            if (*c == '1')
                *data |= b;
            f->len++;
            c++;
        }
    }
}

int main()
{
    Fill fill;
    const char *input = "10001001100000001";
    init_fill(&fill, input);

    printf("Disk bits: %u\n", DISK_BITS);
    printf("Disk quads: %u\n", DISK_QUADS);
    printf("Initial binary: %s\n", input);
    printf("Initial bits: %u\n", fill.len);



    return 0;
}