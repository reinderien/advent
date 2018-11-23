// md5 impl based on
// https://tls.mbed.org/md5-source-code

#include <assert.h>
#include <pthread.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Assume little-endian 64-bit machine

typedef uint8_t buffer_t[64];
typedef uint32_t block_t[16];

typedef struct {
    union {
        uint32_t state[4];  // intermediate and final digest state
        uint8_t output[16];
    };
    uint64_t total;         // number of bytes processed
    buffer_t buffer;        // data block being processed
} md5_context;

static const md5_context md5_init = {{{
    0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476
}}};

static void md5_process(md5_context *ctx, const buffer_t *data) {
    const block_t *X = (const block_t*)data;

    #define S(x,n) ((x << n) | (x >> (32 - n)))
    #define P(a,b,c,d,k,s,t) {       \
        a += F(b,c,d) + (*X)[k] + t; \
        a = S(a,s) + b;              \
    }

    uint32_t A = ctx->state[0], B = ctx->state[1],
             C = ctx->state[2], D = ctx->state[3];

    #define F(x,y,z) (z ^ (x & (y ^ z)))
    P(A, B, C, D,  0,  7, 0xD76AA478); P(D, A, B, C,  1, 12, 0xE8C7B756);
    P(C, D, A, B,  2, 17, 0x242070DB); P(B, C, D, A,  3, 22, 0xC1BDCEEE);
    P(A, B, C, D,  4,  7, 0xF57C0FAF); P(D, A, B, C,  5, 12, 0x4787C62A);
    P(C, D, A, B,  6, 17, 0xA8304613); P(B, C, D, A,  7, 22, 0xFD469501);
    P(A, B, C, D,  8,  7, 0x698098D8); P(D, A, B, C,  9, 12, 0x8B44F7AF);
    P(C, D, A, B, 10, 17, 0xFFFF5BB1); P(B, C, D, A, 11, 22, 0x895CD7BE);
    P(A, B, C, D, 12,  7, 0x6B901122); P(D, A, B, C, 13, 12, 0xFD987193);
    P(C, D, A, B, 14, 17, 0xA679438E); P(B, C, D, A, 15, 22, 0x49B40821);
    #undef F

    #define F(x,y,z) (y ^ (z & (x ^ y)))
    P(A, B, C, D,  1,  5, 0xF61E2562); P(D, A, B, C,  6,  9, 0xC040B340);
    P(C, D, A, B, 11, 14, 0x265E5A51); P(B, C, D, A,  0, 20, 0xE9B6C7AA);
    P(A, B, C, D,  5,  5, 0xD62F105D); P(D, A, B, C, 10,  9, 0x02441453);
    P(C, D, A, B, 15, 14, 0xD8A1E681); P(B, C, D, A,  4, 20, 0xE7D3FBC8);
    P(A, B, C, D,  9,  5, 0x21E1CDE6); P(D, A, B, C, 14,  9, 0xC33707D6);
    P(C, D, A, B,  3, 14, 0xF4D50D87); P(B, C, D, A,  8, 20, 0x455A14ED);
    P(A, B, C, D, 13,  5, 0xA9E3E905); P(D, A, B, C,  2,  9, 0xFCEFA3F8);
    P(C, D, A, B,  7, 14, 0x676F02D9); P(B, C, D, A, 12, 20, 0x8D2A4C8A);
    #undef F

    #define F(x,y,z) (x ^ y ^ z)
    P(A, B, C, D,  5,  4, 0xFFFA3942); P(D, A, B, C,  8, 11, 0x8771F681);
    P(C, D, A, B, 11, 16, 0x6D9D6122); P(B, C, D, A, 14, 23, 0xFDE5380C);
    P(A, B, C, D,  1,  4, 0xA4BEEA44); P(D, A, B, C,  4, 11, 0x4BDECFA9);
    P(C, D, A, B,  7, 16, 0xF6BB4B60); P(B, C, D, A, 10, 23, 0xBEBFBC70);
    P(A, B, C, D, 13,  4, 0x289B7EC6); P(D, A, B, C,  0, 11, 0xEAA127FA);
    P(C, D, A, B,  3, 16, 0xD4EF3085); P(B, C, D, A,  6, 23, 0x04881D05);
    P(A, B, C, D,  9,  4, 0xD9D4D039); P(D, A, B, C, 12, 11, 0xE6DB99E5);
    P(C, D, A, B, 15, 16, 0x1FA27CF8); P(B, C, D, A,  2, 23, 0xC4AC5665);
    #undef F

    #define F(x,y,z) (y ^ (x | ~z))
    P(A, B, C, D,  0,  6, 0xF4292244); P(D, A, B, C,  7, 10, 0x432AFF97);
    P(C, D, A, B, 14, 15, 0xAB9423A7); P(B, C, D, A,  5, 21, 0xFC93A039);
    P(A, B, C, D, 12,  6, 0x655B59C3); P(D, A, B, C,  3, 10, 0x8F0CCC92);
    P(C, D, A, B, 10, 15, 0xFFEFF47D); P(B, C, D, A,  1, 21, 0x85845DD1);
    P(A, B, C, D,  8,  6, 0x6FA87E4F); P(D, A, B, C, 15, 10, 0xFE2CE6E0);
    P(C, D, A, B,  6, 15, 0xA3014314); P(B, C, D, A, 13, 21, 0x4E0811A1);
    P(A, B, C, D,  4,  6, 0xF7537E82); P(D, A, B, C, 11, 10, 0xBD3AF235);
    P(C, D, A, B,  2, 15, 0x2AD7D2BB); P(B, C, D, A,  9, 21, 0xEB86D391);
    #undef F

    ctx->state[0] += A; ctx->state[1] += B;
    ctx->state[2] += C; ctx->state[3] += D;
}

