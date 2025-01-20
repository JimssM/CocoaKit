 **简体中文** | **[English](README-en.md)**

# CocoaKit

**CocoaKit** 是一个基于 MVC 架构的轻量级 Python 桌面自动化框架，提供了一个基础的用户界面示例和模块化的代码结构，可轻松定制和扩展。

![CocoaKit Logo](logo.png)

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
