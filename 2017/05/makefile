#!/usr/bin/make -f

export

cflags=-O3 -march=native -fomit-frame-pointer -Wall --std=c99

05_2: 05_2.o
	gcc $$cflags -o $@ $^

%.o: %.c
	gcc $$cflags -o $@ $^ -c
