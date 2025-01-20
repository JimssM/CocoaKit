#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import win32api

from Application.Control.fileControl import check_single_instance, copy_ppocr_file
from Application.public import static_path

# Ensure only one instance of the application is running
mutex = check_single_instance()
copy_ppocr_file(static_path + ".paddleocr")

if sys.platform == "win32":
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("7777")

from PyQt5.QtWidgets import QApplication
from Application.Control.mainControl import MainController

if __name__ == '__main__':
    def clean_up():
        # Clean up resources
        print("Cleaning up resources")
        win32api.CloseHandle(mutex)


    app = QApplication(sys.argv)

    # Set your application icon
    # app.setWindowIcon(QIcon(ui_path + "your_icon.ico"))

    main_ui = MainController()
    sys.exit(app.exec_())
