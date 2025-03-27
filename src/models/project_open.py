from dataclasses import dataclass, field
from typing import Union
import time


@dataclass
class ProjectOpen:
    name: str
    path: str
    last_opened: Union[str, float]

    @staticmethod
    def from_dict(data: dict) -> "ProjectOpen":
        return ProjectOpen(
            name=data["name"], path=data["path"], last_opened=data["last_opened"]
        )

    def get_dict(self) -> dict:
        return {"name": self.name, "path": self.path, "last_opened": self.last_opened}

    def get_last_opened(self) -> str:
        if isinstance(self.last_opened, float):
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.last_opened))
        return self.last_opened
