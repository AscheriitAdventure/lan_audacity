import json
import yaml
import xmltodict
import csv
import configparser

from typing import Any


class SwitchFile:
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