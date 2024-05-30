import os
import logging

class FileManagement:
    def __init__(
            self, 
            folder_name: str, 
            folder_list: list[str] = [],
            files_list: list[tuple] = []
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
                logging.warning(f"The folder {folder_name} already exists in {project_path}.")

            self.add_folder(folder_name)
        else:
            logging.error(f"The path {project_path} does not exist or is not a directory.")
    
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
                self.add_file((file_name, file_type))
            else:
                logging.warning(f"The file {file_name} already exists in {part2}.")
        else:
            logging.error(f"The path {abs_path} does not exist or is not a directory.")
    
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
        str_return = f"Path: {self.__path}\n Folders: {self.__folders}\n  Files: {self.__files}"
        return str_return

import json
import yaml
import xmltodict
import csv
import configparser
from typing import Any


class SwitchFile2:
    @staticmethod
    def json_read(abs_path: str) -> Any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return json.load(file)
    
    @staticmethod
    def json_write(abs_path: str, data: Any) -> None:
        with open(abs_path, "w+", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def yaml_read(abs_path: str) -> Any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    
    @staticmethod
    def yaml_write(abs_path: str, data: Any) -> None:
        with open(abs_path, "w+", encoding="utf-8") as file:
            yaml.dump(data, file)

    @staticmethod
    def xml_read(abs_path: str) -> Any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return xmltodict.parse(file.read())
    
    @staticmethod
    def xml_write(abs_path: str, data: Any) -> None:
        with open(abs_path, "w+", encoding="utf-8") as file:
            file.write(xmltodict.unparse(data, pretty=True))

    @staticmethod
    def csv_read(abs_path: str) -> Any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return csv.DictReader(file)
    
    @staticmethod
    def csv_write(abs_path: str, data: Any) -> None:
        with open(abs_path, "w+", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def txt_read(abs_path: str) -> Any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return file.read()
    
    @staticmethod
    def txt_write(abs_path: str, data: Any) -> None:
        with open(abs_path, "w+", encoding="utf-8") as file:
            file.write(data)

    @staticmethod
    def ini_read(abs_path: str) -> Any:
        config = configparser.ConfigParser()
        config.read(abs_path, encoding="utf-8")
        return config
    
    @staticmethod
    def ini_write(abs_path: str, data: Any) -> None:
        with open(abs_path, "w+", encoding="utf-8") as file:
            data.write(file)

    @staticmethod
    def conf_read(abs_path: str) -> Any:
        config = configparser.ConfigParser()
        config.read(abs_path)
        return config
    
    @staticmethod
    def conf_write(abs_path: str, data: Any) -> None:
        with open(abs_path, "w+", encoding="utf-8") as file:
            data.write(file)
        
    @staticmethod
    def universal_read(abs_path: str) -> Any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return file.read()

import time

class ClockManager:
    def __init__(
            self, 
            time_start: float = time.time(),
            time_list: list[float] = []
        ) -> None:
        self.__clock_created: float = time_start
        self.__clock_list: list[float] = time_list
        if time_list == []:
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
        return self.clockList[-1]

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

import shutil

class LanAudacity(FileManagement):
    def __init__(
            self, 
            project_name: str, 
            abs_path: str = os.getcwd(),
            folder_list: list[str] = [],
            files_list: list[tuple] = [],
            software_name: str = "Lan Audacity",
            software_version: str = "1.0.4",
            author: str = "Unknown"
            ) -> None:
        super().__init__(project_name, folder_list, files_list)
        self.__abs_path = abs_path
        self.__software: dict = {
            "name": software_name,
            "version": software_version
        }
        self.__author = author
        self.__objPaths = {}
    
    @property
    def absPath(self) -> str:
        return self.__abs_path
    
    @absPath.setter
    def absPath(self, value: str) -> None:
        total_path = os.path.join(value, self.path)
        if os.path.exists(total_path):
            self.__abs_path = value
    
    @property
    def software(self) -> dict:
        return self.__software
    
    def getSoftwareName(self) -> str:
        return self.software["name"]
    
    def getSoftwareVersion(self) -> str:
        return self.software["version"]
    
    @property
    def author(self) -> str:
        return self.__author
    
    @author.setter
    def author(self, value: str) -> None:
        self.__author = value
    
    def dict_objPaths(self) -> dict:
        dict_return = {}
        for key, value in self.__objPaths.items():
            dict_return[key] = value.dict_return()
        return dict_return
    
    def dict_return(self) -> dict:
        return {
            "project_name": self.path,
            "abs_path": self.absPath,
            "software": self.software,
            "author": self.author,
            "obj_paths": self.dict_objPaths()
        }
    
    def updateProject_0(self):
        self.add_folder(self.path)
        self.generate_file("lan_audacity", "json", self.absPath)
        cl_infos = [
            {
                "name": "conf"
            },
            {
                "name": "db",
                "folders": ["interfaces", "desktop"]
            },
            {
                "name": "logs",
                "files": [("lan_audacity", "log")]
            },
            {
                "name": "pixmap"
            }
        ]
        for cl_info in cl_infos:
            self.__objPaths[cl_info["name"]] = FileManagement(cl_info["name"])
            fls_mng = self.__objPaths[cl_info["name"]]
            self.generate_folder(fls_mng.path , self.absPath)
            if "folders" in cl_info:
                # Set the folders attribute using the setter method
                for folder in cl_info["folders"]:
                    fls_mng.generate_folder(folder, os.path.join(self.absPath, self.path))
            if "files" in cl_info:
                for file in cl_info["files"]:
                    fls_mng.generate_file(file[0], file[1], os.path.join(self.absPath, self.path))
            print(fls_mng)


"""class LanAudacity:
    def __init__(
            self,
            software_name: str = "Lan Audacity",
            software_version: str = "1.0.4",
            project_name: str = "Unknown",
            save_path: str = os.getcwd(),
            author: str = "Unknown",
            clock_manager: ClockManager = ClockManager(),
            network_list: list[dict] = [],
            link_list: list[dict] = [],
            device_list: list[dict] = [],
            pixmap_list: list[dict] = []
        ) -> None:
        # Fichier de référence pour le logiciel "Lan Audacity"
        self.refFile: tuple = ("lan_audacity","json")
        self.__softName = software_name
        self.__softVersion = software_version
        self.__projectName = project_name
        self.__savePath = save_path
        self.__author = author
        self.__clockManager = clock_manager
        self.__charTable = "utf-8"
        self.__objPaths = {
            "conf": FileManagement("conf"),
            "db": FileManagement("db", ["interfaces", "desktop"]),
            "logs": FileManagement("logs", [], ["lan_audacity.log"]),
            "pixmap": FileManagement("pixmap"),
        }
        self.__networks: list = network_list
        self.__links: list = link_list
        self.__devices: list = device_list
        self.__pixmap: list = pixmap_list
    
    def dict_return(self) -> dict:
        return {
            "software_name": self.__softName,
            "software_version": self.__softVersion,
            "project_name": self.__projectName,
            "save_path": self.__savePath,
            "char_table": self.__charTable,
            "author": self.__author,
            "clock_manager": self.__clockManager.dict_return(),
            "obj_paths": {
                "conf": self.__objPaths["conf"].dict_return(),
                "db": self.__objPaths["db"].dict_return(),
                "logs": self.__objPaths["logs"].dict_return(),
                "pixmap": self.__objPaths["pixmap"].dict_return(),
            },
            "networks": self.__networks,
            "links": self.__links,
            "devices": self.__devices,
            "pixmap": self.__pixmap
        }

"""

# Test de la classe LanAudacity

temp_path = os.getcwd()

# Test de la classe LanAudacity
def test_lan_audacity():
    # Création d'une instance de LanAudacity
    lan_audacity = LanAudacity(
        project_name="Test_Lan_Audacity",
        abs_path=temp_path,
        software_name="Lan Audacity",
        software_version="1.0.0",
        author="John Doe"
    )
    lan_audacity.updateProject_0()

    # Vérification de la création des répertoires et fichiers
    assert os.path.exists(os.path.join(temp_path, "Test_Lan_Audacity")), "Le répertoire du projet n'a pas été créé"
    assert os.path.exists(os.path.join(temp_path, "Test_Lan_Audacity", "lan_audacity.json")), "Le fichier du projet n'a pas été créé"
    assert os.path.exists(os.path.join(temp_path, "Test_Lan_Audacity", "conf")), "Le répertoire conf.d n'a pas été créé"
    assert os.path.exists(os.path.join(temp_path, "Test_Lan_Audacity", "db")), "Le répertoire db.d n'a pas été créé"
    assert os.path.exists(os.path.join(temp_path, "Test_Lan_Audacity", "db", "interfaces")), "Le répertoire interfaces n'a pas été créé"
    assert os.path.exists(os.path.join(temp_path, "Test_Lan_Audacity", "db", "desktop")), "Le répertoire desktop n'a pas été créé"
    assert os.path.exists(os.path.join(temp_path, "Test_Lan_Audacity", "logs")), "Le répertoire logs.d n'a pas été créé"
    assert os.path.exists(os.path.join(temp_path, "Test_Lan_Audacity", "pixmap")), "Le répertoire pixmap.d n'a pas été créé"

    # Vérification du contenu du fichier du projet
    with open(os.path.join(temp_path, "Test_Lan_Audacity", "lan_audacity.json"), "r") as f:
        project_data = json.load(f)
        assert project_data["project_name"] == "Test_Lan_Audacity", "Le nom du projet dans le fichier est incorrect"
        assert project_data["abs_path"] == os.path.join(temp_path, "Test_Lan_Audacity"), "Le chemin d'accès du projet dans le fichier est incorrect"
        assert project_data["software"]["name"] == "Lan Audacity", "Le nom du logiciel dans le fichier est incorrect"
        assert project_data["software"]["version"] == "1.0.0", "La version du logiciel dans le fichier est incorrecte"
        assert project_data["author"] == "John Doe", "Le nom de l'auteur dans le fichier est incorrect"

    # Suppression de l'instance de LanAudacity
    del lan_audacity

# Exécution des tests
test_lan_audacity()
