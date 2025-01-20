#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Module for managing GUI functionality
"""

from PyQt5.QtWidgets import QWidget, QMessageBox, QHeaderView, QPushButton, QDialog, QLabel, QVBoxLayout
from Application.ui.your_ui_file import Ui_Form


class MainView(Ui_Form, QWidget):
    def __init__(self):
        super(MainView, self).__init__()
        self.setupUi(self)
        self.initialize_ui()

    def initialize_ui(self):
        """ Custom UI styling """
        pass
