import os
import logging

class FileManagement:
    def __init__(
            self, 
            folder_name: str, 
            folder_list: list[str] = [],
            files_list: list[str] = []
        ) -> None:
        self.__path = folder_name
        self.__folders = folder_list
        self.__files = files_list
    
    @property
    def path(self) -> str:
        return self.__path
    
    @property
    def folders(self) -> list:
        return self.__folders
    
    @property
    def files(self) -> list:
        return self.__files
    
    def generate_folder(self, folder_name: str, abs_path: str = os.getcwd()) -> None:
        # Check if the folder exists and if the path is a directory
        part2 = os.path.join(abs_path, self.path)
        if os.path.exists(abs_path) and os.path.isdir(abs_path):
            if not os.path.exists(part2):
                os.mkdir(part2)
            else:
                logging.warning(f"The folder {self.path} already exists in {abs_path}.")
            
            os.mkdir(os.path.join(part2, folder_name))
            self.add_folder(folder_name)
        else:
            logging.error(f"The path {abs_path} does not exist or is not a directory.")
    
    def generate_file(self, file_name: str, file_type: str, abs_path: str = os.getcwd()) -> None:
        part2 = os.path.join(abs_path, self.path)
        if os.path.exists(abs_path) and os.path.isdir(abs_path):
            if not os.path.exists(part2):
                os.mkdir(part2)
            else:
                logging.warning(f"The folder {self.path} already exists in {abs_path}.")
            
            file_path = os.path.join(part2, f"{file_name}.{file_type.lower()}")
            if not os.path.exists(file_path):
                with open(file_path, "w") as file:
                    pass
                self.add_file(file_name)
            else:
                logging.warning(f"The file {file_name} already exists in {part2}.")
        else:
            logging.error(f"The path {abs_path} does not exist or is not a directory.")
    
    def add_folder(self, folder_name: str) -> None:
        self.__folders.append(folder_name)

    def add_file(self, file_name: str) -> None:
        self.__files.append(file_name)
    
    def dict_return(self) -> dict:
        return {
            "path": self.__path,
            "folders": self.__folders,
            "files": self.__files
        }
    
    def __str__(self) -> str:
        str_return = f"Path: {self.__path}\n Folders: {self.__folders}\n  Files: {self.__files}"
        return str_return

# Test the class
# Create an instance of the FileManagement class
fm = FileManagement("test_folder")

# Generate a new folder
fm.generate_folder("sub_folder")

# Generate a new file
fm.generate_file("test_file", "txt")

# Add a folder and a file to the FileManagement object
fm.add_folder("another_folder")
fm.add_file("another_file")

# Print the resulting object
print(fm)