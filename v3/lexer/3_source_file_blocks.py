#!/usr/local/bin/python3

from impl.bundle import Bundle
from impl.source_file_line import SourceFileLine


def main(args):
    bundle = Bundle(args.bundle_directory)
    bundle.load()
    lines = SourceFileLines(args.bundle_directory)
    manifest = bundle.load()
    for source_file_ref in manifest.get_source_file_refs():
        lines.process_file(source_file_ref)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process the bundle source lines')
    parser.add_argument('-b', '--bundle', dest='bundle_directory', required=True,
                        help='The directory to create the bundle in')
    args = parser.parse_args()

    main(args)
