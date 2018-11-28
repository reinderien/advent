#!/usr/bin/make -f

export

cflags=-ggdb -Wall --std=c99
# cflags=-O3 -march=native -fomit-frame-pointer -Wall --std=c99

18: 18.o
	gcc $$cflags -o $@ $<

18.o: 18.c
	gcc $$cflags -o $@ $< -c
