import json
import yaml
import xmltodict
import csv
import configparser


class SwitchFile:
    @staticmethod
    def json(abs_path: str) -> any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def yaml(abs_path: str) -> any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    @staticmethod
    def xml(abs_path: str):
        with open(abs_path, "r+", encoding="utf-8") as file:
            return xmltodict.parse(file.read())

    @staticmethod
    def csv(abs_path: str) -> any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return csv.DictReader(file)

    @staticmethod
    def txt(abs_path: str):
        with open(abs_path, "r+", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def ini(abs_path: str) -> any:
        config = configparser.ConfigParser()
        config.read(abs_path, encoding="utf-8")
        return config

    @staticmethod
    def conf(abs_path: str) -> any:
        config = configparser.ConfigParser()
        config.read(abs_path)
        return config
