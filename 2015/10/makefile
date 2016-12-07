export
cflags=-Wall -O3 -march=native -fomit-frame-pointer -std=c99
# cflags=-Wall -march=native -std=c99 -O0 -ggdb

all: 10
10: 10.o
	gcc -o $@ $^ $$cflags
%.o: %.c
	gcc -o $@ $^ $$cflags -c
clean:
	rm -f *.o 10
