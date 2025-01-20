#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import shutil
import getpass

import win32event
import win32api
import winerror

from Application.public import static_path


def check_single_instance():
    """
    Check for a single instance of the program. Prevents multiple instances from running simultaneously.
    Creates a global mutex lock. If the lock already exists, the program exits.
    """
    # Create a global mutex
    mutex_name = "Global\\MyXGAUTO"
    mutex = win32event.CreateMutex(None, False, mutex_name)
    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        print("The program is already running! Duplicate execution is not allowed.")
        sys.exit(1)
    return mutex


def copy_ppocr_file(source_directory):
    """
    Copies the PPOCR model files from the source directory to the user's default PaddleOCR directory.
    Ensures the required files are available locally, avoiding the need to download them when the project starts.

    :param source_directory: Path to the source directory containing PPOCR model files.
    """
    # Get the current user's username
    current_user = getpass.getuser()

    # Define the destination directory
    destination_directory = os.path.join("C:\\Users", current_user, ".paddleocr")

    # If the destination directory exists, delete it
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)
        print(f"Deleted existing directory: {destination_directory}")

    # Create the destination directory if it does not exist
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Iterate through all files in the source directory and copy them
    for item in os.listdir(source_directory):
        source_item = os.path.join(source_directory, item)
        destination_item = os.path.join(destination_directory, item)

        if os.path.isfile(source_item):
            shutil.copy2(source_item, destination_item)
            print(f"Copied file: {source_item} to {destination_item}")
        elif os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item)
            print(f"Copied directory: {source_item} to {destination_item}")
