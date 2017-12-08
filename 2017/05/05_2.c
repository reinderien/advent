#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>

// It's a miracle we got anything working in these days, but...
// this is insanely fast in comparison to Python

static int *read_offsets(const char *path, int *n) {
    struct stat st;
    assert(!stat(path, &st));
    int fd = open(path, O_RDONLY);
    assert(fd != -1);
    char *raw = malloc(st.st_size);
    assert(raw);
    assert(read(fd, raw, st.st_size) == st.st_size);

    *n = 0;
    for (int i = 0; i < st.st_size; i++)
        *n += raw[i] == '\n';

    int *offsets = malloc(sizeof(int) * *n);
    assert(offsets);

    int off = 0;
    for (int i = 0; i < *n; i++) {
        int nread;
        assert(1 == sscanf(raw+off, "%d%n", offsets+i, &nread));
        off += nread;
    }
    free(raw);
    return offsets;
}

int main() {
    int n;
    int *offsets = read_offsets("05.in", &n);
    printf("%d lines\n", n);

    int index = 0, steps = 0;
    do {
        int *poffset = offsets+index,
            offset = *poffset;
        if (offset >= 3)
            (*poffset)--;
        else (*poffset)++;

        index += offset;
        steps++;
    } while (index >= 0 && index < n);

    printf("%d steps\n", steps);
    return 0;
}
