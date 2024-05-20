import time

class ClockManager:
    def __init__(self):
        self.__clock_created: float = time.time()
        self.__clock_list: list[float] = []
        self.__clock_list.append(self.clock_created)
        self.type_time = "Unix Timestamp Format"

    @property
    def clock_created(self):
        return self.__clock_created

    @property
    def clock_list(self):
        return self.__clock_list

    def add_clock(self):
        self.clock_list.append(time.time())

    def get_clock_list(self):
        return self.clock_list

    def get_clock_created(self):
        return self.clock_created

    def get_clock_last(self):
        return self.clock_list[-1]

    def get_clock_diff(self):
        return self.clock_list[-1] - self.clock_list[-2]

    @staticmethod
    def conv_unix_to_datetime(unix_time: float):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unix_time))

    def __str__(self) -> str:
        return f"ClockManager: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.clock_created))}"
