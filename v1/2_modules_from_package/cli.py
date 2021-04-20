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

def get_source_filename(build, source):
    unmodified = str(Path(build) / "files" / (source + ".yapl"))
    if os.path.exists(unmodified):
        return unmodified
    return str(Path(build) / "files" / "modified_locally" / (source + ".yapl"))

def validate_parsed_args(parsed_args):
    if not os.path.isdir(parsed_args.build):
        error("The build parameter must specify a directory file")
        return 1
    if parsed_args.package is not None:
        if not os.path.isfile(get_package_filename(parsed_args.build, parsed_args.package)):
            error("The parameters must specify a package file")
            return 1
    return 0

def main(parsed_args):
    progress("Starting")
    progress("Preparing output directories")
    modules_path = Path(parsed_args.build) / "modules"
    modules_path.mkdir(parents=True, exist_ok=True)
    if parsed_args.force:
        shutil.rmtree(modules_path, ignore_errors=False, onerror=None)
        modules_path.mkdir(parents=True, exist_ok=True)
    if parsed_args.package:
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

def load_sourcefile(build, hash):
    source_filename = get_source_filename(build, hash)
    with io.open(source_filename, "r") as yapl_file:
        return yapl_file.read()


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
    modules_path = Path(build) / "modules"
    n = 1
    for source_filename, sourcefile_info in source_files:
        progress("Processing sourcefile {} ({} of {})".format(source_filename, n, len(source_files)))
        n = n + 1
        revision = sourcefile_info["revision"]
        if os.path.isdir(modules_path / revision):
            # TODO: this can lead to inconsistency
            continue
        def save_modules(build, package_descriptor, source_filename, sourcefile_info):
            revision = sourcefile_info["revision"]
            source_file = load_sourcefile(build, revision)
            lines = source_file.split("\n")
            extractor = None
            parent_metadata = {
                "package":package_descriptor["identifier"],
                "identifier":package_descriptor["identifier"],
                "source": {
                    "filename": source_filename,
                    "revision": revision,
                },
                "symbols": copy.deepcopy(package_descriptor["symbols"])
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
        save_modules(build, package_descriptor, source_filename, sourcefile_info)


class Extractor:
    def __init__(self, parent_metadata, category):
        self._parent_metadata = parent_metadata
        self._metadata = {
            "identifier":None, # to be filled by subclasses
            "category":category,
            "source":parent_metadata["source"],
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
        assert False

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


class FunctionExtractor(Extractor):

    _expression = re.compile(r"^(private\s+){0,1}\s*("
                             r"((function)|(constructor)|(destructor)|(method)|(generator)|(closure))"
                             r"(\-((function)|(constructor)|(destructor)|(method)|(generator)|(closure)))*"
                             r")\s+(.+)")
    _identifier = re.compile(r"\s*([^\(]+)(.*)")

    def __init__(self, parent_metadata, line):
        super().__init__(parent_metadata, "functions")
        m = FunctionExtractor._expression.match(line)
        _private = m.group(1) is not None and m.group(1).startswith("private")
        remainder = m.group(len(m.groups()))
        m = FunctionExtractor._identifier.match(remainder)
        _name = m.group(1)
        remainder = m.group(len(m.groups()))
        self._metadata["identifier"] = parent_metadata["identifier"] + "." + _name
        self._metadata["function"] = {
            "name":_name,
            "private":_private,
        }

    def process_line(self, line):
        if line.startswith("}"):
            return False
        return True

    def save(self, build):
        return


class ModuleFunctionExtractor(FunctionExtractor):

    def __init__(self, parent, line):
        super().__init__(parent._metadata, line)
        parent.declare_symbol("functions", self._metadata["function"]["name"], self._metadata["identifier"])


class VariableExtractor(Extractor):

    _expression = re.compile(r"^(private\s+){0,1}\s*("
                             r"(\w+)\s*:\s*"
                             r"(\w+)\s*"
                             r"((:{0,1}=)\s*(.*))"
                             r")$"
                             )

    def __init__(self, parent_metadata, line):
        super().__init__(parent_metadata, "variables")
        m = VariableExtractor._expression.match(line)
        _private = m.group(1) is not None and m.group(1).startswith("private")
        _name = m.group(3)
        _type = m.group(4)
        _op = m.group(6)
        _mutable = m.group(6) is not None and _op == ":="
        _remainder = m.group(len(m.groups()))
        # TODO: extends
        self._metadata["identifier"] = parent_metadata["identifier"] + "." + _name
        self._metadata["scope"] = parent_metadata["identifier"]
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

    def save(self, build):
        return


class ClassExtractor(Extractor):

    _expression = re.compile(r"^(private\s+){0,1}\s*("
                          r"((abstract\s+class)|(class)|(interface)|(structure))"
                          r")\s+(.+)")
    _identifier = re.compile(r"(\w+).*")

    def __init__(self, parent_metadata, line):
        super().__init__(parent_metadata, "classes")
        m = ClassExtractor._expression.match(line)
        _private = m.group(1) is not None and m.group(1).startswith("private")
        remainder = m.group(len(m.groups()))
        _name = ClassExtractor._identifier.match(remainder).group(1)
        self._metadata["identifier"] = parent_metadata["identifier"] + "." + _name
        self._metadata["class"] = {
            "name":_name,
            "private":_private,
        }

    def save(self, build):
        return


class ModuleClassExtractor(ClassExtractor):

    def __init__(self, parent, line):
        super().__init__(parent._metadata, line)
        self._parent = parent
        parent.declare_symbol("classes", self._metadata["class"]["name"], self._metadata["identifier"])


class ModuleVariableExtractor(VariableExtractor):

    def __init__(self, parent, line):
        super().__init__(parent._metadata, line)
        parent.declare_symbol("variables", self._metadata["variable"]["name"], self._metadata["identifier"])


class TypeExtractor(Extractor):

    _expression = re.compile(r"^(private\s+){0,1}\s*("
                             r"(type)|(alias)"
                             r")\s+(.+)$"
                             )

    _identifier = re.compile(r"\s*([^:\{\(\s=]+)(.*)")

    def __init__(self, parent_metadata, line):
        super().__init__(parent_metadata, "types")
        m = TypeExtractor._expression.match(line)
        _private = m.group(1) is not None and m.group(1).startswith("private")
        remainder = m.group(len(m.groups()))
        m = TypeExtractor._identifier.match(remainder)
        _name = m.group(1)
        self._metadata["identifier"] = parent_metadata["identifier"] + "." + _name
        self._metadata["type"] = {
            "name":_name,
            "private":_private
        }

    def process_line(self, line):
        super().process_line(line)
        return False

    def save(self, build):
        return

class ModuleTypeExtractor(TypeExtractor):

    def __init__(self, parent, line):
        super().__init__(parent._metadata, line)
        parent.declare_symbol("types", self._metadata["type"]["name"], self._metadata["identifier"])

class ModuleExtractor(Extractor):

    _expression = re.compile(r'^((module)|(service)|(process)|(restservice))\s+(\w+)\s*\{\s*$')
    _import = re.compile(r'^\s{4}import\s+(.+)')
    _import_from = re.compile(r'^\s{4}import\s+(.*)\sfrom\s+(.+)')


    def __init__(self, parent_metadata, line):
        super().__init__(parent_metadata, "modules")
        m = ModuleExtractor._expression.match(line)
        _name = m.group(len(m.groups()))
        assert _name == str(Path(parent_metadata["source"]["filename"]).stem)
        self._metadata["identifier"] = parent_metadata["identifier"] + "." + _name
        self._metadata["symbols"] = copy.deepcopy(parent_metadata["symbols"])

    def declare_symbol(self, symbol_category, symbol_name, symbol_identifier):
        self._metadata["symbols"][symbol_name] = symbol_identifier

    def get_filename(self, build):
        return str(Path(build) / "modules" / self._metadata["source"]["revision"] / "module")

    def process_line(self, line):
        if ModuleExtractor._import.match(line):
            m = ModuleExtractor._import.match(line)
            import_from = None
            if ModuleExtractor._import_from.match(line):
                x = ModuleExtractor._import_from.match(line)
                without_from = x.group(1)
                import_from = x.group(2)
            else:
                without_from = m.group(1)
            for symbol in without_from.split(","):
                symbol = symbol.strip()
                if re_has_whitespace.match(symbol):
                    symbol = re.split(r"\s+", symbol)[0]
                if import_from is None:
                    symbol = import_from
                    if import_from in self._metadata["symbols"]:
                        import_from = self._metadata["symbols"][import_from]
                    self.declare_symbol("imports", symbol, import_from)
                else:
                    if symbol == "*":
                        if import_from in self._metadata["symbols"]:
                            import_from = self._metadata["symbols"][import_from]
                        self.declare_symbol("imports", "*." + import_from, import_from + ".*")
                    else:
                        if import_from in self._metadata["symbols"]:
                            import_from = self._metadata["symbols"][import_from]
                        import_from = import_from + "." + symbol
                        self.declare_symbol("imports", symbol, import_from)
            return True
        return super().process_line(line)

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
            elif ModuleFunctionExtractor.matches(line):
                extractor = ModuleFunctionExtractor(self, line)
            elif ModuleClassExtractor.matches(line):
                extractor = ModuleClassExtractor(self, line)
            elif ModuleTypeExtractor.matches(line):
                extractor = ModuleTypeExtractor(self, line)
        if extractor is not None:
            more = extractor.process_line("")
            assert (not more), "expected the extractor to complete"
            extractor.save(build)
        super().save(build)


if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    exit_code = validate_parsed_args(parsed_args)
    if exit_code == 0:
        exit_code = main(parsed_args)
    sys.exit(exit_code)
