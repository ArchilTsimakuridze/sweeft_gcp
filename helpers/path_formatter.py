from pathlib import Path


def absolute_path(relative_path):
    """Returns an absolute path of a file from a relative path
    in case of an absolute path, returns the same string"""
    return str(Path(relative_path).resolve())
