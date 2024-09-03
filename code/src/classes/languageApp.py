from src.classes.configurationFile import ConfigurationFile


class LanguageApp:
    def __init__(self, file_manager: ConfigurationFile):
        self.data_manager = file_manager.data
        self.langManager: str = "english"
        self.langList = ["english", "français"]

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