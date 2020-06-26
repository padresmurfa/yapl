#!/usr/bin/env python3
import argparse
import sys
import os
from pathlib import Path
import json
import io

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--package", required=True, help="the namespace of the package to process")
    parser.add_argument("-b", "--build", required=True, help="the path of the build folder")
    return parser.parse_args(args)

def error(msg):
    print("[ERROR] " + msg, file=sys.stderr)

def progress(msg):
    print("[PROGRESS] " + msg)

def get_package_filename(build, package):
    return str(Path(build) / "packages" / (package + ".json"))

def get_source_filename(build, source):
    return str(Path(build) / "files" / (source + ".yapl"))

def validate_parsed_args(parsed_args):
    if not os.path.isfile(get_package_filename(parsed_args.build, parsed_args.package)):
        error("The parameters must specify a package file")
        return 1
    return 0

def main(parsed_args):
    progress("Starting")
    progress("Preparing output directories")
    modules_path = Path(parsed_args.build) / "modules"
    modules_path.mkdir(parents=True, exist_ok=True)
    process_package(parsed_args.build, parsed_args.package)
    progress("Finished")
    return 0

def load_package(build, package);
    package_filename = get_package_filename(build, package)
    with io.open(package_filename) as json_file:
        return json.load(json_file)

def load_sourcefile(build, hash);
    source_filename = get_source_filename(build, hash)
    with io.open(source_filename) as yapl_file:
        return yapl_file.read()

def process_package(build, package):
    progress("Processing package " + parsed_args.package)
    descriptor = load_package(build, package)
    for source_filename, sourcefile_info in descriptor["source_files"].items():
        revision = sourcefile_info["revision"]
        source_file = load_sourcefile(build, revision)

if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    exit_code = validate_parsed_args(parsed_args)
    if exit_code == 0:
        exit_code = main(parsed_args)
    sys.exit(exit_code)
