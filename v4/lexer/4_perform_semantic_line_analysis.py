#!/usr/local/bin/python3

import copy

from yapl.v4.lexer.shared.transpilation import Transpilation
from yapl.v4.lexer.shared.tokenized_lines.reader \
    import ManifestReader as TokenizedLinesManifestReader
from yapl.v4.lexer.shared.semantic_lines.builder \
    import ManifestBuilder as SemanticLinesManifestBuilder


def main(args):
    transpilation = Transpilation(args.transpilation_directory)
    transpilation.load()
    modules = transpilation.manifest().get_module_file_refs()
    for module_ref in modules:
        module_sha256 = module_ref["sha256"]
        print("processing module: " + module_ref["filename"] + " (" + module_sha256 + ")")
        builder = SemanticLinesManifestBuilder(
            args.transpilation_directory,
            module_sha256
        )
        reader = TokenizedLinesManifestReader(
            args.transpilation_directory,
            module_sha256
        )
        for tokenized_line in reader.tokenized_lines():
            tokens_before = copy.copy(tokenized_line.tokens())
            try:
                builder.process_line(
                    tokenized_line.sha256(),
                    tokenized_line.tokens()
                )
            except:
                print("FAILED to process tokenized line sha256={}, tokens: {}".format(
                    tokenized_line.sha256(),
                    str(tokens_before)
                ))
                raise
        builder.save()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Performs semantic analysis on previously tokenized module lines')
    parser.add_argument('-t', '--transpilation', dest='transpilation_directory', required=True,
                        help='The transpilation directory')
    args = parser.parse_args()

    main(args)
