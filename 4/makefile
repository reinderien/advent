export
cflags=-Wall -O3 -march=native -fomit-frame-pointer -std=c99

all: 4
4: 4.o md5.o
	gcc -o $@ $^ $$cflags
%.o: %.c
	gcc -o $@ $^ $$cflags -c
clean:
	rm -f *.o 4
