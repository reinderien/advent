#include <assert.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "md5.h"

/*
Zeros    Suffix
    1        11
    2        67
    3     10571
    4     34311
    5    117946
    6   3938038
    7 257209165
*/

static uint32_t mask;
static int nthreads;
static int found = 0;

static void *md5_thread(void *pstart) {
    MD5_CTX ctx;
    const int start = *(int*)pstart;
    char input[32] = "ckczppom", *suffix = input + 8;
    
    for (int nsuffix = start;; nsuffix += nthreads) {
        sprintf(suffix, "%d", nsuffix);
        MD5_Init(&ctx);
        MD5_Update(&ctx, input, strlen(input));
        MD5_Final(&ctx);
        
        if (!(ctx.a & mask)) {
            if (!found || found > nsuffix)
                found = nsuffix;
            return NULL;
        }
        if (found && nsuffix > found)
            return NULL;
    }
}

int main(int argc, const char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s (zerocount)\n", argv[0]);
        return 1;
    }
    
    int zeros;
    sscanf(argv[1], "%d", &zeros);
    if (zeros < 1 || zeros > 8) {
        fprintf(stderr, "Zeros out of range\n");
        return 1;
    }
    
    nthreads = sysconf(_SC_NPROCESSORS_ONLN);
    printf("%d threads\n", nthreads);
    
    // Hack for endian quirk
    mask = (1 << (4*(zeros & ~1))) - 1;
    if (zeros & 1)
        mask |= 0xF << (4*zeros);
    
    pthread_t threads[nthreads];
    for (int t = 1; t <= nthreads; t++) {
        int *pt = (int*)malloc(sizeof(int));
        *pt = t;
        assert(!pthread_create(threads+t-1, NULL, md5_thread, pt));
    }
    for (int t = 0; t < nthreads; t++)
        assert(!pthread_join(threads[t], NULL));
    
    printf("%d\n", found);
    return 0;
}
