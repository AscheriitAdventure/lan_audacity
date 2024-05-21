import logging
import os
import string
from src.models.switch_class import SwitchFile


class ConfigurationFile:
    def __init__(self, abs_path: str):
        self.__abs_path: str = abs_path
        self.__file: str = os.path.basename(abs_path)
        self.__data = self.load_file()

    @property
    def abs_path(self) -> str:
        return self.__abs_path

    @abs_path.setter
    def abs_path(self, absPath: str) -> None:
        if absPath:
            self.__abs_path = absPath
        else:
            logging.error(
                "Le chemin du fichier de configuration est vide ou non-renseigné."
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
                ConfigurationFile.get_extension(self.abs_path),
                switch_file.txt,
            )(self.abs_path)
        else:
            logging.error(f"Le fichier de configuration {self.file} n'existe pas.")
            return None

    def get_value(self, key: str) -> str | None:
        if self.data:
            return self.data.get(key)
        else:
            logging.warning("Aucune configuration chargée ou trouvée.")
            return None

    @staticmethod
    def get_extension(abs_path: str) -> str:
        _, file_extension = os.path.splitext(abs_path)
        return file_extension.lower().strip(string.punctuation)