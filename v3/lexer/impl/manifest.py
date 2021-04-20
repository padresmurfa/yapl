import os
import io
import json
import hashlib

from impl.file_reference import FileReference, to_file_reference


class Manifest(object):

    def __init__(self, bundle_directory):
        self.__bundle_directory = bundle_directory
        self.__manifest_filename = os.path.join(bundle_directory, "manifest.json")
        self.__manifest_dict = None
        self.__source_file_refs = []

    def load(self):
        with io.open(self.__manifest_filename, 'r') as manifest_file:
            manifest_dict = json.load(manifest_file)
            self.__source_file_refs = [
                self.__manifest_entry_to_file_reference(source_file, "source_files")
                for source_file in manifest_dict["source_files"]
            ]

    def save(self):
        manifest_dict = {
            "source_files": []
        }
        for source_file_ref in self.__source_file_refs:
            source_file = {
                "filename": source_file_ref.relative_pathname,
                "sha256": source_file_ref.sha256
            }
            manifest_dict["source_files"].append(source_file)
        manifest_dict["256"] = self.__calculate_manifest_sha256()
        self.__manifest_dict = manifest_dict
        with io.open(self.__manifest_filename, 'w') as manifest_file:
            json.dump(self.__manifest_dict, manifest_file)
        
    def __calculate_manifest_sha256(self):
        stuff = [
            source_file_ref.relative_pathname + "." + source_file_ref.sha256
            for source_file_ref in self.__source_file_refs
        ]
        stuff.sort()
        h = hashlib.sha256()
        for s in stuff:
            h.update(s.encode("utf-8"))
        return h.hexdigest()

    def add_source_file_refs(self, source_file_references):
        self.__source_file_refs.extend(source_file_references)

    def __manifest_entry_to_file_reference(self, manifest_entry, bundle_subdirectory):
        root_directory = os.path.join(self.__bundle_directory, bundle_subdirectory)
        relative = manifest_entry["filename"]
        absolute = os.path.join(root_directory, relative)
        return to_file_reference(root_directory, absolute)

    def get_source_file_refs(self):
        return self.__source_file_refs
