#!/usr/bin/env python3
import argparse
import sys
import os
from pathlib import Path
import json
import io
import re

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--package", required=False, help="the namespace of the package to process")
    parser.add_argument("-b", "--build", required=True, help="the path of the build folder")
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

component_types = {
    "module": "modules",
    "service": "services",
    "process": "processes",
    "restservice": "restful_services"
}

def main(parsed_args):
    progress("Starting")
    progress("Preparing output directories")
    modules_path = Path(parsed_args.build) / "components"
    modules_path.mkdir(parents=True, exist_ok=True)
    for component_type in component_types.values():
        component_path = modules_path / component_type
        component_path.mkdir(parents=True, exist_ok=True)
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

def save_structural_component(build, component_metadata, component_lines):
    component_type_plural = component_types[component_metadata["component"]["type"]]
    component_filename = str(Path(build) / "components" / component_type_plural / (component_metadata["component"]["namespace"] + "." + component_metadata["component"]["name"]))
    with io.open(component_filename + ".yapl", "w") as yapl_file:
        yapl_file.write("\n".join(component_lines))
    with io.open(component_filename + ".json", 'w') as metadata_file:
        json.dump(component_metadata, metadata_file, sort_keys=True, indent=4)

def get_export_statement(exportable_type, remainder):
    statement = {
        "type":exportable_type
    }
    if exportable_type not in ("class", "interface", "structure", "singleton"):
        if exportable_type == "function":
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
            re_returns = re.compile(r"\s*returns\s+([^:]+):(.*)")
            m = re_returns.match(remainder)
            if m:
                statement["returns"] = {
                    "id":m.group(1).strip(),
                    "type":m.group(2).strip()
                }
        elif exportable_type == "alias":
            re_wat = re.compile(r"\s*:\s*(.*)")
            statement["for"] = re_wat.match(remainder).group(1)
    return statement

def process_package(build, package):
    progress("Processing package " + package)
    descriptor = load_package(build, package)
    source_files = list(descriptor["source_files"].items())
    n = 1
    re_structural_component = re.compile(r'(\w+)\s+(\w+)\s*\{')
    re_import = re.compile(r'^\s{4}import\s+(.+)')
    re_import_from = re.compile(r'^\s{4}import\s+(.*)\sfrom\s+(.+)')
    re_has_whitespace = re.compile(r"\s+")
    # properties, procedure, test, template, actor, exception
    re_exportable = re.compile(r"^\s{4}("
                               r"(class)|(function)|(interface)|(structure)|(type)|(alias)|(singleton)"
                               r")\s+(.+)")
    re_exportable_identifier = re.compile(r"\s*([^:\{\(\s=]+)(.*)")
    for source_filename, sourcefile_info in source_files:
        progress("Processing sourcefile {} ({} of {})".format(source_filename, n, len(source_files)))
        n = n + 1
        revision = sourcefile_info["revision"]
        source_file = load_sourcefile(build, revision)
        lines = source_file.split("\n")
        component_lines = []
        component_imports = {}
        component_exports = {}
        component_metadata = None
        for line in lines:
            if line.startswith("#!"):
                # ignore hash-bangs
                pass
            elif len(component_lines) > 0:
                component_lines.append(line)
                if re_import.match(line):
                    m = re_import.match(line)
                    import_from = None
                    if re_import_from.match(line):
                        x = re_import_from.match(line)
                        without_from = x.group(1)
                        import_from = x.group(2)
                    else:
                        without_from = m.group(1)
                    for symbol in without_from.split(","):
                        symbol = symbol.strip()
                        if re_has_whitespace.match(symbol):
                            symbol = re.split(r"\s+", symbol)[0]
                        if import_from is None:
                            component_imports[symbol] = "*"
                        elif import_from not in component_imports:
                            component_imports[import_from] = [symbol]
                        else:
                            component_imports[import_from].append(symbol)
                elif re_exportable.match(line):
                    m = re_exportable.match(line)
                    exportable_type = m.group(1)
                    remainder = re_exportable_identifier.match(m.group(9))
                    identifier = remainder.group(1)
                    remainder = remainder.group(2)
                    component_exports[identifier] = get_export_statement(exportable_type, remainder)
                elif line.startswith("}"):
                    save_structural_component(build, component_metadata, component_lines)
                    component_lines = []
                    component_imports = {}
                    component_exports = {}
            elif re_structural_component.match(line):
                m = re_structural_component.match(line)
                component_metadata = {
                    "package":descriptor["package"],
                    "component":{
                        "type": m.group(1),
                        "name": m.group(2),
                        "namespace":descriptor["package"]["namespace"] + "." + str(Path(source_filename).stem)
                    },
                    "source":{
                        "filename":source_filename,
                        "revision":sourcefile_info["revision"]
                    },
                    "imports":component_imports,
                    "exports":component_exports
                }
                component_lines.append(line)

if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    exit_code = validate_parsed_args(parsed_args)
    if exit_code == 0:
        exit_code = main(parsed_args)
    sys.exit(exit_code)
