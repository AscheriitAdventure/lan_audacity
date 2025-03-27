from dataclasses import dataclass, field
from typing import List
import time

@dataclass
class ClockManager:
    """Manages a list of timestamps to track time events."""
    clock_created: float = field(default_factory=time.time)
    type_time: str = field(default="Unix Timestamp Format")
    clock_list: List[float] = field(default_factory=list)  # Limit to 20 clocks

    @staticmethod
    def from_dict(data: dict) -> "ClockManager":
        """Creates a ClockManager instance from a dictionary."""
        return ClockManager(
            clock_created=data.get("clock_created", time.time()),
            type_time=data.get("type_time", "Unix Timestamp Format"),
            clock_list=data.get("clock_list", []),
        )

    def get_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        return {
            "clock_created": self.clock_created,
            "type_time": self.type_time,
            "clock_list": self.clock_list,
        }

    def add_clock(self) -> None:
        """Adds the current time to the clock list, ensuring a maximum of 20 entries."""
        if len(self.clock_list) >= 20:
            self.clock_list.pop(0)  # Maintain the latest 20 entries
        self.clock_list.append(time.time())

    def get_last_clock(self) -> float:
        """Returns the last recorded time or the creation time if the list is empty."""
        return self.clock_list[-1] if self.clock_list else self.clock_created

    def get_diff_clock(self) -> float:
        """Returns the time difference between the last two recorded timestamps."""
        if len(self.clock_list) < 2:
            return 0.0
        return self.clock_list[-1] - self.clock_list[-2]
