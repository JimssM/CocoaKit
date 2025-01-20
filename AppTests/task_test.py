#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Some test
"""
import time
import winsound

from Application.tasks.your_custom_task_1 import task

t = time.time()

task()

print("耗时", time.time() - t)

winsound.Beep(1000, 500)
