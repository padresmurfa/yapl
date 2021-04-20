#!/usr/local/bin/python3

from yapl.v4.lexer.shared.transpilation import Transpilation
from yapl.v4.lexer.shared.module_lines.manifest.reader \
    import ManifestReader as ModuleLinesManifestReader
from yapl.v4.lexer.shared.tokenized_lines.builder \
    import ManifestBuilder as TokenizedLinesManifestBuilder


def main(args):
    transpilation = Transpilation(args.transpilation_directory)
    transpilation.load()
    modules = transpilation.manifest().get_module_file_refs()
    for module_ref in modules:
        module_sha256 = module_ref["sha256"]
        print("processing module: " + module_ref["filename"] + " (" + module_sha256 + ")")
        builder = TokenizedLinesManifestBuilder(
            args.transpilation_directory,
            module_sha256
        )
        reader = ModuleLinesManifestReader(
            args.transpilation_directory,
            module_sha256
        )
        for logical_line in reader.logical_lines():
            try:
                builder.tokenize_logical_line(
                    logical_line.sha256(),
                    logical_line.content()
                )
            except:
                print("FAILED to process logical line #{}, sha256={}, actual line(s)={}".format(
                    logical_line.logical_line_number(),
                    logical_line.sha256(),
                    str(logical_line.actual_line_numbers())
                ))
                raise
        builder.save()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Tokenize previously collected module lines')
    parser.add_argument('-t', '--transpilation', dest='transpilation_directory', required=True,
                        help='The transpilation directory')
    args = parser.parse_args()

    main(args)
