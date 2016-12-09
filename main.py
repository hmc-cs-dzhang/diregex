import os
from src.semantics import semantics


def main():
    print("Welcome to Diregex")

    prog = ""

    while True:
        line = input('>>> ')

        if not line:
            break

        prog += line + '\n'

    path = os.getcwd()

    semantics.run(prog, path)


if __name__ == '__main__':
    main()
