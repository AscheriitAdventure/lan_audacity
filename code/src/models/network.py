from typing import Optional, Union
import os
import json
import logging
import time
import uuid

from src.models.device import Device


def ip_to_cidr(ip: str, mask: str) -> str:
    # Split the IP address and the subnet mask into their respective octets
    ip_octets = list(map(int, ip.split('.')))
    mask_octets = list(map(int, mask.split('.')))

    # Convert the subnet mask into its binary representation and count the number of 1s
    mask_binary_str = ''.join(format(octet, '08b') for octet in mask_octets)
    cidr_prefix = mask_binary_str.count('1')

    # Combine the IP address with the CIDR prefix to form the CIDR notation
    cidr_notation = f"{ip}/{cidr_prefix}"

    return cidr_notation


class Network:
    def __init__(
            self,
            network_ipv4: str,
            network_mask_ipv4: str,
            save_path: str,
            network_name: str | None = None,
            network_ipv6: Optional[str] = None,
            network_gateway: Optional[str] = None,
            network_dns: Optional[str] = None,
            network_dhcp: Optional[str] = None,
            uuid_str: Optional[str] = None,
    ):
        self.__uuid = None
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
        self.__dhcp: Optional[str] = network_dhcp
        self.__date_unix: float = time.time()
        self.__last_update_unix: float = time.time()
        self.__abs_path: str = ""

        self.__devices = []

        if uuid_str is None:
            self.absPath = f"{save_path}/{self.uuid}.json"
            self.create_network()
        else:
            self.absPath = save_path
            self.open_network()

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
    def dhcp(self) -> str | None:
        return self.__dhcp

    @property
    def dateUnix(self) -> float:
        return self.__date_unix

    @property
    def lastUpdateUnix(self) -> float:
        return self.__last_update_unix

    @lastUpdateUnix.setter
    def lastUpdateUnix(self, new_time: float):
        self.__last_update_unix = new_time

    @property
    def devicesList(self) -> list:
        return self.__devices

    def create_network(self) -> None:
        if not os.path.exists(self.absPath):
            with open(self.absPath, "w+") as f:
                json.dump(self.__dict__, f, indent=4, default=str)
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
            self.lastUpdateUnix = time.time()
            with open(self.absPath, "w") as f:
                json.dump(self.__dict__, f, indent=4, default=str)
            logging.info(f"{self.name} is saved")
        else:
            logging.info(f"{self.name} doesn't exist")

    def add_device(self, device: Device) -> None:
        self.devices.append(device.uuid)
        self.lastUpdateUnix = time.time()
        with open(self.absPath, "w") as f:
            json.dump(self.__dict__, f, indent=4)
        logging.info(f"{device.name} is added to {self.name}")

    def remove_device(self, device: Device) -> None:
        self.devices.remove(device.uuid)
        self.lastUpdateUnix = time.time()
        device.delete_device()
        with open(self.absPath, "w") as f:
            json.dump(self.__dict__, f, indent=4)
        logging.info(f"{device.name} is removed from {self.name}")
    
    def __str__(self) -> str:
        return f"{self.name} - {self.ipv4} - {self.mask_ipv4}"


