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
    classes_path = Path(parsed_args.build) / "classes"
    classes_path.mkdir(parents=True, exist_ok=True)
    if parsed_args.force:
        shutil.rmtree(classes_path, ignore_errors=False, onerror=None)
        classes_path.mkdir(parents=True, exist_ok=True)
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

def describe(exportable_type, remainder):
    statement = {
        "type":exportable_type
    }
    if exportable_type not in ("class", "interface", "structure", "singleton"):
        if exportable_type == "function" or exportable_type == "method":
            statement["params"] = {}
            re_params = re.compile(r"\s*\(([^\)]*)\)\s*([^\{]*){")
            m = re_params.match(remainder)
            params = m.group(1).strip()
            remainder = m.group(2).strip()
            re_param = re.compile(r"([^\:]+)\:\s*([^,]*),?(.*)")
            while re_param.match(params):
                m = re_param.match(params)
                param_id = m.group(1).strip()
                param_type = m.group(2).strip()
                params = m.group(3).strip()
                statement["params"][param_id] = {
                    "type":param_type,
                    "ordinal":len(statement["params"])
                }
                re_param_default_value = re.compile(r"([^=]+)=(.*)")
                if re_param_default_value.match(param_type):
                    m = re_param_default_value.match(param_type)
                    param_type = m.group(1).strip()
                    statement["params"][param_id]["type"] = param_type
                    param_default = m.group(2).strip()
                    statement["params"][param_id]["default_value"] = param_default
            re_returns = re.compile(r"\s*((returns)|(yields))\s+([^:]+):(.*)")
            m = re_returns.match(remainder)
            if m:
                return_type = "yields" if m.group(1) == "yields" else "returns"
                statement[return_type] = {
                    "id":m.group(4).strip(),
                    "type":m.group(5).strip()
                }
        elif exportable_type == "alias":
            re_wat = re.compile(r"\s*:\s*(.*)")
            statement["for"] = re_wat.match(remainder).group(1)
    return statement

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
        return str(Path(build) / "classes" / self._metadata["source"]["revision"] / self._metadata["identifier"])

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


class ClassMethodExtractor(Extractor):

    _expression = re.compile(r"^(private\s+){0,1}("
                             r"((constructor)|(destructor)|(method))"
                             r"(\-((constructor)|(destructor)|(method)|(generator)|(closure)))*"
                             r")\s+(.+)")
    _identifier = re.compile(r"\s*([^\(]+)(.*)")

    def __init__(self, parent, line):
        super().__init__(parent._metadata, "methods")
        self._parent = parent
        m = ClassMethodExtractor._expression.match(line)
        _private = m.group(1) is not None and m.group(1).startswith("private")
        def normalize_function_type(types):
            t = types.split("-")
            t.sort()
            return "-".join(t)
        _type = normalize_function_type(m.group(2))
        remainder = m.group(len(m.groups()))
        m = ClassMethodExtractor._identifier.match(remainder)
        _name = m.group(1)
        remainder = m.group(len(m.groups()))
        description = describe("method", remainder)
        _identifier = parent._metadata["identifier"] + "." + _name
        self._metadata["identifier"] = _identifier
        self._metadata["class"] = parent._metadata["identifier"]
        self._metadata["symbols"][_name] = self._metadata["identifier"]
        self._metadata["method"] = {
            "type":_type,
            "name":_name,
            "private":_private,
            "params":description["params"],
        }
        if "returns" in description:
            self._metadata["method"]["returns"] = description["returns"]
        elif "yields" in description:
            self._metadata["method"]["yields"] = description["yields"]
        parent._metadata["class"][self._get_subcategory()][_name] = self._metadata["identifier"]
        parent.declare_symbol("methods", _name, _identifier)

    def process_line(self, line):
        if line.startswith("}"):
            return False
        return True

    def _get_subcategory(self):
        t = self._metadata["method"]["type"]
        if "constructor" in t:
            return "constructors"
        elif "destructor" in t:
            return "destructors"
        else:
            return "methods"

    def save(self, build):
        pass

