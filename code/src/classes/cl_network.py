from typing import Optional, Union
import json
import logging
import os
import uuid

from src.classes.clockManager import ClockManager
from src.classes.cl_device import Device

from src.functionsExt import ip_to_cidr


class Network:
    def __init__(
            self,
            network_ipv4: str,
            network_mask_ipv4: str,
            save_path: str,
            network_name: Optional[str] = None,
            network_ipv6: Optional[str] = None,
            network_gateway: Optional[str] = None,
            network_dns: Optional[str] = None,
            uuid_str: Optional[str] = None,
    ):
        self.setUUIDObj(uuid_str)
        if network_name is None:
            self.__name: str = ip_to_cidr(network_ipv4, network_mask_ipv4)
        else:
            self.__name: str = network_name

        self.__ipv4: str = network_ipv4
        self.__mask_ipv4: str = network_mask_ipv4
        self.__ipv6: Optional[str] = network_ipv6
        self.__gateway: Optional[str] = network_gateway
        self.__dns: Optional[str] = network_dns
        self.__clockManager = ClockManager()
        self.__abs_path: str = ""

        self.__devices = []
        self.__isConnected: bool = False

        if uuid_str is None:
            self.absPath = f"{save_path}/{self.uuid}.json"
            self.create_network()
        else:
            self.absPath = save_path
            self.open_network()

    @property
    def isConnected(self):
        return self.__isConnected

    @isConnected.setter
    def isConnected(self, var: bool):
        self.__isConnected = var

    @property
    def absPath(self):
        return self.__abs_path

    @absPath.setter
    def absPath(self, new_path: str) -> None:
        try:
            new_path = os.path.abspath(new_path)
            if not os.path.exists(new_path):
                raise ValueError("The path does not exist.")
        except (ValueError, FileNotFoundError) as e:
            logging.error(f"Invalid path: {new_path}. Error: {e}")
        self.__abs_path = new_path

    @property
    def ipv4(self) -> str:
        return self.__ipv4

    @property
    def uuid(self) -> str:
        return self.__uuid

    @uuid.setter
    def uuid(self, new_uuid: str):
        if new_uuid != "" and new_uuid is not None:
            self.__uuid = new_uuid

    def setUUIDObj(self, new_uuid: str = None):
        if new_uuid == "" or new_uuid is None:
            self.uuid = str(uuid.uuid4())
        else:
            self.uuid = new_uuid

    @property
    def name(self) -> str | None:
        return self.__name

    @name.setter
    def name(self, new_name: str):
        if new_name != "" and new_name is not None:
            self.__name = new_name

    @property
    def maskIpv4(self) -> str:
        return self.__mask_ipv4

    @property
    def ipv6(self) -> str | None:
        return self.__ipv6

    @property
    def gateway(self) -> str | None:
        return self.__gateway

    @property
    def dns(self) -> str | None:
        return self.__dns

    @property
    def clockManager(self) -> ClockManager:
        return self.__clockManager

    @clockManager.setter
    def clockManager(self, clock: ClockManager) -> None:
        self.__clockManager = clock

    @property
    def devicesList(self) -> list:
        return self.__devices

    @devicesList.setter
    def devicesList(self, devices: list) -> None:
        self.__devices = devices

    def create_network(self) -> None:
        if not os.path.exists(self.absPath):
            with open(self.absPath, "w+") as f:
                json.dump(self.dict_return(), f, indent=4, default=str)
            logging.info(f"{self.name} is created")
        else:
            logging.info(f"{self.name} already exists")

    def open_network(self) -> Union[list, dict]:
        if os.path.exists(self.absPath):
            with open(self.absPath, "r") as f:
                return json.load(f)
        else:
            logging.info(f"{self.name} doesn't exist")
            return {}

    def save_network(self) -> None:
        if os.path.exists(self.absPath):
            self.clockManager.add_clock()
            with open(self.absPath, "w") as f:
                json.dump(self.dict_return(), f, indent=4, default=str)
            logging.info(f"{self.name} is saved")
        else:
            logging.info(f"{self.name} doesn't exist")

    def add_device(self, device: Device) -> None:
        self.__devices.append(device.uuid)
        self.clockManager.add_clock()
        with open(self.absPath, "w") as f:
            json.dump(self.dict_return(), f, indent=4)
        logging.info(f"{device.nameObj} is added to {self.name}")

    def remove_device(self, device: Device) -> None:
        self.devices.remove(device.uuid)
        self.clockManager.add_clock()
        device.delete_device()
        with open(self.absPath, "w") as f:
            json.dump(self.dict_return(), f, indent=4)
        logging.info(f"{device.nameObj} is removed from {self.name}")

    def dict_return(self) -> dict:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "abs_path": self.absPath,
            "clock_manager": self.clockManager.dict_return(),
            "ipv4": self.ipv4,
            "mask_ipv4": self.maskIpv4,
            "ipv6": self.ipv6,
            "gateway": self.gateway,
            "dns": self.dns,
            "devices_list": self.__devices
        }

    def keys(self) -> list:
        return ["Name", "IPv4", "Mask IPv4", "IPv6", "Gateway", "Nom de Domaine"]

    def __str__(self) -> str:
        return f"{self.name} - {self.ipv4} - {self.maskIpv4}"