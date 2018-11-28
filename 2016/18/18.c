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
    const char *last;
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

static void evolve(Word *row, unsigned nwords, unsigned nbits)
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

        row[i] = (lcarry | (row[i] << 1)) ^
                 (rcarry | (row[i] >> 1));
        lcarry = next_lcarry;
    }

    uint64_t last_mask = (1 << (nbits % WORD_BITS)) - 1;
    row[i] = (
                (lcarry | (row[i] << 1)) ^
                (row[i] >> 1)
             ) & last_mask;
}

static const char *print(const Word *row, unsigned nbits)
{
    char *printed = malloc(nbits+1),
         *p = printed;
    const char *pend = p + nbits;
    printed[nbits] = '\0';

    for (const Word *r = row;; r++)
    {
        for (Word b = 1; b; b <<= 1)
        {
            if (p >= pend)
                return printed;
            *p++ = (*r & b) ? '^' : '.';
        }
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
        evolve(row, nwords, nbits);
        total_safe += count(row, nbits);
    }

    const char *last = print(row, nbits);
    printf("Safe total: %u\n\n", total_safe);

    Result r = {.last = last,
                .total_safe = total_safe};
    return r;
}

int main()
{
    Result r;

    puts("Test 1");
    r = run("..^^.", 3);
    assert(!strcmp(r.last, "^^..^"));
    assert(r.total_safe == 6);
    free((void*)r.last);

    puts("Test 2");
    r = run(".^^.^.^^^^", 10);
    assert(!strcmp(r.last, "^^.^^^..^^"));
    assert(r.total_safe == 38);
    free((void*)r.last);

    puts("Part 1");
    const char *input =
        ".^^..^...^..^^.^^^.^"
        "^^.^^^^^^.^.^^^^.^^."
        "^^^^^^.^...^......^."
        "..^^^..^^^.....^^^^^"
        "^^^^....^^...^^^^..^";
    r = run(input, 40);
    free((void*)r.last);

    puts("Part 2");
    r = run(input, 400000);
    free((void*)r.last);

    return 0;
}
