#!/usr/bin/env python3
import argparse
import sys
import os
if sys.version_info[0] < 3:
    print("This script requires Python version 3 or higher")
    sys.exit(1)

from transpiler.abstract_syntax_tree import AbstractSyntaxTree


def main(args):
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-i", "--input", help="the input yapl file")
    args = argument_parser.parse_args(args[1:])

    if args.input:
        ast = AbstractSyntaxTree()
        filename = os.path.abspath(args.input)
        try:
            ast.parse(filename)
        except FileNotFoundError:
            print("File (" + filename + ") not accessible")
            return -2
    return 0


if __name__ == "__main__":
    exit_code = main(sys.argv)
    sys.exit(exit_code)
