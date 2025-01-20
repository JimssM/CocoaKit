#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Handle your front-end and back-end interactions in this module。
"""

from Application.Model.model import gl_info
from Application.View.mainView import MainView
from Application.public import *


class MainController:
    def __init__(self):
        self.ini = config_path

        self.mainView = MainView()

        gl_info.mainView = self.mainView
        self.mainView.show()
