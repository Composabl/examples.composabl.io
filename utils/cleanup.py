"""
Utils for cleaning up folder structures while running agents.
"""

import os

def clean_folder(path: str, extension: str = '.pkl') -> None:
    """
    Delete old history files.

    Args:
        path (str): Path to the folder containing the history files.
        extension (str): Extension of the files to be deleted. Default is '.pkl'.
    """
    try:
        files = os.listdir(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Path {path} does not exist.")

    pkl_files = [file for file in files if file.endswith(extension)]
    for file in pkl_files:
        file_path = os.path.join(path, file)
        os.remove(file_path)
