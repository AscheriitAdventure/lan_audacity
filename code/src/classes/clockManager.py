import time
from typing import Optional


class ClockManager:
    def __init__(
            self, 
            time_start: float = time.time(),
            time_list: Optional[list[float]] = None
    ) -> None:
        self.__clock_created: float = time_start
        if time_list is None:
            self.__clock_list: list[float] = []
        else:
            self.__clock_list = time_list
        if time_list == [float]:
            self.__clock_list.append(self.clockCreated)
        self.type_time = "Unix Timestamp Format"

    @property
    def clockCreated(self) -> float:
        return self.__clock_created
    
    @clockCreated.setter
    def clockCreated(self, value: float) -> None:
        self.__clock_created = value

    @property
    def clockList(self) -> list[float]:
        return self.__clock_list
    
    @clockList.setter
    def clockList(self, value: list[float]) -> None:
        self.__clock_list = value

    def add_clock(self) -> None:
        self.clockList.append(time.time())
    
    def get_clock_last(self) -> float:
        if not self.clockList:
            return self.clockCreated
        else:
            return self.clockList.pop()

    def get_clock_diff(self) -> float:
        return self.clockList[-1] - self.clockList[-2]
    
    def dict_return(self) -> dict:
        return {
            "clock_created": self.__clock_created,
            "clock_list": self.__clock_list,
            "type_time": self.type_time
        }

    @staticmethod
    def conv_unix_to_datetime(unix_time: float):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unix_time))

    def __str__(self) -> str:
        return f"ClockManager: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.clockCreated))}"

