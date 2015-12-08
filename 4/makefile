export
cflags=-Wall -O3 -march=native -fomit-frame-pointer -std=c99

all: advent-4
advent-4: advent-4.o md5.o
	gcc -o $@ $^ $$cflags
%.o: %.c
	gcc -o $@ $^ $$cflags -c
clean:
	rm -f *.o advent-4
