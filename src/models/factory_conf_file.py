import enum
from typing import Any, Optional, Union
import os
import logging
import inspect
import json
import csv
import yaml
import xmltodict
import configparser


class FactoryConfFile:
    class RWX(enum.Enum):  # Enumération des modes de lecture/écriture des fichiers
        READ = "r"
        WRITE = "w"
        APPEND = "a"
        READ_WRITE = "r+"
        WRITE_READ = "w+"
        APPEND_READ = "a+"

    class FileType(enum.Enum):  # Enumération des types de fichiers acceptés
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

    @file_data.setter
    def file_data(self, data: Any) -> None:
        self.__file_data = data

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
            logging.debug(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: The file {self.file_path} exist."
            )
        else:
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: The file {self.file_path} doesn't exist."
            )
        return exist

    def action_file(self, rw_mode: Optional[RWX]) -> None:
        if rw_mode:
            self.rw_mode = rw_mode
            logging.debug(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: rw_mode set to {rw_mode.name}"
            )

        if self.exist and self.rw_mode == FactoryConfFile.RWX.READ:
            logging.debug(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Reading file {self.file_basename}"
            )
            self.read_file()

        elif self.exist and self.rw_mode == FactoryConfFile.RWX.WRITE:
            logging.debug(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Writing file {self.file_basename}"
            )
            self.write_file()

    def read_file(self) -> None:
        with open(
            file=self.file_path, mode=self.rw_mode.value, encoding=self.file_encoding
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

            elif (
                self.file_type
                == Union[FactoryConfFile.FileType.CONF, FactoryConfFile.FileType.INI]
            ):
                config = configparser.ConfigParser()
                config.read_file(file)
                self.__file_data = config

    def write_file(self) -> None:
        with open(
            file=self.file_path, mode=self.rw_mode.value, encoding=self.file_encoding
        ) as file:
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

            elif (
                self.file_type
                == Union[FactoryConfFile.FileType.CONF, FactoryConfFile.FileType.INI]
            ):
                self.file_data.write(file)

    # def update_file(self) -> None:
    #     pass

