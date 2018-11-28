#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


typedef uint8_t Word;
#define WORD_BYTES (sizeof(Word))
#define WORD_BITS (8*WORD_BYTES)

typedef struct
{
    char *last;
    unsigned total_safe;
} Result;

static Word *init(const char *input, unsigned nbytes)
{
    Word *row = malloc(nbytes);
    memset(row, 0, nbytes);
    const char *c = input;
    for (Word *d = row;; d++)
    {
        for (unsigned b = 0; b < WORD_BITS; b++)
        {
            if (!*c)
                return row;
            Word bit = *c == '^';
            *d |= bit << b;
            c++;
        }
    }
}

static unsigned count(const Word *row, unsigned nbits)
{
    unsigned btot = 0, sum = 0;
    for (const Word *pd = row;; pd++)
    {
        for (Word b = 1; b; b <<= 1)
        {
            sum += !(*pd & b);
            if (++btot >= nbits)
                return sum;
        }
    }
}

static void evolve(Word *row, unsigned nwords)
{
    // lsb       msb
    // L xxxx_xxxx R
    // a aaaa_aaa
    //    bbb_bbbb b

    Word lcarry = 0;
    unsigned i;
    for (i = 0; i < nwords-1; i++)
    {
        Word rcarry = row[i+1] << (WORD_BITS-1),
             next_lcarry = row[i] >> (WORD_BITS-1);
        row[i] = (lcarry | (row[i] >> 1)) ^
                 (rcarry | (row[i] << 1));
        lcarry = next_lcarry;
    }

    row[i] = (lcarry | (row[i] >> 1)) ^
             (row[i] << 1);
}

static void pretty_bin(const Word *row, unsigned nbits)
{
    unsigned i = 0;
    for (const Word *d = row;; d++)
    {
        for (unsigned b = 0; b < WORD_BITS; b++)
        {
            if (i++ >= nbits)
            {
                putchar('\n');
                return;
            }
            putchar('0' + ((*d >> b) & 1));
            if ((b % 4) == 3)
                putchar('_');
        }
        putchar(' ');
    }
}

static Result run(const char *input, unsigned nrows)
{
    unsigned nbits = strlen(input),
             nwords = nbits/WORD_BITS + 1,
             nbytes = nwords * WORD_BYTES;

    Word *row = init(input, nbytes);
    unsigned total_safe = count(row, nbits);

    for (unsigned irow = 0; irow < nrows-1; irow++)
    {
        printf("Safe total so far: %u\n", total_safe);
        pretty_bin(row, nbits);
        putchar('\n');

        evolve(row, nwords);
        total_safe += count(row, nbits);
    }

    Result r = {.last = NULL, .total_safe = total_safe};
    return r;
}

int main()
{
    Result r;

    r = run("..^^.", 3);
    assert(!strcmp(r.last, "^^..^"));
    assert(r.total_safe == 6);

    r = run(".^^.^.^^^^", 10);
    assert(!strcmp(r.last, "^^.^^^..^^"));
    assert(r.total_safe == 38);

    // r = run("my input", 40);

    return 0;
}
