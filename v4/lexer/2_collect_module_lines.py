#!/usr/local/bin/python3

from yapl.v4.lexer.shared.transpilation import Transpilation
from yapl.v4.lexer.shared.module_lines.manifest.builder import ManifestBuilder as ModuleLinesManifestBuilder


def main(args):
    transpilation = Transpilation(args.transpilation_directory)
    transpilation.load()
    modules = transpilation.manifest().get_module_file_refs()
    for module_ref in modules:
        print("processing file: " + module_ref["filename"])
        module_lines = ModuleLinesManifestBuilder(
            args.transpilation_directory,
            module_ref["sha256"]
        )
        module_lines.parse()
        module_lines.save()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Collect source lines from previously collected modules')
    parser.add_argument('-t', '--transpilation', dest='transpilation_directory', required=True,
                        help='The transpilation directory')
    args = parser.parse_args()

    main(args)
