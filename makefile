CC=gcc
CFLAGS=-O3 -match=native -Wall -Wextra

bfasm:
	@$(CC) -o sapphire/bfasm sapphire/bfasm.c $(CFLAGS)
