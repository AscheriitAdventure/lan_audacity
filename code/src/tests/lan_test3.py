import os
import logging
from typing import Optional, Any


class FileManagement:
    def __init__(
            self, folder_name: str,
            folder_list: Optional[list[str]] = None,
            files_list: Optional[list[tuple]] = None
    ) -> None:
        self.__path: str = folder_name
        if folder_list is None:
            self.__folders: list[str] = []
        else:
            self.__folders: list[str] = folder_list
        if files_list is None:
            self.__files: list[tuple] = []
        else:
            self.__files: list[tuple] = files_list
    
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
                # insert the folder into the list of folders if it does not exist
                if folder_name not in self.folders:
                    self.add_folder(folder_name)

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
                # insert the file into the list of files if it does not exist
                if (file_name, file_type) not in self.files:
                    self.add_file((file_name, file_type))

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
        str_return = f"Path: {self.__path}, Folders: {self.__folders},  Files: {self.__files}"
        return str_return


import json
import yaml
import xmltodict
import csv
import configparser


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
            time_list: Optional[list[float]] = None
    ) -> None:
        self.__clock_created: float = time_start
        if time_list is None:
            self.__clock_list: list[float] = []
        else:
            self.__clock_list = time_list
        if time_list == [float]:
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
        if not self.clockList:
            return self.clockCreated
        else:
            return self.clockList.pop()

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
from src.models.network import Network


