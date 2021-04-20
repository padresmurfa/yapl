#!/usr/bin/env python3
import argparse
import sys
import os
from pathlib import Path
import json
import io
import re
import tempfile
import shutil
import copy

re_has_whitespace = re.compile(r"\s+")
re_has_indent = re.compile(r"\s{4}\s+")
re_empty_line = re.compile(r"^\s*$")

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--module", required=False, help="the identifier of the module to process")
    parser.add_argument("-p", "--package", required=False, help="the namespace of the package to process")
    parser.add_argument("-b", "--build", required=True, help="the path of the build folder")
    parser.add_argument("-f", "--force", action="store_true", required=False, help="force generation, as opposed to generating only if more recent")
    return parser.parse_args(args)

def error(msg):
    print("[ERROR] " + msg, file=sys.stderr)

def progress(msg):
    print("[PROGRESS] " + msg)

def get_package_filename(build, package):
    return str(Path(build) / "packages" / (package + ".json"))

def get_module_directory(build, module):
    return str(Path(build) / "modules" / module)

def get_module_filename(build, module):
    return str(Path(build) / "modules" / module / "module.json")

def validate_parsed_args(parsed_args):
    if not os.path.isdir(parsed_args.build):
        error("The build parameter must specify a build directory")
        return 1
    if parsed_args.package is not None:
        if not os.path.isfile(get_package_filename(parsed_args.build, parsed_args.package)):
            error("The parameters must specify a package file")
            return 1
    if parsed_args.module is not None:
        if not os.path.isdir(get_module_directory(parsed_args.build, parsed_args.module)):
            error("The parameters must specify a module directory")
            return 1
    return 0

def main(parsed_args):
    progress("Starting")
    progress("Preparing output directories")
    blocks_path = Path(parsed_args.build) / "blocks"
    blocks_path.mkdir(parents=True, exist_ok=True)
    if parsed_args.force:
        shutil.rmtree(blocks_path, ignore_errors=False, onerror=None)
        blocks_path.mkdir(parents=True, exist_ok=True)
    if parsed_args.module:
        process_module(parsed_args.build, parsed_args.module)
    elif parsed_args.package:
        process_package(parsed_args.build, parsed_args.package)
    else:
        packages_path = Path(parsed_args.build) / "packages"
        packages = list(packages_path.glob("*.json"))
        n = 1
        for package in packages:
            progress("Processing package {} ({} of {})".format(package, n, len(packages)))
            n = n + 1
            process_package(parsed_args.build, Path(package).stem)
    progress("Finished")
    return 0

def load_package(build, package):
    package_filename = get_package_filename(build, package)
    with io.open(package_filename) as json_file:
        return json.load(json_file)

def load_module(build, hash):
    source_filename = get_module_filename(build, hash)
    with io.open(source_filename, "r") as json_file:
        return json.load(json_file)

def load_class(build, module, class_name):
    filename = str(Path(build) / "modules" / module / "classes" / class_name / "class.json")
    with io.open(filename, "r") as json_file:
        return json.load(json_file)

def load_json_and_code(filename):
    with io.open(filename + ".json", "r") as json_file:
        result = json.load(json_file)
    with io.open(filename + ".yapl", "r") as yapl_file:
        code = yapl_file.read()
    result["source"]["code"] = code
    return result

def load_member(mtype, build, module, class_name, member_name):
    filename = str(Path(build) / "modules" / module / "classes" / class_name / mtype / member_name)
    return load_json_and_code(filename)

def load_function(build, module, function_name):
    filename = str(Path(build) / "modules" / module / "functions" / function_name)
    return load_json_and_code(filename)

def load_property_accessor(build, module, class_name, property_name, property_accessor):
    gs = "get_" if property_accessor == "getter" else "set_"
    filename = str(Path(build) / "modules" / module / "classes" / class_name / "properties" / (gs + property_name))
    return load_json_and_code(filename)

def dedent(l):
    if l == "":
        return l
    elif l[0] == "\t":
        return l[1:]
    elif l[:4] == "    ":
        return l[4:]
    elif l.strip() == "":
        return ""
    else:
        assert False, "expected leading whitespace, not '{}'".format(l)
        return l

