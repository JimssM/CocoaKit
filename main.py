#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from Application.Control.fileControl import *

mutex = check_single_instance()  # 进行锁，确保只有一个进程运行中
copy_ppocr_file(static_path + ".paddleocr")


if sys.platform == "win32":
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("7777")

from PyQt5.QtWidgets import QApplication
from Application.Control.mainControl import MainController

if __name__ == '__main__':
    def clean_up():
        print("清理资源")
        win32api.CloseHandle(mutex)


    app = QApplication(sys.argv)

    # Set your App icon。
    # app.setWindowIcon(QIcon(ui_path + "your_icon.ico"))

    main_ui = MainController()
    sys.exit(app.exec_())
