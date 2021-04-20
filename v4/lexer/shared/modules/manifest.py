import os
import io
import yaml
import hashlib


class Manifest(object):

    def __init__(self, transpilation_directory):
        self.__modules_directory = os.path.join(transpilation_directory, "modules")
        self.__manifest_filename = os.path.join(self.__modules_directory, "manifest.yaml")
        self.__manifest_dict = None
        self.__module_file_refs = []

    def load(self):
        os.makedirs(self.__modules_directory, mode=0o777, exist_ok=True)
        with io.open(self.__manifest_filename, 'r') as manifest_file:
            manifest_dict = yaml.safe_load(manifest_file)
            self.__module_file_refs = manifest_dict["modules"]

    def save(self):
        os.makedirs(self.__modules_directory, mode=0o777, exist_ok = True)
        manifest_dict = {
            "modules": [],
        }
        for module_file_ref in self.__module_file_refs:
            filename_without_extension = os.path.splitext(module_file_ref.relative_pathname)[0]
            basename_without_extension = os.path.basename(filename_without_extension)
            if basename_without_extension.startswith("."):
                d = os.path.dirname(module_file_ref.relative_pathname)
                id = d.replace(".", "_").replace("/", ".")
            else:
                id = filename_without_extension.replace(".", "_").replace("/", ".")
            module = {
                "filename": module_file_ref.relative_pathname,
                "sha256": module_file_ref.sha256,
                "id": id
            }
            manifest_dict["modules"].append({"module": module})
        manifest_dict["manifest"] = {
            "sha256": self.__calculate_manifest_sha256()
        }
        self.__manifest_dict = manifest_dict
        with io.open(self.__manifest_filename, 'w') as manifest_file:
            yaml.safe_dump(self.__manifest_dict, manifest_file)

    def __calculate_manifest_sha256(self):
        stuff = [
            module_file_ref.relative_pathname + "." + module_file_ref.sha256
            for module_file_ref in self.__module_file_refs
        ]
        stuff.sort()
        h = hashlib.sha256()
        for s in stuff:
            h.update(s.encode("utf-8"))
        return h.hexdigest()

    def add_module_file_refs(self, module_file_references):
        self.__module_file_refs.extend(module_file_references)

    def get_module_file_refs(self):
        return [m["module"] for m in self.__module_file_refs]
