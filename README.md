# Sapphire 2

Sapphire 2 is a Python-like programming language that compiles to the brainfuck.

## Features

  - Variables
  - Functions
  - Strings
  - Some operators
  - Imports
  - Arrays
  - Tuples
  - If, else, while
  - Exceptions (bugged)

## Requirements

  - Python 3.6.x
  - sly
  - C compiler (recommended gcc or clang)

## Installation

```sh
$ git clone https://github.com/SapphireProject/sapphire-2
$ cd sapphire-2
$ make
$ pip3 install sly
```

## Usage

```sh
$ python3 sapphire -h
usage: sapphire [-h] [-o output.b] [-S] file.sph

Py-like to Brainfuck compiler.

positional arguments:
  file.sph     Source file

optional arguments:
  -h, --help   show this help message and exit
  -o output.b  Output file
  -S           Output assembly
```

## Development

Want to contribute? Great!
Fork the repository, make changes, and create a pull request.

## Todos

 - Add tests
 - Add optimization

License
----
`MIT`
