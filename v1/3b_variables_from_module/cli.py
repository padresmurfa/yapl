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

re_has_indent = re.compile(r"\s{4}\s+")
re_empty_line = re.compile(r"^\s*$")

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--module", required=False, help="the module to process")
    parser.add_argument("-b", "--build", required=True, help="the path of the build folder")
    parser.add_argument("-f", "--force", action="store_true", required=False, help="force generation, as opposed to generating only if more recent")
    return parser.parse_args(args)

def error(msg):
    print("[ERROR] " + msg, file=sys.stderr)

def progress(msg):
    print("[PROGRESS] " + msg)

def get_module_filename(build, module):
    return str(Path(build) / "modules" / module / "module.json")

def get_source_filename(build, source):
    unmodified = str(Path(build) / "files" / (source + ".yapl"))
    if os.path.exists(unmodified):
        return unmodified
    return str(Path(build) / "files" / "modified_locally" / (source + ".yapl"))

def validate_parsed_args(parsed_args):
    if not os.path.isdir(parsed_args.build):
        error("The build parameter must specify a directory file")
        return 1
    if parsed_args.module is not None:
        if not os.path.isfile(get_module_filename(parsed_args.build, parsed_args.module)):
            error("The parameters must specify a module file")
            return 1
    return 0

def main(parsed_args):
    progress("Starting")
    progress("Preparing output directories")
    variables_path = Path(parsed_args.build) / "variables"
    variables_path.mkdir(parents=True, exist_ok=True)
    if parsed_args.force:
        shutil.rmtree(variables_path, ignore_errors=False, onerror=None)
        variables_path.mkdir(parents=True, exist_ok=True)
    if parsed_args.module:
        process_module(parsed_args.build, parsed_args.module)
    else:
        modules_path = Path(parsed_args.build) / "modules"
        modules = list(modules_path.glob("*"))
        n = 1
        for module in modules:
            progress("Processing module {} ({} of {})".format(module, n, len(modules)))
            n = n + 1
            process_module(parsed_args.build, Path(module).stem)
    progress("Finished")
    return 0

def load_sourcefile(build, hash):
    source_filename = get_source_filename(build, hash)
    with io.open(source_filename, "r") as yapl_file:
        return yapl_file.read()

def load_module(build, module):
    module_filename = get_module_filename(build, module)
    with io.open(module_filename) as json_file:
        return json.load(json_file)

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

def process_module(build, revision):
    progress("Processing module " + revision)
    if not os.path.isfile(get_module_filename(build, revision)):
        return
    module = load_module(build, revision)
    source_file = load_sourcefile(build, revision)
    lines = source_file.split("\n")
    extractor = None
    parent_metadata = {
        "identifier":module["package"],
        "source": module["source"],
        "symbols": copy.deepcopy(module["symbols"])
    }
    for line in lines:
        if line.startswith("#!"):
            # ignore hash-bangs
            pass
        elif extractor is None and re_has_indent.match(line):
            pass
        elif extractor is not None:
            if not extractor.process_line(line):
                extractor.save(build)
                extractor = None
        elif ModuleExtractor.matches(line):
            extractor = ModuleExtractor(parent_metadata, line)
    if extractor is not None:
        more = extractor.process_line("")
        assert (not more), "expected the extractor to complete"
        extractor.save(build)


class Extractor:
    def __init__(self, parent_metadata, category):
        self._parent_metadata = parent_metadata
        self._metadata = {
            "identifier":None, # to be filled by subclasses
            "category":category,
            "source":parent_metadata["source"],
            "symbols":copy.deepcopy(parent_metadata["symbols"])
        }
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
        return str(Path(build) / "variables" / self._metadata["source"]["revision"] / self._metadata["identifier"])

    def save(self, build):
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
        _filename = self.get_filename(build)
        with io.open(_filename + ".yapl", "w") as yapl_file:
            yapl_file.write("\n".join(strip_empty_lines(_lines)))
        with io.open(_filename + ".json", 'w') as metadata_file:
            json.dump(self._metadata, metadata_file, sort_keys=True, indent=4)

    @classmethod
    def matches(cls, line):
        m = cls._expression.match(line)
        return m is not None and m and True


class ModuleVariableExtractor(Extractor):

    _expression = re.compile(r"^(private\s+){0,1}("
                             r"(\w+)\s*:\s*"
                             r"(\w+)\s*"
                             r"((:{0,1}=)\s*(.*))"
                             r")$"
                             )

    def __init__(self, parent, line):
        super().__init__(parent._metadata, "variables")
        self._parent = parent
        m = ModuleVariableExtractor._expression.match(line)
        _private = m.group(1) is not None and m.group(1).startswith("private")
        _name = m.group(3)
        _type = m.group(4)
        _op = m.group(6)
        _mutable = m.group(6) is not None and _op == ":="
        _remainder = m.group(len(m.groups()))
        # TODO: extends
        self._metadata["identifier"] = parent._metadata["identifier"] + "." + _name
        self._metadata["module"] = parent._metadata["identifier"]
        self._metadata["variable"] = {
            "type":_type,
            "name":_name,
            "private":_private,
            "mutable":_mutable
        }
        self._lines.append("{}:{} {} {}".format(_name, _type, _op, _remainder))

    def process_line(self, line):
        if re_has_indent.match(line):
            self._lines.append(dedent(line))
            return True
        return False

    def get_path(self, build):
        return str(Path(self._parent.get_path(build)))

    def get_filename(self, build):
        _path = self.get_path(build)
        return str(Path(_path) / self._metadata["variable"]["name"])


class ModuleExtractor(Extractor):

    _expression = re.compile(r'^((module)|(service)|(process)|(restservice))\s+(\w+)\s*\{\s*$')

    def __init__(self, parent_metadata, line):
        super().__init__(parent_metadata, "modules")
        m = ModuleExtractor._expression.match(line)
        _name = m.group(len(m.groups()))
        assert _name == str(Path(parent_metadata["source"]["filename"]).stem)
        self._metadata["identifier"] = parent_metadata["identifier"] + "." + _name

    def save(self, build):
        extractor = None
        for line in self._lines:
            if extractor is None and re_has_indent.match(line):
                continue
            if extractor is not None:
                if not extractor.process_line(line):
                    extractor.save(build)
                    extractor = None
            elif ModuleVariableExtractor.matches(line):
                extractor = ModuleVariableExtractor(self, line)
        if extractor is not None:
            more = extractor.process_line("")
            assert (not more), "expected the extractor to complete"
            extractor.save(build)


if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    exit_code = validate_parsed_args(parsed_args)
    if exit_code == 0:
        exit_code = main(parsed_args)
    sys.exit(exit_code)