class LanAudacity(FileManagement):
    def __init__(
            self, 
            project_name: str,
            abs_path: str = os.getcwd(),
            folder_list: Optional[list[str]] = None,
            files_list: Optional[list[tuple]] = None,
            software_name: str = "Lan Audacity",
            software_version: str = "1.0.4",
            author: str = "Unknown",
            clock_manager: ClockManager = ClockManager(),
            network_list: Optional[list[dict]] = None,
            link_list: Optional[list[dict]] = None,
            device_list: Optional[list[dict]] = None,
            pixmap_list: Optional[list[dict]] = None
            ) -> None:
        super().__init__(project_name, folder_list, files_list)
        self.__abs_path = abs_path
        self.__software: dict = {
            "name": software_name,
            "version": software_version
        }
        self.__author = author
        self.__objPaths = {}
        self.__clockManager = clock_manager
        self.char_table = "utf-8"

        self.__networks = network_list
        self.__links = link_list
        self.__devices = device_list
        self.__pixmap = pixmap_list
    
    @property
    def pixmap(self) -> list[dict]:
        return self.__pixmap
    
    def setPixmap(self, value: list[dict]) -> None:
        # transform value into a list of Pixmap objects
        self.__pixmap = value

    @property
    def networks(self) -> list[dict]:
        return self.__networks

    @networks.setter
    def networks(self, value: list[dict]) -> None:
        # transform value into a list of Network objects
        self.__networks = value

    @property
    def links(self) -> list[dict]:
        return self.__links
    
    def setLinks(self, value: list[dict]) -> None:
        # transform value into a list of Link objects
        self.__links = value
    
    @property
    def devices(self) -> list[dict]:
        return self.__devices
    
    def setDevices(self, value: list[dict]) -> None:
        # transform value into a list of Device objects
        self.__devices = value
    
    @property
    def clockManager(self) -> ClockManager:
        return self.__clockManager

    @clockManager.setter
    def clockManager(self, clock: ClockManager) -> None:
        self.__clockManager = clock
    
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
            "char_table": self.char_table,
            "abs_path": self.absPath,
            "software": self.software,
            "author": self.author,
            "clock_manager": self.clockManager.dict_return(),
            "obj_paths": self.dict_objPaths(),
            "networks": self.networks,
            "links": self.links,
            "devices": self.devices,
        }
    
    def getOneObjPath(self, obj_path: str) -> FileManagement:
        return self.__objPaths[obj_path]

    def create_project(self):
        self.add_folder(self.path)
        self.generate_file("lan_audacity", "json", self.absPath)
        print(self.dict_return())
        # dump the project data into the json file
        self.updateLanAudacity()
        # Create the folders and files of the project
        cl_infos = [
            {
                "name": "conf",
                "folders": [],
                "files": []
            },
            {
                "name": "db",
                "folders": ["interfaces", "desktop"],
                "files": []
            },
            {
                "name": "logs",
                "folders": [],
                "files": [("lan_audacity", "log")]
            },
            {
                "name": "pixmap",
                "folders": [],
                "files": []
            }
        ]

        for cl_info in cl_infos:
            self.__objPaths[cl_info["name"]] = FileManagement(cl_info["name"])
            fls_mng = self.__objPaths[cl_info["name"]]
            self.generate_folder(fls_mng.path, self.absPath)

            if cl_info["folders"] != []:
                # Set the folders attribute using the setter method
                for folder in cl_info["folders"]:
                    fls_mng.generate_folder(folder, os.path.join(self.absPath, self.path))
            else:
                fls_mng.folders = []

            if cl_info["files"] != []:
                for file in cl_info["files"]:
                    fls_mng.generate_file(file[0], file[1], os.path.join(self.absPath, self.path))
            else:
                fls_mng.files = []
            
        self.updateLanAudacity()
    
    def updateLanAudacity(self):
        # Update the project with the new data
        if self.path in self.absPath:
            SwitchFile2.json_write(os.path.join(self.absPath, "lan_audacity.json"), self.dict_return())
        else:
            SwitchFile2.json_write(os.path.join(self.absPath, self.path, "lan_audacity.json"), self.dict_return())
    
    def delete_project(self) -> None:
        if os.path.exists(os.path.join(self.absPath, self.path)):
            try:
                shutil.rmtree(os.path.join(self.absPath, self.path))
                logging.info(f"{self.path} is deleted")
            except OSError as e:
                logging.error(f"Error remove {self.path} : {e}")
        else:
            logging.info(f"{self.path} doesn't exist")
    
    def update_project(self, old_path: str = os.getcwd()) -> None:
        # Search "lan_audacity.json" in the old path
        if os.path.exists(os.path.join(old_path, "lan_audacity.json")):
            # Load the data from the old path
            old_data = SwitchFile2.json_read(os.path.join(old_path, "lan_audacity.json"))
            # Compare the data from the old path with the current data
            if old_data != self.dict_return():
                # Update the project with the new data
                print(f"abs_path: {old_data['abs_path']}")
                print(f"char_table: {old_data['char_table']}")
                print(f"project_name: {old_data['project_name']}")
                print(f"software: {old_data['software']}")
                print(f"author: {old_data['author']}")
                print(f"clock_manager: {old_data['clock_manager']}")
                print(f"obj_paths: {old_data['obj_paths']}")
                print(f"networks: {old_data['networks']}")
                print(f"links: {old_data['links']}")
                print(f"devices: {old_data['devices']}")
                print(f"pixmap: {old_data['pixmap']}")
            else:
                logging.info(f"{self.path} is already up to date")
        else:
            logging.error(f"File 'lan_audacity.json' not found in {old_path}")
    
    def add_network(self, network: dict | Network) -> None:
        if self.networks is None:
            # Vérifie le champ list de "__networks" et l'initialise
            self.networks = {"path": "interfaces", "obj_ls": []}
        if isinstance(network, Network):
            # Vérifie si la variable "network" est bien un objet Network
            self.networks["obj_ls"].append(
                {
                    "uuid": network.uuid,
                    "name": network.name,
                    "path": network.absPath,
                    "ls_devices": [],
                })
            self.clockManager.add_clock()
            if self.path in self.absPath:
                chemin = os.path.join(self.absPath, "lan_audacity.json")
            else:
                chemin = os.path.join(self.absPath, self.path, "lan_audacity.json")
            with open(chemin, "w") as f:
                json.dump(self.dict_return(), f, indent=4)
            logging.info(f"{network.name} is added to {self.path}")
        elif isinstance(network, dict):
            # Vérifie si la variable "network" est bien un objet Network
            print(network)
        else:
            logging.error("The network object is not a Network object or a dictionary.")
    
    def remove_network(self, network: str | Network) -> None:
        if isinstance(network, Network):
            if self.networks is not None:
                self.networks["obj_ls"].remove(network.uuid)
                self.clockManager.add_clock()
                with open(
                        f"{self.absPath}/lan_audacity.json", "w"
                ) as f:
                    json.dump(self.__dict__, f, indent=4)
                logging.info(f"{network.name} is removed from {self.path}")
            else:
                logging.info(f"{network.name} doesn't exist in {self.path}")
        elif isinstance(network, str):
            # the network variable is  the uuid of the network
            if self.networks is not None:
                self.networks["obj_ls"].remove(network)
                self.clockManager.add_clock()
                with open(
                        f"{self.absPath}/lan_audacity.json", "w"
                ) as f:
                    json.dump(self.__dict__, f, indent=4)
                logging.info(f"{network} is removed from {self.path}")
            else:
                logging.info(f"{network} doesn't exist in {self.path}")
        else:  
            logging.error("The network object is not a Network object or a string.")

    def getObjNetwork(self, network_name):
        for network in self.networks.get('obj_ls', []):
            if network.get('name') == network_name:
                net_data = SwitchFile2.json_read(network['path'])
                logging.debug(net_data['name'])
                network_object = Network(
                    network_ipv4=net_data['ipv4'], network_mask_ipv4=net_data['mask_ipv4'], save_path=net_data['abs_path'],
                    network_name=net_data['name'], network_ipv6=net_data['ipv6'], network_gateway=net_data['gateway'],
                    network_dns=net_data['dns'], network_dhcp=net_data['dhcp'], uuid_str=net_data['uuid']
                )
                network_object.clockManager = ClockManager(net_data['clock_manager']['clock_created'], net_data['clock_manager']['clock_list'])
                return network_object
        return None

    # def add_link(self, link: dict) -> None:
    # def remove_link(self, link: dict) -> None:
    # def add_device(self, device: dict) -> None:
    # def remove_device(self, device: dict) -> None:
    # def add_pixmap(self, pixmap: dict) -> None:
    # def remove_pixmap(self, pixmap: dict) -> None:


# Test de la classe LanAudacity

temp_path = os.getcwd()

# Test de la classe LanAudacity
def test_lan_audacity():
    # Création d'une instance de LanAudacity
    lan_audacity = LanAudacity(
        project_name="Test_Lan_Audacity",
        abs_path=temp_path,
        software_name="Lan Audacity",
        software_version="1.0.4",
        author="John Doe"
    )
    # print(lan_audacity.dict_return())
    lan_audacity.create_project()

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
        assert project_data["abs_path"] == temp_path, "Le chemin d'accès du projet dans le fichier est incorrect"
        assert project_data["software"]["name"] == "Lan Audacity", "Le nom du logiciel dans le fichier est incorrect"
        assert project_data["software"]["version"] == "1.0.4", "La version du logiciel dans le fichier est incorrecte"
        assert project_data["author"] == "John Doe", "Le nom de l'auteur dans le fichier est incorrect"

    chemin_lan_1 = os.path.join(lan_audacity.absPath, lan_audacity.path, "db", "interfaces")
    # print(chemin_lan_1)
    lan_1 = Network("192.168.90.0", "255.255.255.0", chemin_lan_1, "Siège de Eyrein Industrie", None, "192.168.90.254")

    lan_audacity.add_network(lan_1)
    lan_audacity.updateLanAudacity()



    # Suppression de l'instance de LanAudacity
    lan_audacity.delete_project()
    del lan_audacity

# Exécution des tests
test_lan_audacity()
