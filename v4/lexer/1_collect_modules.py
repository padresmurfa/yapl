#!/usr/local/bin/python3

import os
from yapl.v4.lexer.shared.file_reference import to_file_reference
from yapl.v4.lexer.shared.transpilation import Transpilation

# TODO: split into read and write path, akin to module_lines

class InputDirectory(object):

    def __init__(self, input_directory):
        self.input_directory = os.path.abspath(input_directory)

    def __enumerate(self, path):
        for subpath in os.listdir(path):
            fullpath = os.path.join(path, subpath)
            if os.path.isdir(fullpath):
                for each in self.__enumerate(fullpath):
                    yield each
            elif os.path.isfile(fullpath):
                extension = os.path.splitext(subpath)[1]
                if extension == ".yapl":
                    yield fullpath

    def get_module_file_references(self):
        for module_filename in self.__enumerate(self.input_directory):
            yield to_file_reference(self.input_directory, module_filename)


def main(args):
    input_directory = InputDirectory(args.input_directory)
    transpilation = Transpilation.create(args.transpilation_directory)
    module_file_references = list(input_directory.get_module_file_references())
    for module_file_reference in module_file_references:
        transpilation.add_module_file_ref(module_file_reference)
    transpilation.save()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=
                                     'Collect YAPL modules from a directory, recursively')
    parser.add_argument('-i', '--input', dest='input_directory', required=True,
            help='the directory to process YAPL packages within')
    parser.add_argument('-t', '--transpilation', dest='transpilation_directory', required=True,
                        help='The transpilation directory')
    args = parser.parse_args()

    main(args)
