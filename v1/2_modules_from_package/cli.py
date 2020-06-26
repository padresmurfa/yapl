#!/usr/bin/env python3
import argparse
import sys
import os
import time
from datetime import datetime
import shutil
from pathlib import Path
import yapl.repository.git.lib as git
import json
import io
import yapl

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--package", required=True, help="the namespace of the package to process")
    parser.add_argument("-b", "--build", required=True, help="the path of the build folder")
    return parser.parse_args(args)

def error(msg):
    print("[ERROR] " + msg, file=sys.stderr)

def progress(msg):
    print("[PROGRESS] " + msg)

def get_package_filename(parsed_args):
    return str(Path(parsed_args.build) / "packages" / (parsed_args.package + ".json"))

def validate_parsed_args(parsed_args):
    if not os.path.isfile(get_package_filename(parsed_args)):
        error("The parameters must specify a package file")
        return 1
    return 0

def main(parsed_args):
    package_filename = get_package_filename(parsed_args)
    progress("Starting")
    progress("Preparing output directories")
    modules_path = Path(parsed_args.build) / "modules"
    Path(modules_path).mkdir(parents=True, exist_ok=True)
    progress("Finished")
    return 0


if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    exit_code = validate_parsed_args(parsed_args)
    if exit_code == 0:
        exit_code = main(parsed_args)
    sys.exit(exit_code)
