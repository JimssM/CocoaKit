**简体中文** | **[English](README-en.md)**

# CocoaKit

**CocoaKit** 是一个基于 MVC 架构的轻量级 Python 桌面自动化框架，提供了一个基础的用户界面示例和模块化的代码结构，可轻松定制和扩展。

![CocoaKit Logo](logo.png)

## 项目结构

- Application
    - Common - 各种各样的函数
    - Control - 线程处理、日志操作、数据库操作、前后端操作等
    - data - 其他与项目相关的数据
    - log - 日志处理
    - Model - 全局数据存储
    - Resources - 大量静态资源
    - Tasks - 自定义自动化任务
    - tools - 有用的函数，图像识别、输入控制等
    - ui - QT生成的ui文件
    - Units - 包含YOLO调用
    - View - UI类
    - public.py - 公共变量
- main.py - 入口文件
- requrements.txt - 需求文件

## 环境要求

- Python 3.8（请确保使用 Python 3.8 版本以保证框架的兼容性）
- Windows 操作系统（CocoaKit 专为 Windows 桌面环境设计）

## 安装依赖

```
pip install -r requirements.txt
```

## 功能特点

**CocoaKit** 集成了以下关键技术和工具：

1. **PyQt5**：作为 GUI 框架，提供灵活且强大的用户界面。
2. **OpenCV, Numpy, PIL**：实现图像识别模块，用于处理各种图像处理任务。
3. **pyautogui, win32api, pynput**：
    - 实现鼠标和键盘输入控制。
    - 包含贝塞尔曲线函数，用于实现平滑的鼠标轨迹移动。
4. **win32api**：支持基本的窗口功能和进程功能。
5. **Paddle OCR**：集成 OCR（光学字符识别）功能，用于识别图像中的文字。
6. **Fastdeploy 集成 ONNX 模型**：
    - 使用 ONNX 模型实现高效流畅的目标检测。
7. **SQLite**：提供轻量级数据库解决方案，用于数据存储和管理。