def process_package(build, package):
    progress("Processing package " + package)
    package_descriptor = load_package(build, package)
    source_files = list(package_descriptor["source_files"].items())
    blocks_path = Path(build) / "blocks"
    n = 1
    for source_filename, sourcefile_info in source_files:
        progress("Processing sourcefile {} ({} of {})".format(source_filename, n, len(source_files)))
        n = n + 1
        revision = sourcefile_info["revision"]
        if os.path.isdir(blocks_path / revision):
            # TODO: this can lead to inconsistency
            continue
        module = load_module(build, revision)
        classes = list(module["classes"].items())
        m = 1
        for class_name, class_info in classes:
            progress("Processing class {} ({} of {})".format(class_name, m, len(classes)))
            m = m + 1
            _class = load_class(build, revision, class_name)
            for member_type in ["constructors", "destructors", "methods"]:
                for member_name in _class["class"][member_type].keys():
                    member = load_member(member_type, build, revision, class_name, member_name)
                    process_member(build, package, module, _class, member_name, member)
            for property_name, property_info in _class["class"]["properties"].items():
                for property_accessor in ["getter", "setter"]:
                    if property_accessor in property_info:
                        accessor = load_property_accessor(build, revision, class_name, property_name, property_accessor)
                        process_accessor(build, package, module, _class, property_name, property_accessor, accessor)
        functions = list(module["functions"].items())
        m = 1
        for function_name, function_info in functions:
            progress("Processing function {} ({} of {})".format(function_name, m, len(functions)))
            m = m + 1
            function = load_function(build, revision, function_name)
            process_function(build, package, module, function_name, function)


class Extractor:
    def __init__(self, parent_metadata, category):
        self._parent_metadata = parent_metadata
        self._metadata = {
            "identifier":None, # to be filled by subclasses
            "category":category,
            "source":copy.deepcopy(parent_metadata["source"]),
        }
        if "module" in parent_metadata:
            self._metadata["module"] = parent_metadata["module"]
        elif "package" in parent_metadata:
            self._metadata["package"] = parent_metadata["package"]
        self._lines = []

    def process_line(self, line):
        if line.startswith("}"):
            return False
        self._lines.append(dedent(line))
        return True

    def get_path(self, build):
        _filename = self.get_filename(build)
        _path = Path(_filename).parents[0]
        _path.mkdir(parents=True, exist_ok=True)
        return str(_path)

    def get_filename(self, build):
        return str(Path(build) / "modules" / self._metadata["source"]["revision"] / self._metadata["category"] / self._metadata["identifier"])

    def save(self, build):
        _filename = self.get_filename(build)
        _path = self.get_path(build)
        Path(_path).mkdir(parents=True, exist_ok=True)
        def strip_empty_lines(lines):
            # this is a brute force evil algorithm, fix this one day.
            while lines and re_empty_line.match(lines[0]):
                lines.pop(0)
            while lines and re_empty_line.match(lines[-1]):
                lines.pop(-1)
            lines.append("")
            return lines
        _lines = strip_empty_lines(self._lines)
        with io.open(_filename + ".yapl", "w") as yapl_file:
            yapl_file.write("\n".join(strip_empty_lines(_lines)))
        with io.open(_filename + ".json", 'w') as metadata_file:
            json.dump(self._metadata, metadata_file, sort_keys=True, indent=4)

    @classmethod
    def matches(cls, line):
        m = cls._expression.match(line)
        return m is not None and m and True

_reserved_words = {
    "true", "false",
    "and", "or", "xor", "not",
    "null", "undefined",
    "if", "else", "import", "from",
    "assert",
    "try", "catch", "finally", "throw",
    "for", "while", "repeat", "until", "in",
    "block", "scope",
    "function", "coroutine", "return", "returns", "method", "procedure", "classmethod", "staticmethod",
    "class", "interface", "abstract", "structure",
    "this", "args",
    "extends", "implements", "reifies",
    "public", "private", "protected", "overridable", "override", "overrides",
    "continue", "break", "pass",
    "is","as",
    "type","alias",
    "generator","yield", "yields",
    "lazy","singleton",
    "constructor","destructor",
    "new", "delete", "release", "claim", "give",
    "superclass", "subclass",
    "let", "const", "constant",
    "switch", "case",
    "optional", "some", "none",
    "enumeration",
    "shared",
    "bool", "boolean", "exception",
    "float32", "float64",
    "complex64", "complex128",
    "real", "number",
    "rational32", "rational64", "rational128",
    "decimal", "decimal32", "decimal64", "decimal128",
    "integer", "int", "int8", "int16", "int32", "int64",
    "unsigned", "uint", "uint8", "uint16", "uint32", "uint64",
    "byte", "char", "character",
    "bits", "bit",
    "bitwise_or", "bitwise_not", "bitwise_and", "bitwise_xor", "bitwise_ffs", "bitwise_ctz", "bitwise_ntz",
    "bitwise_popcount", "bitwise_shift", #(https://en.wikipedia.org/wiki/Bitwise_operation)
    "time", "date", "moment", "interval", "timezone",
    "millenium", "milleniums", "century", "centuries",
    "year", "years", "month", "months", "day", "days", "hour", "hours", "minute", "minutes", "second", "seconds",
    "millisecond", "milliseconds", "nanosecond", "nanoseconds",
    "utc", "now",
    "identifier",
    "unicode", "ascii",
    "string", "filename", "uri", "url",
    "lambda", "global", "with",
    "serialise", "deserialise", "serialize", "deserialize",
    "modulo", "pow",
    "collection", "array", "map", "iterator", "list", "set", "tuple", "queue", "hashtable", "bag", "heap", "stack",
    "test", "testsuite", "mock",
    "each",
    "mutable", "immutable", "readonly",
    "transaction", "commit", "rollback",
    "using",
    "lock",
    "pointer", "dereference",
    "implicit",
    "property", "getter", "setter",
    "async", "await", "run",
    "template",
    "trait", "mixin", "sealed",
    "actor", "select",
    "channel", "send", "receive",
    "thread", "fiber",
    "sensitive",
    "goto", "label",
    "function_body",
}

