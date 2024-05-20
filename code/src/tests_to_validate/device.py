import json
import os
import time
import uuid


class Device:
    def __init__(
        self,
        device_ipv4: str,
        mask_ipv4: str,
        save_path: str,
        device_name: str = None,
        device_ipv6: str = None,
        mask_ipv6: str = None,
        device_type: str = None,
        device_os: str = None,
        device_model: str = None,
        device_brand: str = None,
        device_mac: str = None,
        device_gateway: str = None,
        device_dns: str = None,
        device_dhcp: str = None,
        device_snmp: str = None,
        device_ssh: str = None,
        device_logs: str = None,
        device_data: str = None,
    ):
        self.uuid = uuid.uuid4()
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

    def create_device(self):
        if not os.path.exists(self.abs_path):
            with open(self.abs_path, "w") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.name} is created"
        else:
            return f"{self.name} already exists"

    def open_device(self):
        if os.path.exists(self.abs_path):
            with open(self.abs_path, "r") as f:
                return json.load(f)
        else:
            return f"{self.name} doesn't exist"

    def save_device(self):
        if os.path.exists(self.abs_path):
            self.last_update_unix = time.time()
            with open(self.abs_path, "w") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.name} is saved"
        else:
            return f"{self.name} doesn't exist"

    def delete_device(self):
        if os.path.exists(self.abs_path):
            os.remove(self.abs_path)
            return f"{self.name} is deleted"
        else:
            return f"{self.name} doesn't exist"

    def ip_to_cidr(self):
        pass

    def cidr_to_ip(self):
        pass
