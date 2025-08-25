from src.classes.configurationFile import ConfigurationFile
from typing import List

VAR_LANGUAGES: List[str] = ["english", "français"]
VAR_LANGUAGE: str = "english"

class LanguageApp:
    def __init__(self, file_manager: ConfigurationFile, language: str = VAR_LANGUAGE, lang_list: list = VAR_LANGUAGES):
        self.data_manager = file_manager.data
        self.langManager = language
        self.langList = lang_list

    @property
    def language(self):
        return self.langManager

    @language.setter
    def language(self, lang: str):
        self.langManager = lang

    @property
    def language_list(self):
        return self.langList

    def get_textTranslate(self, key: str):
        for data in self.data_manager:
            if key in data["string"]:
                return data[self.language]