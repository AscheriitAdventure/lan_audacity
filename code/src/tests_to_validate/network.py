import json
import os
import time
import uuid
from device import Device


class Network:
    def __init__(
        self,
        network_ipv4: str,
        network_mask_ipv4: str,
        save_path: str,
        network_name: str = None,
        network_ipv6: str = None,
        network_gateway: str = None,
        network_dns: str = None,
        network_dhcp: str = None,
        uuid: str = None,
    ):
        if uuid:
            self.uuid: str = uuid
        else:
            self.uuid: str = str(uuid.uuid4())
        self.name: str = network_name
        self.ipv4: str = network_ipv4
        self.mask_ipv4: str = network_mask_ipv4
        self.ipv6: str = network_ipv6
        self.gateway: str = network_gateway
        self.dns: str = network_dns
        self.dhcp: str = network_dhcp
        self.date_unix: float = time.time()
        self.last_update_unix: float = time.time()

        self.abs_path = f"{save_path}/{self.uuid}.json"
        self.devices = []

        self.create_network()

    def create_network(self):
        if not os.path.exists(self.abs_path):
            with open(self.abs_path, "w+") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.name} is created"
        else:
            return f"{self.name} already exists"

    def open_network(self):
        if os.path.exists(self.abs_path):
            with open(self.abs_path, "r") as f:
                return json.load(f)
        else:
            return f"{self.name} doesn't exist"

    def save_network(self):
        if os.path.exists(self.abs_path):
            self.last_update_unix = time.time()
            with open(self.abs_path, "w") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.name} is saved"
        else:
            return f"{self.name} doesn't exist"

    def add_device(self, device: Device):
        self.devices.append(device.uuid)
        self.last_update_unix = time.time()
        with open(self.abs_path, "w") as f:
            json.dump(self.__dict__, f, indent=4)
        return f"{device.name} is added to {self.name}"

    def remove_device(self, device: Device):
        self.devices.remove(device.uuid)
        self.last_update_unix = time.time()
        device.delete_device()
        with open(self.abs_path, "w") as f:
            json.dump(self.__dict__, f, indent=4)
        return f"{device.name} is removed from {self.name}"
