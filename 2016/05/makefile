export
cflags=-Wall -O3 -march=native -fomit-frame-pointer -std=c99

all: 05
05: 05.o md5.o
	gcc -o $@ $^ $$cflags -pthread
%.o: %.c
	gcc -o $@ $^ $$cflags -c
clean:
	rm -f *.o 05
