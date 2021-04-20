#!/usr/bin/env python3
import argparse
import sys
import os
import time
from datetime import datetime
import shutil
from pathlib import Path
import yapl.repository.git.lib as git
import json
import io
import yapl

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="the path of the repository to process")
    parser.add_argument("-o", "--output", required=True, help="the path of the output folder")
    parser.add_argument("-a", "--authority", required=True, help="the directly responsible organisation, and/or individual, that produced the package")
    parser.add_argument("-f", "--force", action="store_true", required=False, help="force generation, as opposed to generating only if more recent")
    parser.add_argument("-r", "--root", required=True, help="the root namespace of the output package")
    return parser.parse_args(args)

def error(msg):
    print("[ERROR] " + msg, file=sys.stderr)

def progress(msg):
    print("[PROGRESS] " + msg)

def validate_parsed_args(parsed_args):
    is_input_directory = os.path.isdir(parsed_args.input)
    if not is_input_directory:
        error("The input parameter ({}) must specify a directory".format(parsed_args.input))
        return 2
    Path(parsed_args.output).mkdir(parents=True, exist_ok=True)
    is_output_directory = os.path.isdir(parsed_args.output)
    if not is_output_directory:
        error("The output parameter ({}) must specify a directory".format(parsed_args.output))
        return 3
    return 0

def _get_local_changes(source_folder):
    local_root = str(git.get_root_relative_path_of(source_folder))
    local_changes = git.get_locally_changed_files_from_path(source_folder)
    changed = {}
    for hash, filename in local_changes:
        if filename.startswith(local_root):
            test = filename[len(local_root):]
            if test.startswith(os.path.sep):
                test = test[1:]
            if os.path.sep not in test:
                changed[filename] = hash
    return changed

def _copy_file(source_filename, files_folder, root, metadata, symbols, locally_changed=False):
    metadata_files = metadata["source_files"]
    source_path = Path(source_filename)
    if source_path.suffix != ".yapl":
        return
    local = str(Path(source_path.name).stem)
    source = git.get_hash_of_file(source_filename, root)
    if source is None:
        if Path(source_filename).is_file():
            os.remove(source_filename)
    else:
        destination_filename = Path(files_folder)
        if locally_changed:
            destination_filename = destination_filename / "modified_locally"
        destination_filename = destination_filename / (source + ".yapl")
        if not destination_filename.is_file():
            progress("copying {} -> {}".format(source_filename, destination_filename))
            shutil.copyfile(source_filename, destination_filename)
        metadata_files[local] = {
            "revision": source
        }
        symbols[local] = metadata["identifier"] + "." + local
        if locally_changed:
            modified_seconds_since_epoch = os.path.getmtime(source_filename)
            modified_datetime = datetime.fromtimestamp(modified_seconds_since_epoch)
            modified_time = modified_datetime.astimezone().replace(microsecond=0).isoformat()
            metadata_files[local]["modified_locally"] = modified_time

def _copy_all_changed_files(source_folder, files_folder, root, metadata, symbols):
    done = {}
    local_changes = _get_local_changes(source_folder)
    check = True
    while check:
        check = False
        for relative_filename, hash in local_changes.items():
            if hash is None:
                key = "<none>/" + relative_filename
            else:
                key = hash + "/" + relative_filename
            if key not in done:
                absolute_filename = str(Path(root) / relative_filename)
                _copy_file(absolute_filename, files_folder, root, metadata, symbols, locally_changed=True)
                done[key] = True
                check = True

def _handle_dir(source_folder, files_folder, root, metadata, locally_changed_files, symbols):
    entries = list(Path(source_folder).glob("*.yapl"))
    if len(entries) > 0:
        progress("Processing unchanged files")
        n = 1
        for entry in entries:
            source_absolute = str(entry)
            source_relative = os.path.relpath(source_absolute, root)
            progress("Processing {} (file {} of {})".format(source_relative, n, len(entries)))
            n = n + 1
            if source_relative not in locally_changed_files:
                _copy_file(source_absolute, files_folder, root, metadata, symbols)
    if len(entries) > 0 or len(locally_changed_files) > 0:
        progress("Processing changed files")
        _copy_all_changed_files(source_folder, files_folder, root, metadata, symbols)
        progress("Done processing changed files")
    for yapl_file in Path(source_folder).glob("**/*.yapl"):
        source_absolute = str(yapl_file)
        source_relative = os.path.relpath(source_absolute, source_folder)
        p = Path(source_relative)
        parent = str(p.parent).replace(os.path.sep, ".")
        if parent != ".":
            source_relative = os.path.relpath(source_absolute, source_folder)
            p = Path(source_relative)
            parent = str(p.parent)
            stem = p.stem
            full_path = metadata["identifier"] + "." + str(parent + "." + stem).replace(os.path.sep, ".")
            symbols[parent + "." + stem] = full_path

