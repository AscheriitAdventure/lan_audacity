from dataclasses import dataclass, field
from typing import Union, List
import logging
import os
import inspect


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
        if os.path.basename(absolute_path) != self.directory_name:
            project_path = os.path.join(absolute_path, self.directory_name)
        else:
            project_path = absolute_path
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