def is_reserved_word(word):
    return word in _reserved_words

_non_identifier = re.compile("^\s*([^\w\.]+)(.*)$")
_identifier = re.compile("^\s*([a-zA-Z][\w\.]*)(.*)$")
def extract_identifiers(line):
    remainder = line
    while remainder:
        m = _identifier.match(remainder)
        if not m:
            m = _non_identifier.match(remainder)
            if not m:
                break
            else:
                remainder = m.group(2)
                continue
        i = m.group(1)
        if not is_reserved_word(i):
            yield i
        remainder = m.group(2)

class BlockStatementExtractor(Extractor):

    _block_id = 0

    _expression = re.compile(r"^("
                             r"(if)|(else\s+if)|(else)"
                             r"|(try)|(catch)|(finally)"
                             r"|(switch)|(case)|(default)"
                             r"|(for)|(while)|(until)|(repeat)"
                             r")\s*([^\{]*)\{\s*$")

    _repeat_expression = re.compile(r"^\}\s*("
                                r"(while)|(until)"
                                r")\s*(.*)$")

    @staticmethod
    def type_from_line(line):
        m = BlockStatementExtractor._expression.match(line)
        return re.sub(r"else\s+if", "else if", m.group(1))

    def __init__(self, parent_metadata, line, _type = None, _remainder = None):
        super().__init__(parent_metadata, "blocks")
        if _type is None:
            _type = BlockStatementExtractor.type_from_line(line)
            m = BlockStatementExtractor._expression.match(line)
            _remainder = m.group(len(m.groups())).strip()
        _id = str(BlockStatementExtractor._block_id)
        BlockStatementExtractor._block_id += 1
        self._subblocks = []
        self._current_subblock = None
        self._metadata["block"] = {
            "type":_type,
            "id":_id,
            "symbols":{}
        }
        self._remainder = _remainder
        if "source" in parent_metadata and "callable" in parent_metadata["source"]:
            self._metadata["source"]["callable"] = parent_metadata["source"]["callable"]
        else:
            self._metadata["source"]["callable"] = parent_metadata["identifier"]
        self._metadata["identifier"] = self._metadata["source"]["callable"] + "." + _id
        self._lines.append(line)

    def get_caller_statement(self):
        _type = self._metadata["block"]["type"]
        _remainder = self._remainder
        _blockid = self._metadata["block"]["id"]
        if _remainder:
            result = "{} {} ${}".format(_type, _remainder, _blockid)
        else:
            result = "{} ${}".format(_type, _blockid)
        if "repeat_criteria" in self._metadata['block']:
            result = result + " " + self._metadata['block']["repeat_criteria"]
        return result

    def process_line(self, line):
        if line.startswith("}"):
            if BlockStatementExtractor._repeat_expression.match(line):
                m = BlockStatementExtractor._repeat_expression.match(line)
                self._lines.append("} " + m.group(1) + " " + m.group(len(m.groups())))
                self._metadata["block"]["repeat_criteria"] = m.group(1) + " " + m.group(len(m.groups()))
            else:
                self._lines.append("}")
            return False
        dline = dedent(line)
        if self._current_subblock is not None:
            r = self._current_subblock.process_line(dline)
            if not r:
                self._lines.append("    " + self._current_subblock.get_caller_statement())
                if ContinuationBlockStatementExtractor.matches(self._current_subblock, dline):
                    self._current_subblock = ContinuationBlockStatementExtractor(self._metadata, dline)
                    self._subblocks.append(self._current_subblock)
                else:
                    self._current_subblock = None
            return True
        elif BlockStatementExtractor.matches(dline):
            self._current_subblock = BlockStatementExtractor(self._metadata, dline)
            self._subblocks.append(self._current_subblock)
            return True
        else:
            self._lines.append(line)
            return True

    def save(self, build):
        symbols = self._metadata["block"]["symbols"]
        for line in self._lines:
            for identifier in extract_identifiers(line):
                if identifier not in symbols:
                    symbols[identifier] = {}
        for s in self. _subblocks:
            s.save(build)
        super().save(build)

    def get_path(self, build):
        t = self._metadata["block"]["type"]
        fname = str(self._metadata["source"]["callable"])
        if t == "property_getter":
            fname += ".getter"
        elif t == "property_setter":
            fname += ".setter"
        return str(Path(build) / "blocks" / self._metadata["source"]["revision"] / fname)

    def get_filename(self, build):
        _path = self.get_path(build)
        return str(Path(_path) / self._metadata["block"]["id"])

