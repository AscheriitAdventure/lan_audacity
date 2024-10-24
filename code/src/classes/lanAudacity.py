import os
import logging
import json
import shutil
from typing import Optional

from src.classes.fileManagement import FileManagement
from src.classes.clockManager import ClockManager
from src.classes.switchFile import SwitchFile
from src.classes.cl_network import Network




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
            SwitchFile.json_write(os.path.join(self.absPath, "lan_audacity.json"), self.dict_return())
        else:
            SwitchFile.json_write(os.path.join(self.absPath, self.path, "lan_audacity.json"), self.dict_return())
    
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
            old_data = SwitchFile.json_read(os.path.join(old_path, "lan_audacity.json"))
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
            logging.warning("The network object is not a Network object or a string.")

    def getObjNetwork(self, network_name):
        for network in self.networks.get('obj_ls', []):
            if network.get('name') == network_name:
                net_data = SwitchFile.json_read(network['path'])
                network_object = Network(
                    network_ipv4=net_data['ipv4'], network_mask_ipv4=net_data['mask_ipv4'], save_path=net_data['abs_path'],
                    network_name=net_data['name'], network_ipv6=net_data['ipv6'], network_gateway=net_data['gateway'],
                    network_dns=net_data['dns'], uuid_str=net_data['uuid']
                )
                network_object.clockManager = ClockManager(net_data['clock_manager']['clock_created'], net_data['clock_manager']['clock_list'])
                network_object.devicesList = net_data['devices_list'] if 'devices_list' in net_data else []
                return network_object
        return None

    # def add_link(self, link: dict) -> None:
    # def remove_link(self, link: dict) -> None:
    # def add_device(self, device: dict) -> None:
    # def remove_device(self, device: dict) -> None:
    # def add_pixmap(self, pixmap: dict) -> None:
    # def remove_pixmap(self, pixmap: dict) -> None: