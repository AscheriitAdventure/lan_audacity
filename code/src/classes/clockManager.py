import time
from typing import Optional, List


class ClockManager:
    def __init__(
            self, 
            time_start: float = time.time(),
            time_list: Optional[List[float]] = []
    ) -> None:
        self.__clock_created: float = time_start
        self.__clock_list: List[float] = time_list
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
    def clockList(self) -> List[float]:
        return self.__clock_list
    
    @clockList.setter
    def clockList(self, value: List[float]) -> None:
        self.__clock_list = value

    def add_clock(self) -> None:
        """Adds the current time to the clock list, ensuring a maximum of 20 entries."""
        if len(self.clockList) >= 20:
            self.clockList.pop(0)
        self.clockList.append(time.time())
    
    def get_clock_last(self) -> float:
        """Returns the last recorded time or the creation time if the list is empty."""
        return self.clockList[-1] if self.clockList else self.clockCreated

    def get_diff_clock(self) -> float:
        """Returns the time difference between the last two recorded timestamps."""
        if len(self.clockList) < 2:
            return 0.0
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

