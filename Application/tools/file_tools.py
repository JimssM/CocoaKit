#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

def get_all_files_name(directory, parent_dir=None):
    """
    Retrieves all file names in the specified directory.

    Parameters:
        directory (str): The directory to scan for files.
        parent_dir (str, optional): The parent directory to prepend to the file names. Defaults to None.

    Returns:
        list: A list of file names or file paths (if parent_dir is provided).
    """
    files = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            if parent_dir is not None:
                files.append(os.path.join(parent_dir, file))  # Include parent directory in file paths
            else:
                files.append(file)  # Only include file names
    return files
