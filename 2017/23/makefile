#!/usr/bin/make -f

export

cflags=-O3 -march=native -fomit-frame-pointer -Wall --std=c99

23_2: 23_2.o
	gcc $$cflags -o $@ $<

23_2.o: 23_2.c prog.c
	gcc $$cflags -o $@ $< -c

prog.c: 23_2.py 23.in
	./$<
