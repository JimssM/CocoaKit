#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import time

project_path = os.path.join(os.path.dirname(__file__), )  # 项目根目录

ocr_model_path = project_path + "\\Resources\\ocr\\"
static_path = project_path + "\\Resources\\static\\"
img_path = static_path + "img\\"
ui_path = static_path+"ui\\"
data_path = project_path + "\\data\\"
database_path = f"{static_path}/account_state.db"

log_dir = f"{data_path}/log"
log_path = f"{log_dir}/{time.strftime('%Y-%m-%d', time.localtime(time.time()))}.txt"
config_path = data_path + "config.ini"

post_url = "your server url"

"""
Other public data
"""
public_data_1 = None
public_data_2 = None

