import os

import yapl.internal.shell_call as shell_call

_is_git_installed = None
def is_git_installed():
    global _is_git_installed
    if _is_git_installed is None:
        _is_git_installed = "yes" == shell_call.func("repository/git/shell_commands/is_git_installed")
    return _is_git_installed

def is_path_in_git_repository(path):
    if not is_git_installed():
        return False
    fullpath = os.path.realpath(path)
    return "yes" == shell_call.func("repository/git/shell_commands/is_git_repository", fullpath)
