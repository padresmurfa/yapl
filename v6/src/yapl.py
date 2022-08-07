#!/usr/bin/env python3
import argparse
import sys
import os
import os.path

if sys.version_info[0] < 3:
    print("This script requires Python version 3 or higher")
    sys.exit(1)

from transpiler.job import Job as TranspilationJob

def main(args):
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-i", "--input", help="the input yapl file")
    argument_parser.add_argument("-o", "--output_directory", help="the output directory")
    argument_parser.add_argument("-v", "--verbose", help="verbose level output", action='store_true')
    args = argument_parser.parse_args(args[1:])

    job = TranspilationJob()

    if args.input:
        job.set_input_file_name(args.input)

    if args.output_directory:
        job.set_output_directory_name(args.output_directory)

    if args.verbose:
        job.set_verbose()

    job.run()

    return 1 if job.failed() else 0


if __name__ == "__main__":
    exit_code = main(sys.argv)
    sys.exit(exit_code)
