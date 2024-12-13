from typing import Optional, Any, Union
import logging
import json
import yaml
import xmltodict
import csv
import os
import enum
import configparser
import inspect

""" 
    Remarques:
    Suite à la création de la classe ConfigurationFile, il est devenu difficile de gérer les fichiers de configuration.
    Gérer des classes est devenu un casse-tête, surtout les classes de type management qui gère beaucoup de données.
    Objectifs:
    - Créer une classe qui gère les fichiers de configuration ou les fichiers de données.
    - Cette classe doit être capable de lire
    - Cette classe doit être capable d'écrire
    - Cette classe doit être capable de modifier [?]
    - 
"""


class FactoryConfFile:
    class RWX(enum.Enum): # Enumération des modes de lecture/écriture des fichiers
        READ = "r"
        WRITE = "w"
        APPEND = "a"
        READ_WRITE = "r+"
        WRITE_READ = "w+"
        APPEND_READ = "a+"
    
    class FileType(enum.Enum): # Enumération des types de fichiers acceptés
        JSON = "json"
        YAML = "yaml"
        XML = "xml"
        CSV = "csv"
        TXT = "txt"
        CONF = "conf" 
        INI = "ini"
    
    def __init__(self, file_path: str, rw_mode: RWX = RWX.READ) -> None:
        """ 
        Classe de gestion des fichiers de configuration.

        Args:
            file_path (str): Chemin absolue du fichier. Ne fonctionne pas avec les chemins relatifs.
            rw_mode (RWX, optional): Permet de savoir qu'elles sont les actions possible sur le fichier, valeur par
                    defaut lecture. Defaults to RWX.READ.
        """
        self.file_path = file_path
        self.file_type = self.get_file_type(file_path)
        self.file_basename = os.path.basename(file_path)
        self.__file_data: Any
        self.exist: bool = self.check_file_exist()
        self.__encoding = "utf-8"
        self.__rw_mode = rw_mode
  
    @property
    def file_encoding(self) -> str:
        return self.__encoding
    
    def set_file_encoding(self, encoding: str) -> None:
        self.__encoding = encoding
    
    @property
    def file_data(self) -> Any:
        return self.__file_data
    
    @property
    def rw_mode(self) -> RWX:
        return self.__rw_mode
    
    @rw_mode.setter
    def rw_mode(self, rw_mode: RWX) -> None:
        self.__rw_mode = rw_mode
    
    @staticmethod
    def get_file_type(file_path: str) -> FileType:
        file_extension = file_path.split(".")[-1]
        res_file_type = getattr(FactoryConfFile.FileType, file_extension.upper())
        return res_file_type
    
    def check_file_exist(self) -> bool:
        exist = os.path.exists(self.file_path)
        if exist:
            logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: The file {self.file_path} exist.")
        else:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: The file {self.file_path} doesn't exist.")
        return exist

    def action_file(self, rw_mode: Optional[RWX]) -> None:
        if rw_mode:
            self.rw_mode = rw_mode
            logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: rw_mode set to {rw_mode.name}")
        
        if self.exist and self.rw_mode == FactoryConfFile.RWX.READ:
            logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Reading file {self.file_basename}")
            self.read_file()
        
        elif self.exist and self.rw_mode == FactoryConfFile.RWX.WRITE:
            logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Writing file {self.file_basename}")
            self.write_file()
        
    def read_file(self) -> None:
        with open(
            file=self.file_path,
            mode=self.rw_mode.value,
            encoding=self.file_encoding
        ) as file:
            if self.file_type == FactoryConfFile.FileType.JSON:
                self.__file_data = json.load(file)

            elif self.file_type == FactoryConfFile.FileType.YAML:
                self.__file_data = yaml.load(file, Loader=yaml.FullLoader)

            elif self.file_type == FactoryConfFile.FileType.XML:
                self.__file_data = xmltodict.parse(file.read())

            elif self.file_type == FactoryConfFile.FileType.TXT:
                self.__file_data = file.read()

            elif self.file_type == FactoryConfFile.FileType.CSV:
                self.__file_data = csv.DictReader(file)

            elif self.file_type == Union[FactoryConfFile.FileType.CONF, FactoryConfFile.FileType.INI]:
                config = configparser.ConfigParser()
                config.read_file(file)
                self.__file_data = config
    
    def write_file(self) -> None:
        with open(file=self.file_path, mode=self.rw_mode.value, encoding=self.file_encoding) as file:
            if self.file_type == FactoryConfFile.FileType.JSON:
                json.dump(self.file_data, file, indent=4)
            
            elif self.file_type == FactoryConfFile.FileType.YAML:
                yaml.dump(self.file_data, file)
            
            elif self.file_type == FactoryConfFile.FileType.XML:
                file.write(xmltodict.unparse(self.file_data, pretty=True))
            
            elif self.file_type == FactoryConfFile.FileType.TXT:
                file.write(self.file_data)
            
            elif self.file_type == FactoryConfFile.FileType.CSV:
                csv_writer = csv.DictWriter(file, fieldnames=self.file_data[0].keys())
                csv_writer.writeheader()
                csv_writer.writerows(self.file_data)
            
            elif self.file_type == Union[FactoryConfFile.FileType.CONF, FactoryConfFile.FileType.INI]:
                self.file_data.write(file)
    
    # def update_file(self) -> None:
    #     pass

import qtawesome as qta
from qtpy.QtGui import QIcon

class IconsManager(FactoryConfFile):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path, FactoryConfFile.RWX.READ)
        self.action_file(self.rw_mode)
    
    def get_icon(self, icon_name: str) -> Optional[QIcon]:
        for data in self.file_data:
            if data["name"] == icon_name:
                if data["options"] is None:
                    ico_obj = qta.icon(*data["platform_and_name"])
                else:
                    ico_obj = qta.icon(
                        *data["platform_and_name"], options=data["options"]
                    )
                return ico_obj
        return None

class ShortcutsManager(FactoryConfFile):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path, FactoryConfFile.RWX.READ)
        self.action_file(self.rw_mode)
    
    def get_shortcut(self, shortcut_name: str) -> Optional[str]:
        for data in self.file_data:
            if data["name"] == shortcut_name:
                return data["shortcut"]
        return None

class MenuBarManager(FactoryConfFile):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path, FactoryConfFile.RWX.READ)
        self.action_file(self.rw_mode)
    
    def get_menu_name(self, menu_name: str) -> Optional[str]:
        for data in self.file_data:
            if data["name"] == menu_name:
                return data["title"]
        return None
    
    def get_one_menu(self, menu_name: str) -> Optional[dict]:
        for data in self.file_data:
            if data["name"] == menu_name:
                return data
        return None
    
    def get_one_action(self, menu_name: str, action_name: str) -> Optional[dict]:
        menu = self.get_one_menu(menu_name)
        if menu is not None:
            for action in menu["actions"]:
                if action["name_low"] == action_name:
                    return action
        
        return None
    