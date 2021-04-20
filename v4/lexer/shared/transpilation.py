import os
import shutil

from yapl.v4.lexer.shared.modules.manifest import Manifest as ModulesManifest


class Transpilation(object):

    def __init__(self, transpilation_directory):
        self.__transpilation_directory = os.path.abspath(transpilation_directory)
        os.makedirs(self.__transpilation_directory, mode=0o777, exist_ok=True)
        self.__manifest = None
        self.__module_file_refs = []

    @staticmethod
    def create(transpilation_directory):
        os.makedirs(transpilation_directory, mode=0o777, exist_ok = True)
        return Transpilation(transpilation_directory)

    def manifest(self):
        return self.__manifest

    def load(self):
        self.__manifest = ModulesManifest(self.__transpilation_directory)
        self.__manifest.load()
        self.__module_file_refs = list(self.__manifest.get_module_file_refs())
        return self

    def save(self):
        self.__manifest = ModulesManifest(self.__transpilation_directory)
        self.__manifest.add_module_file_refs(self.__module_file_refs)
        self.__manifest.save()
        return self

    def add_module_file_ref(self, module_file_ref):
        self.__module_file_refs.append(module_file_ref)
        destination = os.path.join(
            self.__transpilation_directory, "modules", module_file_ref.sha256 + ".yapl")
        destination_directory = os.path.dirname(destination)
        os.makedirs(destination_directory, mode=0o777, exist_ok=True)
        shutil.copyfile(module_file_ref.absolute_pathname, destination)
        return self

    def get_module_file_refs(self):
        return self.__module_file_refs
