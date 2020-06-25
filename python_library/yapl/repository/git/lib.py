from pathlib import Path
import os

import yapl.internal.shell_call as shell_call

_is_git_installed = None
def is_installed():
    global _is_git_installed
    if _is_git_installed is None:
        _is_git_installed = "yes" == shell_call.func("repository/git/shell_commands/is_installed")
    return _is_git_installed

def is_path_in_repository(path):
    if not is_installed():
        return False
    fullpath = os.path.realpath(path)
    return "yes" == shell_call.func("repository/git/shell_commands/is_repository", fullpath)

def get_revision_from_path(path):
    if not is_path_in_repository(path):
        return ""
    fullpath = os.path.realpath(path)
    return shell_call.func("repository/git/shell_commands/get_revision", fullpath)

def get_current_branch_from_path(path):
    if not is_path_in_repository(path):
        return ""
    fullpath = os.path.realpath(path)
    return shell_call.func("repository/git/shell_commands/get_current_branch", fullpath)

def get_user_name_from_path(path):
    if not is_path_in_repository(path):
        return ""
    fullpath = os.path.realpath(path)
    return shell_call.func("repository/git/shell_commands/get_user_name", fullpath)

def get_user_email_from_path(path):
    if not is_path_in_repository(path):
        return ""
    fullpath = os.path.realpath(path)
    return shell_call.func("repository/git/shell_commands/get_user_email", fullpath)

def get_timestamp_of_hash_from_path(path, hash):
    if not is_path_in_repository(path):
        return ""
    fullpath = os.path.realpath(path)
    return shell_call.func("repository/git/shell_commands/get_timestamp_of_hash", fullpath, hash)

def get_remote_origin_from_path(path):
    if not is_path_in_repository(path):
        return ""
    fullpath = os.path.realpath(path)
    return shell_call.func("repository/git/shell_commands/get_remote_origin", fullpath)

def get_root_from_path(path):
    if not is_path_in_repository(path):
        return ""
    fullpath = os.path.realpath(path)
    return shell_call.func("repository/git/shell_commands/get_root", fullpath)

def get_hash_of_file(filename, root=None):
    if root is None:
        root = get_root_from_path(path)
    if root == "":
        return None
    if not os.path.exists(filename):
        return None
    return shell_call.func("repository/git/shell_commands/get_hash_of_file", root, filename)

def is_path_ignored(path, root=None):
    if root is None:
        root = get_root_from_path(path)
    if root == "":
        return True
    if not os.path.exists(path):
        return True
    return "yes" == shell_call.func("repository/git/shell_commands/is_ignored", root, path)

def get_root_relative_path_of(path, root=None):
    if root is None:
        root = get_root_from_path(path)
    if root == "":
        return None
    fullpath = os.path.realpath(path)
    return os.path.relpath(fullpath, root)

def get_locally_changed_files_from_path(path):
    root = get_root_from_path(path)
    if root == "":
        return []
    fullpath = os.path.realpath(path)
    changes = []
    output = shell_call.func("repository/git/shell_commands/get_local_changes", fullpath)
    lines = output.split("\n")
    for line in lines:
        sections = line.split(" ")
        if len(sections) == 2 and sections[0] == "?":
            # untracked file
            relative_filenames = [ sections[1] ]
        elif len(sections) == 9:
            relative_filenames = [ sections[8] ]
        elif len(sections) == 10:
            relative_filenames = sections[9].split("\t")
        else:
            assert False, "Expected 2, 9 or 10 columns from get_local_changes, not " + str(len(sections))
        for relative_filename in relative_filenames:
            absolute_filename = os.path.realpath(os.path.join(fullpath, relative_filename))
            hash = get_hash_of_file(absolute_filename, root)
            relative_filename = os.path.relpath(absolute_filename, root)
            changes.append((hash, relative_filename))
    return changes
