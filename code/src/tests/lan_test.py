import os
import time
import logging
import json
import shutil

from src.models.switch_file import SwitchFile

DFLT_STR_V = "Unknown"

class LanAudacity:
    def __init__(
            self,
            software_version: str = "1.0.4",
            project_name: str = DFLT_STR_V,
            save_path: str = DFLT_STR_V,
            author: str = DFLT_STR_V,
        ) -> None:
        # Fichier de référence pour le logiciel "Lan Audacity"
        self.refFile = "lan_audacity.json"
        self.__softName = "Lan Audacity"
        self.__softVersion = software_version
        self.__projectName = project_name
        self.__savePath = save_path
        self.__author = author
        self.__dateUnix: float = time.time()
        self.__lastUpdateUnix: float = time.time()
        self.__charTable = "utf-8"
        self.__objPaths = {
            "conf": {
                "path": "conf",
                "folders": [],
                "files": []
            },
            "db": {
                "path": "db",
                "folders": ["interfaces", "desktop"],
                "files": [],
            },
            "logs": {
                "path": "logs",
                "folders": [],
                "files": ["lan_audacity.log"]
            },
            "pixmap": {
                "path": "pixmap",
                "folders": [],
                "files": []
            },
        }
        self.__networks: list = []
        self.__links: list = []
        self.__devices: list = []
        self.__pixmap: list = []
    
    @property
    def softwareName(self) -> str:
        return self.__softName
    
    @property
    def softwareVersion(self) -> str:
        return self.__softVersion
    
    @property
    def projectName(self) -> str:
        return self.__projectName
    
    @property
    def savePath(self) -> str:
        return self.__savePath
    
    @property
    def author(self) -> str:
        return self.__author
    
    @property
    def dateUnix(self) -> float:
        return self.__dateUnix
    
    @property
    def lastUpdateUnix(self) -> float:
        return self.__lastUpdateUnix
    
    @property
    def charTable(self) -> str:
        return self.__charTable
    
    @property
    def objPaths(self) -> dict:
        return self.__objPaths
    
    @property
    def networks(self) -> list:
        return self.__networks
    
    @property
    def links(self) -> list:
        return self.__links
    
    @property
    def devices(self) -> list:
        return self.__devices
    
    @property
    def pixmap(self) -> list:
        return self.__pixmap
    
    @softwareName.setter
    def softwareName(self, value: str) -> None:
        if not isinstance(value, str) or not value:
            raise ValueError("The software name must be a non-empty string.")
        else:
            self.__softName = value
    
    @softwareVersion.setter
    def softwareVersion(self, value: str) -> None:
        # Vérification de la validité de la version
        if not isinstance(value, str) or not value:
            raise ValueError("The software version must be a non-empty string.")
        else:
            self.__softVersion = value
    
    @projectName.setter
    def projectName(self, value: str) -> None:
        if not isinstance(value, str) or not value:
            raise ValueError("The project name must be a non-empty string.")
        else:
            self.__projectName = value
    
    @savePath.setter
    def savePath(self, value: str) -> None:
        if not isinstance(value, str) or not value:
            raise ValueError("The save path must be a non-empty string.")
        else:
            self.__savePath = value
    
    @author.setter
    def author(self, value: str) -> None:
        if not isinstance(value, str) or not value:
            raise ValueError("The author must be a non-empty string.")
        else:
            self.__author = value
    
    @dateUnix.setter
    def dateUnix(self, value: float) -> None:
        if not isinstance(value, float) or value < 0:
            raise ValueError("The date must be a positive float.")
        else:
            self.__dateUnix = value
    
    @lastUpdateUnix.setter
    def lastUpdateUnix(self, value: float) -> None:
        if not isinstance(value, float) or value < 0:
            raise ValueError("The last update must be a positive float.")
        else:
            self.__lastUpdateUnix = value
    
    def setSavePath(self, new_path: str) -> None:
        if os.path.exists(new_path):
            path_part1 = f"{new_path}/{self.projectName}"
            if os.path.isdir(path_part1) and os.path.exists(f"{path_part1}/{self.refFile}"):
                logging.warning(f"The project {self.projectName} already exists in {new_path}.")
                self.load_project(new_path)
            else:
                self.savePath = new_path
                logging.info(f"The save path of {self.projectName} is set to {new_path}.")
              
    def create_project(self) -> None:
        path_part1 = f"{self.savePath}/{self.projectName}"
        if not os.path.exists(path_part1):
            os.mkdir(path_part1)
            with open(f"{path_part1}/{self.refFile}", "w") as f:
                json.dump(self.__dict__, f, indent=4)
            for key, value in self.objPaths.items():
                os.mkdir(f"{path_part1}/{value['path']}")
                if value["folders"]:
                    for folder in value["folders"]:
                        os.mkdir(f"{path_part1}/{value['path']}/{folder}")
                if value["files"]:
                    for file in value["files"]:
                        with open(f"{path_part1}/{value['path']}/{file}", "w") as f:
                            f.write("")
            logging.info(f"{self.projectName} is created in {path_part1}.")

    def load_project(self, path: str) -> None:
        path_part1 = f"{path}/{self.projectName}"
        swift_read = SwitchFile()
        if os.path.exists(path_part1) and os.path.exists(f"{path_part1}/{self.refFile}"):
            data_swiftRead = swift_read.json(f"{path_part1}/{self.refFile}")
            self.softwareName = data_swiftRead["software"]
            self.softwareVersion = data_swiftRead["version"]
            self.savePath = path_part1
            self.author = data_swiftRead["author"]
            self.dateUnix = data_swiftRead["date_unix"]
            self.lastUpdateUnix = time.time()
            self.charTable = data_swiftRead["char_table"]
            self.objPaths = data_swiftRead["objPaths"]
            self.networks = data_swiftRead["networks"]
            self.links = data_swiftRead["links"]
            self.devices = data_swiftRead["devices"]
            self.pixmap = data_swiftRead["pixmap"]
            logging.info(f"{self.projectName} is loaded from {path}.")
        else:
            logging.error(f"The project {self.projectName} does not exist in {path}.")

    def save_project(self) -> None:
        part_part1 = f"{self.savePath}/{self.projectName}"
        with open(f"{part_part1}/{self.refFile}", "w") as f:
            self.lastUpdateUnix = time.time()
            json.dump(self.__dict__, f, indent=4)
        logging.info(f"{self.projectName} is saved in {self.savePath}.")

    def delete_project(self) -> None:
        part_part1 = f"{self.savePath}/{self.projectName}"
        if os.path.exists(path=part_part1):
            try:
                shutil.rmtree(part_part1)
                logging.info(f"{self.projectName} is deleted")
            except OSError as e:
                logging.info(f"Error remove {self.projectName} : {e}")
        else:
            logging.info(f"{self.projectName} doesn't exist")
