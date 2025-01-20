import ctypes
import os
import subprocess
import psutil
import win32con
import win32gui
import win32process

"""
Window Management Functions
"""

def find_window_handle(cls: str, title: str):
    """
    Find a window handle based on its class name and title.

    Parameters:
        cls (str): Class name of the window.
        title (str): Title of the window.

    Returns:
        int: Handle to the window, or 0 if not found.
    """
    return win32gui.FindWindow(cls, title)

def close_window_by_handle(hwnd):
    """
    Close a window using its handle.

    Parameters:
        hwnd (int): Handle to the window.

    Returns:
        None
    """
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

def set_window_top_left(hwnd):
    """
    Move a window to the top-left corner of the screen.

    Parameters:
        hwnd (int): Handle to the window.

    Returns:
        None
    """
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, right - left, bottom - top, win32con.SWP_SHOWWINDOW)

def set_window_top(hwnd):
    """
    Set a window to always stay on top.

    Parameters:
        hwnd (int): Handle to the window.

    Returns:
        None
    """
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def set_window_no_top(hwnd):
    """
    Remove the always-on-top property from a window.

    Parameters:
        hwnd (int): Handle to the window.

    Returns:
        None
    """
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def find_cls_and_title_by_pid(pid):
    """
    Find all window class names and titles for a given process ID.

    Parameters:
        pid (int): Process ID.

    Returns:
        None
    """
    def callback(hwnd, hwnds):
        if all([win32process.GetWindowThreadProcessId(hwnd)[1] == pid, win32gui.IsWindowVisible(hwnd)]):
            print(win32gui.GetClassName(hwnd), win32gui.GetWindowText(hwnd))
            hwnds.append(hwnd)
        return True

    hwnd_list = []
    win32gui.EnumWindows(callback, hwnd_list)

"""
Process Management Functions
"""

def start_process(process_path):
    """
    Start a process using PowerShell.

    Parameters:
        process_path (str): Path to the executable.

    Returns:
        None
    """
    command = f'powershell -command "Start-Process \'{process_path}\'"'
    subprocess.run(command, shell=True)

def start_process_2(process_path):
    """
    Start a process with a hidden console window.

    Parameters:
        process_path (str): Path to the executable.

    Returns:
        None
    """
    working_directory = os.path.dirname(process_path)
    os.chdir(working_directory)

    SW_HIDE = 0
    STARTF_USESHOWWINDOW = 1

    class STARTUPINFO(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_ulong),
                    ("lpReserved", ctypes.c_void_p),
                    ("lpDesktop", ctypes.c_void_p),
                    ("lpTitle", ctypes.c_void_p),
                    ("dwX", ctypes.c_ulong),
                    ("dwY", ctypes.c_ulong),
                    ("dwXSize", ctypes.c_ulong),
                    ("dwYSize", ctypes.c_ulong),
                    ("dwXCountChars", ctypes.c_ulong),
                    ("dwYCountChars", ctypes.c_ulong),
                    ("dwFillAttribute", ctypes.c_ulong),
                    ("dwFlags", ctypes.c_ulong),
                    ("wShowWindow", ctypes.c_ushort),
                    ("cbReserved2", ctypes.c_ushort),
                    ("lpReserved2", ctypes.c_void_p),
                    ("hStdInput", ctypes.c_void_p),
                    ("hStdOutput", ctypes.c_void_p),
                    ("hStdError", ctypes.c_void_p)]

    class PROCESS_INFORMATION(ctypes.Structure):
        _fields_ = [("hProcess", ctypes.c_void_p),
                    ("hThread", ctypes.c_void_p),
                    ("dwProcessId", ctypes.c_ulong),
                    ("dwThreadId", ctypes.c_ulong)]

    startupinfo = STARTUPINFO()
    startupinfo.cb = ctypes.sizeof(startupinfo)
    startupinfo.dwFlags = STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = SW_HIDE

    process_information = PROCESS_INFORMATION()
    creation_flags = 0x08000000  # CREATE_NO_WINDOW

    ctypes.windll.kernel32.CreateProcessW(None, process_path, None, None, False, creation_flags, None, None,
                                          ctypes.byref(startupinfo), ctypes.byref(process_information))
    print("Process started, continuing execution.")

def start_process_3(process_path):
    """
    Start a process using subprocess.Popen.

    Parameters:
        process_path (str): Path to the executable.

    Returns:
        Popen: Subprocess object.
    """
    return subprocess.Popen(process_path)

def start_process_4(process_path):
    """
    Start a process with hidden output and error streams.

    Parameters:
        process_path (str): Path to the executable.

    Returns:
        None
    """
    command = [f"{process_path}", "--console"]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)

def close_process(process_name):
    """
    Forcefully terminate a process by name using taskkill.

    Parameters:
        process_name (str): Name of the process to terminate.

    Returns:
        None
    """
    os.system(f"taskkill /F /IM {process_name}")

def close_process_2(process_name):
    """
    Terminate a process by name using psutil.

    Parameters:
        process_name (str): Name of the process to terminate.

    Returns:
        None
    """
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'] == process_name:
            try:
                process.kill()
            except psutil.NoSuchProcess:
                pass

def is_process_running(process_name):
    """
    Check if a process is running by its name.

    Parameters:
        process_name (str): Name of the process to check.

    Returns:
        bool: True if the process is running, False otherwise.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return True
    return False

def count_processes_by_name(process_name):
    """
    Count the number of processes with a specific name.

    Parameters:
        process_name (str): Name of the process.

    Returns:
        int: Number of processes with the given name.
    """
    count = 0
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            count += 1
    return count
