#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


// 20 to test
// 272 for part 1
// 35651584 for part 2
#define DISK_BITS 272

typedef uint64_t Word;
#define WORD_BITS (8*sizeof(Word))
#define DISK_WORDS (DISK_BITS/WORD_BITS + 1)


typedef struct
{
    unsigned len;
    Word data[DISK_WORDS];
} Fill;

static void init_fill(Fill *restrict f, const char *restrict input)
{
    memset(f->data, 0, DISK_WORDS*sizeof(Word));

    const char *c = input;
    for (Word *data = f->data;; data++)
    {
        for (Word b = 0; b < WORD_BITS; b++)
        {
            if (!*c)
                return;
            *data |= (*c - '0') << b;
            f->len++;
            c++;
        }
    }
}

static void fill_churn(Fill *restrict f)
{
    unsigned tail_end = 2*f->len,  // Virtual offset of tail
             b_tail;               // Offset of tail
    if (tail_end > DISK_BITS-1)
        b_tail = DISK_BITS-1;
    else b_tail = tail_end;
    int o_tail = b_tail % WORD_BITS;            // Offset in tail quad
    Word *d_tail = f->data + b_tail/WORD_BITS;  // Tail data pointer

    f->len = b_tail+1;

    unsigned b_head = tail_end - b_tail;              // Offset of head
    Word m_head = 1 << (b_head % WORD_BITS);          // Mask in head quad
    const Word *d_head = f->data + b_head/WORD_BITS;  // Head data pointer

    for (; b_head < b_tail; b_head++, b_tail--)
    {
        *d_tail |= ((Word)!(*d_head & m_head)) << o_tail;

        m_head <<= 1;
        if (!m_head)
        {
            m_head = 1;
            d_head++;
        }

        o_tail--;
        if (o_tail < 0)
        {
            o_tail = WORD_BITS-1;
            d_tail--;
        }
    }
}

static void pretty_bin(const Word *restrict data, unsigned len, bool sep)
{
    unsigned btot = 0;
    for (const uint8_t *d = (const uint8_t*)data;; d++)
    {
        for (unsigned b = 0; b < 8; b++)
        {
            putchar('0' + ((*d >> b)&1));
            if (sep && b==3) putchar('_');
            if (++btot >= len)
            {
                putchar('\n');
                return;
            }
        }
        if (sep) putchar(' ');
    }
}

static void checksum(const Fill *restrict f)
{
    Word cs[DISK_WORDS/2 + 1];
    unsigned in_len = f->len, out_len;
    const Word *in_dat = f->data;

    do
    {
        const Word *din = in_dat;
        unsigned bin = 0, bin_total = 0;
        for (Word *dout = cs; bin_total < in_len; dout++)
        {
            Word new_dout = 0;
            for (unsigned bout = 0; bout < WORD_BITS; bout++)
            {
                Word bit = !((
                                 (*din >> bin) & 1
                             ) ^ (
                                 (*din >> (bin+1)) & 1
                             ));
                new_dout |= bit << bout;

                bin_total += 2;
                if (bin_total >= in_len)
                    break;

                bin += 2;
                if (bin >= WORD_BITS)
                {
                    bin = 0;
                    din++;
                }
            }
            *dout = new_dout;
        }
        out_len = in_len/2;

        in_dat = cs;
        in_len = out_len;
    } while (!(out_len & 1));


    printf("CS: ");
    pretty_bin(cs, out_len, false);
    printf("CS bits: %u\n\n", out_len);
}

int main()
{
    Fill fill;
    const char *input = "10001001100000001"; // our input; use "10000" to test
    init_fill(&fill, input);

    printf("Word bits: %lu\n", WORD_BITS);
    printf("Disk bits: %u\n", DISK_BITS);
    printf("Disk words: %lu\n", DISK_WORDS);
    printf("Initial data: ");
    pretty_bin(fill.data, fill.len, true);
    printf("Initial bits: %u\n\n", fill.len);

    while (fill.len < DISK_BITS)
        fill_churn(&fill);

    // printf("Data: ");
    // pretty_bin(fill.data, fill.len, TRUE);
    printf("Data bits: %u\n\n", fill.len);

    checksum(&fill);
    // Part 1: 10101001010100001 is correct
    // Part 2: 10100001101101110 is too low

    return 0;
}