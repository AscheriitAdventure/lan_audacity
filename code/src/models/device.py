from typing import Union, Optional
import os
import json
import logging
import time
import uuid

class Device:
    def __init__(
            self,
            device_ipv4: str,
            mask_ipv4: str,
            save_path: str,
            device_name: Optional[str] = None,
            device_ipv6: Optional[str] = None,
            mask_ipv6: Optional[str] = None,
            device_type: Optional[str] = None,
            device_os: Optional[str] = None,
            device_model: Optional[str] = None,
            device_brand: Optional[str] = None,
            device_mac: Optional[str] = None,
            device_gateway: Optional[str] = None,
            device_dns: Optional[str] = None,
            device_dhcp: Optional[str] = None,
            device_snmp: Optional[str] = None,
            device_ssh: Optional[str] = None,
            device_logs: Optional[str] = None,
            device_data: Optional[str] = None,
            device_uuid: Optional[str] = None
    ):
        if device_uuid is not None:
            self.uuid: str = device_uuid
        else:
            self.uuid: str = str(uuid.uuid4())
        self.name = device_name
        self.ipv4 = device_ipv4
        self.mask_ipv4 = mask_ipv4
        self.ipv6 = device_ipv6
        self.mask_ipv6 = mask_ipv6
        self.type = device_type
        self.os = device_os
        self.model = device_model
        self.brand = device_brand
        self.mac = device_mac
        self.gateway = device_gateway
        self.dns = device_dns
        self.dhcp = device_dhcp
        self.snmp = device_snmp
        self.ssh = device_ssh
        self.logs = device_logs
        self.data = device_data
        self.date_unix: float = time.time()
        self.last_update_unix: float = time.time()
        self.abs_path = f"{save_path}/{self.uuid}.json"

    def create_device(self) -> None:
        if not os.path.exists(self.abs_path):
            with open(self.abs_path, "w") as f:
                json.dump(self.__dict__, f, indent=4, default=str)
            logging.info(f"{self.name} is created")
        else:
            logging.info(f"{self.name} already exists")

    def open_device(self) -> Optional[dict]:
        if os.path.exists(self.abs_path):
            with open(self.abs_path, "r") as f:
                return json.load(f)
        else:
            logging.info(f"{self.name} doesn't exist")
            return {}

    def save_device(self) -> None:
        if os.path.exists(self.abs_path):
            self.last_update_unix = time.time()
            with open(self.abs_path, "w") as f:
                json.dump(self.__dict__, f, indent=4, default=str)
            logging.info(f"{self.name} is saved")
        else:
            logging.info(f"{self.name} doesn't exist")

    def delete_device(self) -> None:
        if os.path.exists(self.abs_path):
            os.remove(self.abs_path)
            logging.info(f"{self.name} is deleted")
        else:
            logging.info(f"{self.name} doesn't exist")
