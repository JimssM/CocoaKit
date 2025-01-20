#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Module for storing global data and thread-specific data.
"""

class Custom:
    def __init__(self):
        self.mainView = None

        # Global variables
        self.da = []
        self.thread_main = None
        self.thread = None
        self.thread_son = None
        self.task_list = []

        # Task flags
        self.task_1 = True
        self.task_2 = True

        # ThreadControl timeout flag
        self.interrupt = False

        self.process = "Not Started"
        self.finished_task = []
        self.log = "Initialized"

    def clear(self):
        """
        Clears all data except global and view-related data.
        """
        mainView = self.mainView

        # Preserve threads and task list
        thread_main = self.thread_main
        thread = self.thread
        thread_son = self.thread_son
        task_list = self.task_list

        # Reinitialize
        self.__init__()

        # Restore preserved data
        self.mainView = mainView
        self.thread_main = thread_main
        self.thread = thread
        self.thread_son = thread_son
        self.task_list = task_list

    def clear_all(self):
        """
        Clears all data except view-related data.
        """
        mainView = self.mainView
        self.__init__()
        self.mainView = mainView

def tdi():
    """
    Initialize a list of Custom objects for thread-specific data.
    """
    return [Custom() for _ in range(100)]


# Global data instance
gl_info = Custom()

# Thread-specific data instances
td_info = tdi()
