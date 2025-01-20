#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Storing qt signals.
"""

from PyQt5.Qt import QObject, pyqtSignal

class SignalUnit(QObject):
    table = pyqtSignal(int, int, str, int,int)
    log = pyqtSignal(str)
signal = SignalUnit()

