from typing import Optional, List, Union
from dataclasses import dataclass, field
import os
import logging
import inspect
import time


@dataclass
class FileManagement:
    directory_path: str
    directory_name: str
    folders: List[str] = field(default_factory=list)
    files: List[Union[str, tuple]] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> "FileManagement":
        """Creates a FileManagement instance from a dictionary."""
        data.setdefault("directory_path", data.pop("abs_path", ""))
        data.setdefault("directory_name", os.path.basename(
            data["directory_path"]))
        return FileManagement(
            directory_path=data["directory_path"],
            directory_name=data["directory_name"],
            folders=data.get("folders", []),
            files=data.get("files", []),
        )

    def get_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        return {
            "directory_path": self.directory_path,
            "directory_name": self.directory_name,
            "folders": self.folders,
            "files": self.files,
        }

    ######## Native Function Folder Management ########
    def add_folder(self, folder_name: str) -> None:
        """Adds a folder to the folder list if it doesn't already exist."""
        if folder_name not in self.folders:
            self.folders.append(folder_name)

    def generate_folder(self, folder_name: str, absolute_path: str = os.getcwd()) -> None:
        """Creates a folder inside the project directory if it does not already exist."""
        project_path = os.path.join(absolute_path, self.directory_name)
        folder_path = os.path.join(project_path, folder_name)

        if not os.path.isdir(project_path):
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe(
            ).f_code.co_name}: The path {project_path} does not exist or is not a directory.")
            return

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            self.add_folder(folder_name)
        else:
            logging.warning(f"{self.__class__.__name__}::{inspect.currentframe(
            ).f_code.co_name}: The folder {folder_name} already exists in {project_path}.")
            self.add_folder(folder_name)

    ####### Native Function File Management ########
    def add_file(self, file_info: tuple) -> None:
        """Adds a file to the file list if it doesn't already exist."""
        if file_info not in self.files:
            self.files.append(file_info)

    def generate_file(self, file_name: str, file_type: str, abs_path: str = os.getcwd()) -> None:
        """Creates a file inside the specified directory if it does not already exist."""
        project_path = os.path.join(abs_path, self.directory_path)

        if not os.path.isdir(abs_path):
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe(
            ).f_code.co_name}: The path {abs_path} does not exist or is not a directory.")
            return

        if not os.path.exists(project_path):
            os.mkdir(project_path)
        else:
            logging.warning(f"{self.__class__.__name__}::{inspect.currentframe(
            ).f_code.co_name}: The folder {self.directory_path} already exists in {abs_path}.")

        file_path = os.path.join(
            project_path, f"{file_name}.{file_type.lower()}")
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                pass
            self.add_file((file_name, file_type))
        else:
            logging.warning(f"{self.__class__.__name__}::{inspect.currentframe(
            ).f_code.co_name}: The file {file_name} already exists in {project_path}.")
            self.add_file((file_name, file_type))


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