class ClassVariableExtractor(Extractor):

    _expression = re.compile(r"^(private\s+){0,1}\s*("
                             r"(\w+)\s*:\s*"
                             r"(\w+)\s*"
                             r"((:{0,1}=)\s*(.*))"
                             r")$"
                             )

    def __init__(self, parent, line):
        super().__init__(parent._metadata, "variables")
        self._parent = parent
        m = ClassVariableExtractor._expression.match(line)
        _private = m.group(1) is not None and m.group(1).startswith("private")
        _name = m.group(3)
        _type = m.group(4)
        _op = m.group(6)
        _mutable = m.group(6) is not None and _op == ":="
        _remainder = m.group(len(m.groups()))
        # TODO: extends
        _identifier = parent._metadata["identifier"] + "." + _name
        parent._metadata["class"]["members"][_name] = _identifier
        parent.declare_symbol("members", _name, _identifier)

    def process_line(self, line):
        if re_has_indent.match(line):
            return True
        return False

    def save(self, build):
        pass

class ClassPropertyExtractor(Extractor):

    _expression = re.compile(r"^(private\s+){0,1}\s*("
                             r"(getter)|(setter)"
                             r")\s*(.+)$")
    _identifier = re.compile(r"\s*([^\:\=]+)(.*)$")

    def __init__(self, parent, line):
        super().__init__(parent._metadata, line)
        self._parent = parent
        m = ClassPropertyExtractor._expression.match(line)
        _private = m.group(1) is not None and m.group(1).startswith("private")
        _type = m.group(2)
        remainder = m.group(len(m.groups()))
        m = ClassPropertyExtractor._identifier.match(remainder)
        _name = m.group(1)
        _identifier = parent._metadata["identifier"] + "." + _name
        p = parent._metadata["class"]["properties"]
        if _name not in p:
            p[_name] = {}
        p[_name][_type] = _identifier
        remainder = m.group(len(m.groups()))
        parent.declare_symbol("properties", _name, _identifier)

    def process_line(self, line):
        if line.startswith("}"):
            return False
        return True

    def save(self, build):
        pass


class ModuleClassExtractor(Extractor):

    _expression = re.compile(r"^(private\s+){0,1}\s*("
                          r"((abstract\s+class)|(class)|(interface)|(structure))"
                          r")\s+(.+)")
    _identifier = re.compile(r"(\w+).*")

    def __init__(self, parent, line):
        super().__init__(parent._metadata, "classes")
        self._parent = parent
        m = ModuleClassExtractor._expression.match(line)
        _private = m.group(1) is not None and m.group(1).startswith("private")
        _type = m.group(2)
        remainder = m.group(len(m.groups()))
        _name = ModuleClassExtractor._identifier.match(remainder).group(1)
        # TODO: extends
        self._metadata["identifier"] = parent._metadata["identifier"] + "." + _name
        self._metadata["symbols"] = copy.deepcopy(parent._metadata["symbols"])
        self._metadata["module"] = parent._metadata["identifier"]
        self._metadata["class"] = {
            "type":_type,
            "name":_name,
            "private":_private,
            "properties":{},
            "constructors":{},
            "destructors":{},
            "methods":{},
            "members":{}
        }

    def declare_symbol(self, symbol_category, symbol_name, symbol_identifier):
        self._metadata["symbols"][symbol_name] = symbol_identifier

    def get_path(self, build):
        _path = str(Path(build) / "classes" / self._metadata["source"]["revision"] / self._metadata["class"]["name"])
        return str(_path)

    def get_filename(self, build):
        _path = str(Path(self.get_path(build)) / "class")
        return str(_path)

    def save(self, build):
        _path = self.get_path(build)
        _filename = self.get_filename(build)
        extractor = None
        for line in self._lines:
            if extractor is None and re_has_indent.match(line):
                continue
            if extractor is not None:
                if not extractor.process_line(line):
                    extractor.save(build)
                    extractor = None
            elif ClassVariableExtractor.matches(line):
                extractor = ClassVariableExtractor(self, line)
            elif ClassMethodExtractor.matches(line):
                extractor = ClassMethodExtractor(self, line)
            elif ClassPropertyExtractor.matches(line):
                extractor = ClassPropertyExtractor(self, line)
        if extractor is not None:
            more = extractor.process_line("")
            assert (not more), "expected the extractor to complete"
            extractor.save(build)
        super().save(build)


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
            elif ModuleClassExtractor.matches(line):
                extractor = ModuleClassExtractor(self, line)
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
