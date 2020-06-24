#!/usr/bin/env python3
import argparse
import sys
import os
if sys.version_info[0] < 3:
    print("This script requires Python version 3.5 or higher")
    sys.exit(1)
if sys.version_info[0] == 3 and sys.version_info[1] < 5:
    print("This script requires Python version 3.5 or higher")
    sys.exit(1)

from pathlib import Path

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="the path of the repository to process")
    parser.add_argument("-o", "--output", required=True, help="the path of the output folder")
    return parser.parse_args(args)

def error(msg):
    print("[ERROR] " + msg, file=sys.stderr)

def validate_parsed_args(parsed_args):
    is_input_directory = os.path.isdir(parsed_args.input)
    if not is_input_directory:
        error("The input parameter ({}) must specify a directory".format(parsed_args.input))
        return 2
    Path(parsed_args.output).mkdir(parents=True, exist_ok=True)
    is_output_directory = os.path.isdir(parsed_args.output)
    if not is_output_directory:
        error("The output parameter ({}) must specify a directory".format(parsed_args.output))
        return 3
    return 0

def main(parsed_args):
    from yapl.repository.git.lib import is_git_installed, is_path_in_git_repository
    print("is installed: " + str(is_git_installed()))
    print("is repository: " + str(is_path_in_git_repository(parsed_args.input)))
    return 0


if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    exit_code = validate_parsed_args(parsed_args)
    if exit_code == 0:
        exit_code = main(parsed_args)
    sys.exit(exit_code)
