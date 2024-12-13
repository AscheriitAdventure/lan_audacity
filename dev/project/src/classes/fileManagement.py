import os
import logging
from typing import Optional, Any
import inspect


class FileManagement:
    def __init__(
            self, folder_name: str,
            folder_list: Optional[list[str]] = None,
            files_list: Optional[list[tuple]] = None
    ) -> None:
        self.__path: str = folder_name
        if folder_list is None:
            self.__folders: list[str] = []
        else:
            self.__folders: list[str] = folder_list
        if files_list is None:
            self.__files: list[tuple] = []
        else:
            self.__files: list[tuple] = files_list
    
    @property
    def path(self) -> str:
        return self.__path
    
    @property
    def folders(self) -> list:
        return self.__folders
    
    @folders.setter
    def folders(self, value: list) -> None:
        self.__folders = value

    @property
    def files(self) -> list:
        return self.__files
    
    @files.setter
    def files(self, value: list) -> None:
        self.__files = value
    
    def generate_folder(self, folder_name: str, abs_path: str = os.getcwd()) -> None:
        # Check if the folder exists and if the path is a directory
        project_path = os.path.join(abs_path, self.path)
        if os.path.exists(project_path) and os.path.isdir(project_path):
            if not os.path.exists(os.path.join(project_path, folder_name)):
                os.mkdir(os.path.join(project_path, folder_name))
            else:
                logging.warning(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: The folder {folder_name} already exists in {project_path}.")
                # insert the folder into the list of folders if it does not exist
                if folder_name not in self.folders:
                    self.add_folder(folder_name)

            self.add_folder(folder_name)
        else:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: The path {project_path} does not exist or is not a directory.")
    
    def generate_file(self, file_name: str, file_type: str, abs_path: str = os.getcwd()) -> None:
        part2 = os.path.join(abs_path, self.path)
        if os.path.exists(abs_path) and os.path.isdir(abs_path):
            if not os.path.exists(part2):
                os.mkdir(part2)
            else:
                logging.warning(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: The folder {self.path} already exists in {abs_path}.")
            
            file_path = os.path.join(part2, f"{file_name}.{file_type.lower()}")
            if not os.path.exists(file_path):
                with open(file_path, "w") as file:
                    pass
                self.add_file((file_name, file_type))
            else:
                logging.warning(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: The file {file_name} already exists in {part2}.")
                # insert the file into the list of files if it does not exist
                if (file_name, file_type) not in self.files:
                    self.add_file((file_name, file_type))

        else:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: The path {abs_path} does not exist or is not a directory.")
    
    def add_folder(self, folder_name: str) -> None:
        self.__folders.append(folder_name)

    def add_file(self, file_name: tuple) -> None:
        self.__files.append(file_name)
    
    def dict_return(self) -> dict:
        return {
            "path": self.__path,
            "folders": self.__folders,
            "files": self.__files
        }
    
    def __str__(self) -> str:
        str_return = f"Path: {self.__path}, Folders: {self.__folders},  Files: {self.__files}"
        return str_return