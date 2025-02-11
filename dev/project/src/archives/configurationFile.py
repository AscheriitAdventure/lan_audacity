from dev.project.src.classes.switchFile import SwitchFile
import os
import logging
import string
import inspect


class ConfigurationFile:
    def __init__(self, abs_path: str):
        self.__abs_path: str = abs_path
        self.__file: str = os.path.basename(abs_path)
        self.__data = self.load_file()

    @property
    def abs_path(self) -> str:
        return self.__abs_path

    @abs_path.setter
    def abs_path(self, abs_path: str) -> None:
        if abs_path:
            self.__abs_path = abs_path
        else:
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Le chemin du fichier de configuration est vide ou non-renseigné."
            )

    @property
    def file(self) -> str:
        return self.__file

    @property
    def data(self) -> any:
        return self.__data

    def load_file(self) -> any:
        switch_file = SwitchFile()
        if os.path.exists(self.abs_path):
            return getattr(
                switch_file,
                ConfigurationFile.get_extension(self.abs_path)+"_read",
                switch_file.txt_read,
            )(self.abs_path)
        else:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Le fichier de configuration {self.file} n'existe pas.")
            return None

    def get_value(self, key: str) -> str | None:
        if self.data:
            return self.data.get(key)
        else:
            logging.warning(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Aucune configuration chargée ou trouvée.")
            return None

    @staticmethod
    def get_extension(abs_path: str) -> str:
        _, file_extension = os.path.splitext(abs_path)
        return file_extension.lower().strip(string.punctuation)
