#!/usr/local/bin/python3

import glob
import os
from impl.file_reference import FileReference, to_file_reference
from impl.bundle import Bundle


class SourceDirectory(object):

    def __init__(self, source_directory):
        self.source_directory = os.path.abspath(source_directory)

    def get_input_file_references(self):
        glob_all_yapl_files = os.path.join(self.source_directory, "**/*.yapl")
        for source_filename in glob.glob(glob_all_yapl_files, recursive=True):
            yield to_file_reference(self.source_directory, source_filename)


class BundleDirectory(object):

    def __init__(self, bundle_directory):
        self.bundle_directory = os.path.abspath(bundle_directory)

    def create_bundle(self):
        os.makedirs(self.bundle_directory, mode = 0o777, exist_ok = True)
        return Bundle(self.bundle_directory)


def main(args):
    source_directory = SourceDirectory(args.source_directory)
    bundle_directory = BundleDirectory(args.bundle_directory)

    bundle = bundle_directory.create_bundle()
    input_file_references = list(source_directory.get_input_file_references())
    for source_ref in input_file_references:
        bundle.add_source_file_ref(source_ref)
    bundle.save()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Create a YAPL source bundle from a directory')
    parser.add_argument('-s', '--source', dest='source_directory', required=True,
            help='the directory to convert to a YAPL source bundle')
    parser.add_argument('-b', '--bundle', dest='bundle_directory', required=True,
                        help='The directory to create the bundle in')
    args = parser.parse_args()

    main(args)
