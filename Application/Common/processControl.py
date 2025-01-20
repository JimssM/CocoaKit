#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Module to manage the control process.
"""

from Application.Control.threadControl import ThreadControl
from Application.Model.model import gl_info


def task_control_main():
    """
    Main entry point to initialize and control the task processing thread.
    """
    # Prepare data and logic before starting the thread
    data = "Some data"

    # Initialize the thread with the task function and callback
    process_thread = ThreadControl(
        func=_task_control,
        callback=lambda: _task_control_callback(data=data)
    )

    # Assign the thread to the global info object and start it
    gl_info.thread_main = process_thread  # Main thread reference
    process_thread.start()
    process_thread.join()


def _task_control_callback(data):
    """
    Callback function executed after the task is completed.
    Args:
        data: Additional data passed to the callback.
    """
    # Add logic for the callback, if necessary
    pass


def _task_control():
    """
    Function to handle pre-processing, invoking the process control logic,
    and post-processing steps.
    """
    # Logic before running process_control
    _process_control()

    # Logic after running process_control
    gl_info.clear_all()


def _process_control():
    """
    Core process logic to be executed during the task control.
    """
    # Add the main processing logic here
    pass
