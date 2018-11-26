#!/usr/bin/make -f

export

cflags=-ggdb -Wall --std=c99
# cflags=-O3 -march=native -fomit-frame-pointer -Wall --std=c99

16: 16.o
	gcc $$cflags -o $@ $<

16.o: 16.c
	gcc $$cflags -o $@ $< -c
