CC=gcc
CFLAGS=-O3 -march=native -Wall -Wextra

bfasm:
	@$(CC) -o sapphire/bfasm sapphire/bfasm.c $(CFLAGS)
