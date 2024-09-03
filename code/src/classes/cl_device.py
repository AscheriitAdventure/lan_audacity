from typing import Any, Optional

import json
import logging
import os
import subprocess
import uuid

from classes.clockManager import ClockManager
from classes.cl_deviceType import DeviceType


class Device:
    def __init__(
            self,
            device_ipv4: str,
            mask_ipv4: str,
            save_path: str,
            device_name: Optional[str] = None,
            uuid_str: Optional[str] = None
            ) -> None:
        self.__uuid = None
        self.setUUIDObj(uuid_str)
        self.__is_connected: bool = False
        self.__clockManager = ClockManager()
        self.__name = device_name
        self.__ipv4 = device_ipv4
        self.__mask_ipv4 = mask_ipv4
        self.__ipv6: Optional[str] = None
        self.__mask_ipv6: Optional[str] = None
        self.__type: Optional[DeviceType] = None
        self.__os: Optional[str] = None
        self.__model: Optional[str] = None
        self.__brand: Optional[str] = None
        self.__mac: Optional[str] = None
        self.__gateway: Optional[str] = None
        self.__dns: Optional[str] = None
        self.__snmp: Optional[str] = None
        self.__ssh: Optional[str] = None
        self.__data: Optional[str] = None

        self.__links = []

        if uuid_str is None:
            self.absPath = f"{save_path}/{self.uuid}.json"
            self.create_file()
        else:
            self.absPath = save_path
            self.open_file()
    
    @property
    def macAddress(self) -> str | None:
        return self.__mac
    
    @macAddress.setter
    def macAddress(self, new_mac: str):
        self.__mac = new_mac
    
    @property
    def gateway(self) -> str | None:
        return self.__gateway
    
    @gateway.setter
    def gateway(self, new_gateway: str):
        self.__gateway = new_gateway
    
    @property
    def ipv6(self) -> str | None:
        return self.__ipv6
    
    @ipv6.setter
    def ipv6(self, new_ipv6: str):
        self.__ipv6 = new_ipv6
    
    @property
    def maskIpv6(self) -> str | None:
        return self.__mask_ipv6
    
    @maskIpv6.setter
    def maskIpv6(self, new_mask_ipv6: str):
        self.__mask_ipv6 = new_mask_ipv6
    
    @property
    def type(self) -> DeviceType | None:
        return self.__type
    
    @type.setter
    def type(self, new_type: dict | DeviceType):
        self.__type = new_type

    @property
    def isConnected(self):
        return self.__is_connected

    @isConnected.setter
    def isConnected(self, var: bool):
        self.__is_connected = var
    
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

    def setUUIDObj(self, new_uuid: Optional[str] = None):
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
    def clockManager(self) -> ClockManager:
        return self.__clockManager

    @clockManager.setter
    def clockManager(self, clock: ClockManager) -> None:
        self.__clockManager = clock

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
    def linksList(self) -> list:
        return self.__links
    
    def create_file(self) -> None:
        if not os.path.exists(self.absPath):
            with open(self.absPath, "w+") as f:
                json.dump(self.dict_return(), f, indent=4, default=str)
            logging.info(f"{self.name} is created")
        else:
            logging.info(f"{self.name} already exists")

    def open_file(self) -> Any:
        if os.path.exists(self.absPath):
            with open(self.absPath, "r") as f:
                return json.load(f)
        else:
            logging.info(f"{self.name} doesn't exist")
            return {}

    def save_file(self) -> None:
        if os.path.exists(self.absPath):
            self.clockManager.add_clock()
            with open(self.absPath, "w") as f:
                json.dump(self.dict_return(), f, indent=4, default=str)
            logging.info(f"{self.name} is saved")
        else:
            logging.info(f"{self.name} doesn't exist")

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
            "dhcp": self.dhcp,
            "links_list": self.linksList,
        }

    def keys(self) -> list:
        return list(self.dict_return().keys())
    
    @staticmethod
    def from_dict(device_dict: dict) -> Device:  # type: ignore
        new_device = Device(
            device_dict["ipv4"],
            device_dict["mask_ipv4"],
            device_dict["abs_path"],
            device_dict["name"],
            device_dict["uuid"]
        )
        new_device.clockManager = ClockManager.from_dict(device_dict["clock_manager"])
        new_device.__ipv6 = device_dict["ipv6"]
        new_device.__gateway = device_dict["gateway"]
        new_device.__dns = device_dict["dns"]
        new_device.__links = device_dict["links_list"]
        return new_device
    
    def set_isConnected(self) -> None:
        try:
            result = subprocess.run(
                ["ping", "-c4", self.ipv4],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
            if result.returncode == 0:
                self.isConnected = True
                logging.info("La machine est connectée.")
            else:
                self.isConnected = False
                logging.error("La machine n'est pas connectée.")
        except subprocess.TimeoutExpired:
            self.isConnected = False
            logging.error("Timeout lors de la tentative de connexion à la machine.")
    
    def update_auto(self):
        pass

    def update_obj(self):
        pass

    def set_deviceName(self, new_name: Optional[str]) -> None:
        if new_name == "" or new_name is None:
            self.__name = f"Device_{self.ipv4}"
        else:
            self.__name = new_name