static void md5_update(md5_context *ctx, const uint8_t *input, int32_t ilen) {
    if (ilen < 1) return;

    uint32_t left = ctx->total & 63,
             fill = 64 - left;
    ctx->total += ilen;

    if (left && ilen >= fill) {
        memcpy(ctx->buffer + left, input, fill);
        md5_process(ctx, &ctx->buffer);
        input += fill;
        ilen -= fill;
        left = 0;
    }

    const buffer_t *buffer = (const buffer_t*)input;
    for (; ilen >= 64; ilen -= 64) {
        md5_process(ctx, buffer);
        buffer++;
    }

    if (ilen > 0)
        memcpy(ctx->buffer + left, buffer, ilen);
}

static const buffer_t md5_padding = { 0x80 };

static void md5_finish(md5_context *ctx) {
    uint32_t last = ctx->total & 63,
             padn = (last < 56) ? (56 - last) : (120 - last);
    uint64_t total = ctx->total << 3;

    md5_update(ctx, md5_padding, padn);
    md5_update(ctx, (const uint8_t*)&total, 8);
}

static char dec2hex(uint8_t d) {
    return d + (d >= 10 ? 'a'-10 : '0');
}

static uint8_t hex2dec(char h) {
    return h - (h >= 'a' ? 'a'-10 : '0');
}

static void md5_to_hex(const md5_context *ctx, char *hex) {
    for (int i = 0; i < 16; i++) {
        uint8_t c = ctx->output[i];
        hex[2*i    ] = dec2hex(c >> 4);
        hex[2*i + 1] = dec2hex(c & 15);
    }
    hex[32] = '\0';
}

static char get_repeat(const char (*hex)[33], unsigned n) {
    int run;
    for (int start = 0;; start += run) {
        char first = (*hex)[start];
        for (run = 1;; run++) {
            if (run >= n)
                return first;
            if (start + run >= 32)
                return 0;
            if ((*hex)[start + run] != first)
                break;
        }
    }
}


typedef struct {
    unsigned index;
    uint8_t hexit;
} matched_hash;

typedef struct {
    unsigned i_first, i_last, n;
    matched_hash queue[1000];
} circular;
circular quints, triples;

static md5_context root_ctx;

// Positions in circular buffers
unsigned first_index = 0, last_index = 0, keys_found = 0;

static unsigned quint_counts[16] = { 0 };

static char push(circular *buf, const char (*hex)[33], unsigned n) {
    char repeat = get_repeat(hex, n);
    if (!repeat) return -1;
    matched_hash m = {last_index, hex2dec(repeat)};
    buf->queue[buf->i_last] = m;
    buf->i_last = (buf->i_last + 1) % 1000;
    buf->n++;
    return m.hexit;
}

static char pop(circular *buf) {
    matched_hash m = buf->queue[buf->i_first];
    first_index = m.index;
    buf->i_first = (buf->i_first + 1) % 1000;
    buf->n--;
    return m.hexit;
}

static void produce() {
    // As long as the distance between the first and last index is smaller
    // than 1000, populate.
    for (; last_index - first_index < 1000; last_index++) {
        char hex[33];
        md5_context ctx = root_ctx;
        int len = snprintf(hex, 33, "%u", last_index);
        for (unsigned r = 0; r < 2017; r++) {
            md5_update(&ctx, (uint8_t*)hex, len);
            md5_finish(&ctx);
            md5_to_hex(&ctx, hex);
            len = 32;
            ctx = md5_init;
        }
        push(&triples, &hex, 3);
        char repeat = push(&quints, &hex, 5);
        if (repeat)
            quint_counts[(int)repeat]++;
    }
}

static void consume() {
    // Advance the first index through triples until the current triple does
    // not have enough of a queue ahead of it, or there are no more triples.
    for (;;) {
        unsigned advance_to;
        if (!triples.n)
            advance_to = last_index;
        else
            advance_to = triples.queue[triples.i_first].index;
        for (; first_index < advance_to;) {
            // Clear out old quints
            if (quints.n)
                quint_counts[(int)pop(&quints)]--;
            else
                first_index = advance_to;
        }
        if (last_index - first_index < 1000)
            return;

        // Consume oldest triple
        if (quint_counts[(int)pop(&triples)]) {
            keys_found++;
            if (keys_found >= 64) {
                printf("%u\n", first_index);
                exit(0);
            }
        }
    }
}

int main() {
    // Set up root hash context: always used before updating with index
    root_ctx = md5_init;
    md5_update(&root_ctx, (uint8_t*)"abc", 3);

    for (;;) {
        produce();
        consume();
    }

    return 0;
}
