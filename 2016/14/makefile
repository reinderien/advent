#!/usr/bin/make -f

export

cflags=-O3 -march=native -fomit-frame-pointer -Wall --std=c99

14-2: 14-2.o
	gcc $$cflags -o $@ $<

14-2.o: 14-2.c
	gcc $$cflags -o $@ $< -c