def main(parsed_args):
    input_path = parsed_args.input
    output_path = parsed_args.output
    progress("Checking preconditions")
    assert git.is_installed(), "Expected git to be installed"
    assert git.is_path_in_repository(input_path), "Expected input to be in a git repository"
    root = str(git.get_root_from_path(input_path))
    progress("Starting")
    progress("Preparing output directories")
    files_path = Path(output_path) / "files"
    Path(files_path).mkdir(parents=True, exist_ok=True)
    if parsed_args.force:
        shutil.rmtree(files_path, ignore_errors=False, onerror=None)
        files_path.mkdir(parents=True, exist_ok=True)
    (files_path / "modified_locally").mkdir(parents=True, exist_ok=True)
    Path(files_path).mkdir(parents=True, exist_ok=True)
    packages_path = Path(output_path) / "packages"
    Path(packages_path).mkdir(parents=True, exist_ok=True)
    if parsed_args.force:
        shutil.rmtree(packages_path, ignore_errors=False, onerror=None)
        packages_path.mkdir(parents=True, exist_ok=True)
    progress("Determining locally changed files")
    locally_changed_files = _get_local_changes(input_path)
    progress("Preparing list of directories to process")
    if not git.is_path_ignored(input_path, root):
        paths = [ input_path ]
        for parent_dir, subdirectories, file in os.walk(input_path):
            for subdirectory in subdirectories:
                package_path = os.path.join(parent_dir,subdirectory)
                if not git.is_path_ignored(package_path, root):
                    paths.append(package_path)
        n = 1
        for package_path in paths:
            progress("Processing {} ({} of {})".format(package_path, n, len(paths)))
            n = n + 1
            process_package(package_path, files_path, packages_path, root, locally_changed_files)
    progress("Finished")

def process_package(input_path, files_path, packages_path, root, locally_changed_files):
    source_files = {}
    symbols = {}
    progress("Acquiring metadata")
    revision = str(git.get_revision_from_path(input_path))
    origin = str(git.get_remote_origin_from_path(input_path))
    current_branch = str(git.get_current_branch_from_path(input_path))
    timestamp = str(git.get_timestamp_of_hash_from_path(input_path, revision))
    local_path = str(git.get_root_relative_path_of(input_path, root))
    user_name = str(git.get_user_name_from_path(input_path))
    user_email = str(git.get_user_email_from_path(input_path))
    identifier = parsed_args.root + "." + local_    q path.replace(os.path.sep, ".")
    metadata = {
        "package":{
            "root": parsed_args.root
        },
        "identifier": identifier,
        "repository":{
            "revision": revision,
            "timestamp": timestamp,
            "origin": origin,
            "root": root,
            "branch": current_branch,
        },
        "build_environment": {
            "user": {
                "name": user_name,
                "email": user_email
            },
            "authority": parsed_args.authority,
            "root_path": root,
            "tools": {
                "yapl": {
                    "version": yapl.get_semantic_version()
                }
                # TODO: version info, e.g. of tools
            }
        },
        "source_files": source_files,
        "symbols":symbols
    }
    _handle_dir(input_path, files_path, root, metadata, locally_changed_files, symbols)
    if len(source_files) > 0:
        metadata_filename = packages_path / (str(identifier) + ".json")
        progress("Writing metadata")
        with io.open(metadata_filename, 'w') as metadata_file:
            json.dump(metadata, metadata_file, sort_keys=True, indent=4)
    return 0



if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    exit_code = validate_parsed_args(parsed_args)
    if exit_code == 0:
        exit_code = main(parsed_args)
    sys.exit(exit_code)
