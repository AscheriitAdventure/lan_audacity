from typing import Optional, Union
import os
import json
import logging
import time
import uuid

from src.models.device import Device


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
            network_dhcp: Optional[str] = None,
            uuid_str: Optional[str] = None,
    ):
        if uuid_str is not None:
            self.uuid: str = uuid_str
        else:
            self.uuid: str = str(uuid.uuid4())
        self.name: Optional[str] = network_name
        self.ipv4: str = network_ipv4
        self.mask_ipv4: str = network_mask_ipv4
        self.ipv6: Optional[str] = network_ipv6
        self.gateway: Optional[str] = network_gateway
        self.dns: Optional[str] = network_dns
        self.dhcp: Optional[str] = network_dhcp
        self.date_unix: float = time.time()
        self.last_update_unix: float = time.time()

        self.devices = []

        if uuid_str is None:
            self.abs_path = f"{save_path}/{self.uuid}.json"
            self.create_network()
        else:
            self.abs_path = save_path
            self.open_network()

    def create_network(self) -> None:
        if not os.path.exists(self.abs_path):
            logging.debug(self.abs_path)
            with open(self.abs_path, "w+") as f:
                json.dump(self.__dict__, f, indent=4, default=str)
            logging.info(f"{self.name} is created")
        else:
            logging.info(f"{self.name} already exists")

    def open_network(self) -> Union[list, dict]:
        if os.path.exists(self.abs_path):
            with open(self.abs_path, "r") as f:
                return json.load(f)
        else:
            logging.info(f"{self.name} doesn't exist")
            return {}

    def save_network(self) -> None:
        if os.path.exists(self.abs_path):
            self.last_update_unix = time.time()
            with open(self.abs_path, "w") as f:
                json.dump(self.__dict__, f, indent=4, default=str)
            logging.info(f"{self.name} is saved")
        else:
            logging.info(f"{self.name} doesn't exist")

    def add_device(self, device: Device) -> None:
        self.devices.append(device.uuid)
        self.last_update_unix = time.time()
        with open(self.abs_path, "w") as f:
            json.dump(self.__dict__, f, indent=4)
        logging.info(f"{device.name} is added to {self.name}")

    def remove_device(self, device: Device) -> None:
        self.devices.remove(device.uuid)
        self.last_update_unix = time.time()
        device.delete_device()
        with open(self.abs_path, "w") as f:
            json.dump(self.__dict__, f, indent=4)
        logging.info(f"{device.name} is removed from {self.name}")
