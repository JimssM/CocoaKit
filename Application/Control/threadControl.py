import ctypes
import threading
import time

from Application.Model.model import gl_info

'''
Example Usage:
thread = ThreadControl(
    func=lambda: _run_one_account(line, thread=thread),
    callback=lambda: _call_back(thread=thread), 
    max_time=999999
)
thread.start()
thread.join()
'''


class ThreadControl(threading.Thread):
    """
    Custom thread control class with a timer and callback mechanism.

    Methods:
        ThreadControl.start() - Starts the thread.
        ThreadControl.join() - Waits for the thread to complete.

    Parameters:
        func (callable): The function to execute in the thread.
        callback (callable): The callback function to call upon completion.
        max_time (int): The maximum execution time for the thread in seconds (default is 10 minutes).
    """

    def __init__(self, func=lambda: None, callback=lambda: None, max_time=600):
        super().__init__()

        self.func = func
        self.callback = callback
        self.max_time = max_time

        self.execution_time = 0
        self.timer_thr = None

    def run(self):
        """
        Executes the target function and manages the callback and timer.
        """
        # Start the timer thread
        self.timer_thr = threading.Thread(target=self.__timer, daemon=True)
        self.timer_thr.start()

        try:
            self.func()
        except SystemExit:
            pass
        finally:
            if self.callback is not None:
                self.callback()

    def stop(self):
        """
        Stops the thread by raising a SystemExit exception in the thread.
        """
        if not self.is_alive():  # If the thread is not active
            return

        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(self.ident), exc
        )
        if res == 0:
            raise ValueError("Thread ID not found")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, None)
            raise SystemError("Thread stop failed")

    def __timer(self):
        """
        Internal timer function that tracks execution time and stops the thread if it exceeds max_time.
        """
        while self.is_alive():
            if self.execution_time < self.max_time:
                self.execution_time += 1
                print(f"Thread running time: {self.execution_time} seconds")
                time.sleep(1)
            else:
                gl_info.interrupt = True  # Trigger interruption flag
                self.stop()
                break