class ContinuationBlockStatementExtractor(BlockStatementExtractor):

    _expression = re.compile(r"^\}\s*("
                              r"(else\s+if)|(else)"
                              r"|(catch)|(finally)"
                              r")\s*([^\{]*)\{\s*$")

    _continuation_expressions_by_expression = {
        "if":["elif", "else"],
        "else if":["else"],
        "try":["catch", "finally"],
        "catch":["finally"],
    }

    def __init__(self, parent_metadata, line):
        super().__init__(parent_metadata, line[1:].strip())

    @classmethod
    def matches(cls, parent, line):
        m = ContinuationBlockStatementExtractor._expression.match(line)
        if m:
            t = parent._metadata["block"]["type"]
            if t in ContinuationBlockStatementExtractor._continuation_expressions_by_expression:
                allowed = ContinuationBlockStatementExtractor._continuation_expressions_by_expression[t]
                _type = BlockStatementExtractor.type_from_line(line[1:].strip())
                return _type in allowed
        return super().matches(line)

    def save(self, build):
        for s in self. _subblocks:
            s.save(build)
        super().save(build)

class FunctionBlockStatementExtractor(BlockStatementExtractor):

    _expression = re.compile(r"^\s*[^\{]*\{\s*$")

    _repeat_expression = re.compile(r"^\}\s*("
                                r"(while)|(until)"
                                r")\s*(.*)$")

    def __init__(self, metadata, line):
        if "property" in metadata:
            super().__init__(metadata, line, "property_" + metadata['property']["type"], metadata['property']["name"])
        else:
            super().__init__(metadata, line, metadata["function"]["type"], metadata['function']["name"])
        self._metadata["identifier"] = metadata["identifier"]

    def process_line(self, line):
        if line.startswith("}"):
            self._lines.append("}")
            return False
        dline = dedent(line)
        if self._current_subblock is not None:
            r = self._current_subblock.process_line(dline)
            if not r:
                self._lines.append("    " + self._current_subblock.get_caller_statement())
                if ContinuationBlockStatementExtractor.matches(self._current_subblock, dline):
                    self._current_subblock = ContinuationBlockStatementExtractor(self._metadata, dline)
                    self._subblocks.append(self._current_subblock)
                else:
                    self._current_subblock = None
            return True
        elif BlockStatementExtractor.matches(dline):
            self._current_subblock = BlockStatementExtractor(self._metadata, dline)
            self._subblocks.append(self._current_subblock)
            return True
        else:
            self._lines.append(line)
            return True

    def save(self, build):
        for s in self._subblocks:
            s.save(build)
        super().save(build)

    def get_filename(self, build):
        _path = self.get_path(build)
        return str(Path(_path) / "body")


def extract_blocks_from_function(build, metadata):
    code = metadata["source"]["code"]
    metadata = copy.deepcopy(metadata)
    del metadata["source"]["code"]
    lines = code.split("\n")
    header = lines[0]
    footer = lines[-1]
    body = [dedent(line) for line in lines[1:-1] if re_has_whitespace.match(line)]
    extractor = FunctionBlockStatementExtractor(metadata, header)
    for line in lines[1:]:
        if re_empty_line.match(line):
            continue
        if not extractor.process_line(line):
            extractor.save(build)
            extractor = None


def process_member(build, package, module, _class, member_name, member):
    extract_blocks_from_function(build, member)

def process_accessor(build, package, module, _class, property_name, property_accessor, accessor):
    extract_blocks_from_function(build, accessor)

def process_function(build, package, module, function_name, function):
    extract_blocks_from_function(build, function)


if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    exit_code = validate_parsed_args(parsed_args)
    if exit_code == 0:
        exit_code = main(parsed_args)
    sys.exit(exit_code)
