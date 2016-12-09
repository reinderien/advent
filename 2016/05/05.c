#include <assert.h>
#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "md5.h"

// Part 1 answer: 2414bc77

#define PART      2
#define ZEROS     5
// 0x00F0FFFF
#define MASK       ( ((1 << 4*(ZEROS-1))-1) | 0xF<<4*ZEROS )
#define NDIGITS    8
#define PREFIX_REF "abc"
#define PREFIX     "wtnhxymk"
#define PREFIXLEN  sizeof(PREFIX)-1

static int nthreads;
static int found = 0;
static int8_t pwd[NDIGITS];

static void *md5_thread(void *pstart) {
    MD5_CTX ctx;
    uint32_t nindex = *(uint32_t*)pstart;
    char input[32] = PREFIX, *index = input + PREFIXLEN;

    for (;; nindex += nthreads) {
        int indexlen = sprintf(index, "%u", nindex);
        MD5_Init(&ctx);
        MD5_Update(&ctx, input, PREFIXLEN+indexlen);
        MD5_Final(&ctx);

        if (!(ctx.a & MASK)) {
            uint8_t d6 = (ctx.a >> 4*(ZEROS-1)) & 0xF;
#if PART==1
            pwd[found++] = d6;
#elif PART==2
            if (d6 < NDIGITS && pwd[d6] == -1) {
                int d7 = (ctx.a >> 4*(ZEROS+2)) & 0xF;
                pwd[d6] = d7;
                found++;
            }
#endif
        }
        if (found >= NDIGITS)
            return NULL;
    }
}


int main(int argc, const char **argv) {

    nthreads = sysconf(_SC_NPROCESSORS_ONLN);
    printf("%d threads\n", nthreads);

    memset(pwd, -1, NDIGITS);

    pthread_t threads[nthreads];
    uint32_t starts[nthreads];
    for (int t = 0; t < nthreads; t++) {
        starts[t] = t;
        assert(!pthread_create(threads+t, NULL, md5_thread, starts+t));
    }
    for (int t = 0; t < nthreads; t++)
        assert(!pthread_join(threads[t], NULL));
    for (int i = 0; i < NDIGITS; i++)
        printf("%X", pwd[i]);
    putchar('\n');

    return 0;
}