from os import path
from subprocess import check_output, check_call
from pathlib import Path

def _filename(fname):
    import yapl
    yapl_root = Path(yapl.__file__).parent
    filename = fname + ".sh"
    full_filename = yapl_root / filename
    return str(full_filename)

def func(fname, *args):
    shell_script = _filename(fname)
    command = list([shell_script] + [str(a) for a in args])
    result = check_output(command, text=True).strip()
    return result

def proc(fname, *args):
    shell_script = _filename(fname)
    command = list([shell_script] + [str(a) for a in args])
    check_call(command)
