from qtpy.QtCore import Signal, Slot


class Window1:
    def __init__(self):
        pass


class Window2:
    def __init__(self):
        pass


class CustomProgressBar:
    def __init__(self):
        pass


class ProcessRun:
    progress = Signal(int)
    completed = Signal(int)

    @Slot(int)
    def do_process(self, n):
        for i in range(1, n + 1):
            time.sleep(1)
            self.progress.emit(i)
        self.completed.emit(i)