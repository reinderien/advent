#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define DISK_BITS 272 // our input; use 20 to test
#define DISK_QUADS (DISK_BITS/64 + 1)


typedef struct
{
    unsigned len;
    uint64_t data[DISK_QUADS];
} Fill;

static void init_fill(Fill *restrict f, const char *restrict input)
{
    // memfill(f->data, 0, DISK_QUADS*sizeof(uint64_t));
    for (int d = 0; d < DISK_QUADS; d++)
        f->data[d] = 0;

    const char *c = input;
    for (uint64_t *data = f->data;; data++)
    {
        for (uint64_t b = 0; b < 64; b++)
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
    int o_tail = b_tail % 64;                // Offset in tail quad
    uint64_t *d_tail = f->data + b_tail/64;  // Tail data pointer

    f->len = b_tail+1;

    unsigned b_head = tail_end - b_tail;           // Offset of head
    uint64_t m_head = 1 << (b_head % 64);          // Mask in head quad
    const uint64_t *d_head = f->data + b_head/64;  // Head data pointer

    for (; b_head < b_tail; b_head++, b_tail--)
    {
        *d_tail |= ((uint64_t)!(*d_head & m_head)) << o_tail;

        m_head <<= 1;
        if (!m_head)
        {
            m_head = 1;
            d_head++;
        }

        o_tail--;
        if (o_tail < 0)
        {
            o_tail = 63;
            d_tail--;
        }
    }
}

static void pretty_bin(const uint64_t *restrict data, unsigned len)
{
    unsigned btot = 0;
    for (const uint8_t *d = (const uint8_t*)data;; d++)
    {
        for (unsigned b = 0; b < 8; b++)
        {
            putchar('0' + ((*d >> b)&1));
            if (b==3) putchar('_');
            if (++btot >= len)
            {
                putchar('\n');
                return;
            }
        }
        putchar(' ');
    }
}

static void checksum(const Fill *restrict f)
{
    uint64_t cs[DISK_QUADS/2 + 1];
    unsigned in_len = f->len, out_len;
    const uint64_t *in_dat = f->data;

    do
    {
        const uint64_t *din = in_dat;
        unsigned bin = 0, bin_total = 0;
        for (uint64_t *dout = cs; bin_total < in_len; dout++)
        {
            uint64_t new_dout = 0;
            for (unsigned bout = 0; bout < 64; bout++)
            {
                uint64_t bit = !((
                                     (*din >> bin) & 1
                                 ) ^ (
                                     (*din >> (bin+1)) & 1
                                 ));
                new_dout |= bit << bout;

                bin_total += 2;
                if (bin_total >= in_len)
                    break;

                bin += 2;
                if (bin >= 64)
                {
                    bin = 0;
                    din++;
                }
            }
            *dout = new_dout;
        }
        out_len = in_len/2;
        printf("CS: ");
        pretty_bin(cs, out_len);
        printf("Len: %u\n\n", out_len);

        in_dat = cs;
        in_len = out_len;
    } while (!(out_len & 1));
}

int main()
{
    Fill fill;
    const char *input = "10001001100000001"; // our input; use "10000" to test
    init_fill(&fill, input);

    printf("Disk bits: %u\n", DISK_BITS);
    printf("Disk quads: %u\n", DISK_QUADS);
    printf("Initial data: ");
    pretty_bin(fill.data, fill.len);
    printf("Initial len: %u\n\n", fill.len);

    while (fill.len < DISK_BITS)
    {
        fill_churn(&fill);

        printf("Data: ");
        pretty_bin(fill.data, fill.len);
        printf("Len: %u\n\n", fill.len);
    }

    checksum(&fill);

    return 0;
}