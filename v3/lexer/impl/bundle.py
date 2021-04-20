import os
import shutil

from impl.manifest import Manifest


class Bundle(object):

    def __init__(self, bundle_directory):
        self.__bundle_directory = os.path.abspath(bundle_directory)
        os.makedirs(self.__bundle_directory, mode = 0o777, exist_ok = True)
        self.__manifest = None
        self.__source_file_refs = []

    def load(self):
        self.__manifest = Manifest(self.__bundle_directory)
        self.__manifest.load()
        self.__source_file_refs = list(self.__manifest.get_source_file_refs())
        return self.__manifest

    def save(self):
        self.__manifest = Manifest(self.__bundle_directory)
        self.__manifest.add_source_file_refs(self.__source_file_refs)
        self.__manifest.save()
        
    def add_source_file_ref(self, source_ref):
        self.__source_file_refs.append(source_ref)
        destination = os.path.join(self.__bundle_directory, "source_files", source_ref.relative_pathname)
        destination_directory = os.path.dirname(destination)
        os.makedirs(destination_directory, mode=0o777, exist_ok=True)
        shutil.copyfile(source_ref.absolute_pathname, destination)

    def get_source_file_refs(self):
        return self.__source_file_refs
