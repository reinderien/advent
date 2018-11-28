#!/usr/bin/make -f

export

cflags=-ggdb -Wall --std=c99
# cflags=-O3 -march=native -fomit-frame-pointer -Wall --std=c99

19: 19.o
	gcc $$cflags -o $@ $<

19.o: 19.c
	gcc $$cflags -o $@ $< -c
