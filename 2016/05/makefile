export
cflags_release=-O3 -march=native -fomit-frame-pointer
cflags_debug=-ggdb
cflags=-Wall -std=c99 -pthread $(cflags_release)

all: 05
05: 05.o md5.o
	gcc -o $@ $^ $$cflags
%.o: %.c makefile
	gcc -o $@ $< $$cflags -c
clean:
	rm -f *.o 05
