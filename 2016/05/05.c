#include <assert.h>
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include "md5.h"

static const uint32_t mask = 0x00F0FFFF;
static int nthreads;
static int found = 0;

static void *md5_thread(void *pstart) {
    MD5_CTX ctx;
    uint32_t nindex = *(int*)pstart;
    const int prefixlen = 8;
    char input[32] = "wtnhxymk", *index = input + prefixlen;

    for (;; nindex += nthreads) {
        int indexlen = sprintf(index, "%u", nindex);
        MD5_Init(&ctx);
        MD5_Update(&ctx, input, prefixlen+indexlen);
        MD5_Final(&ctx);

        if (!(ctx.a & mask)) {
            int digit = (ctx.a >> 16) & 0xF;
            printf("%u: %X\n", found++, digit);
        }
        if (found >= 8)
            return NULL;
    }
}


int main(int argc, const char **argv) {

    nthreads = sysconf(_SC_NPROCESSORS_ONLN);
    printf("%d threads\n", nthreads);

    pthread_t threads[nthreads];
    uint32_t starts[nthreads];
    for (int t = 0; t < nthreads; t++) {
        starts[t] = t;
        assert(!pthread_create(threads+t, NULL, md5_thread, starts+t));
    }
    for (int t = 0; t < nthreads; t++)
        assert(!pthread_join(threads[t], NULL));

    return 0;
}