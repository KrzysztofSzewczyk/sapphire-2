CC=gcc
CFLAGS=-Ofast -march=native -Wall -Wextra

bfasm:
	@$(CC) -o sapphire/bfasm vendor/bfasm.c $(CFLAGS)
