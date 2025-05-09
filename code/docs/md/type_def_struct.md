## Structure App

## Structure Projet
* :file_folder: `<Project Name>`
    * :page_facing_up: `lan_audacity.json`
    * :page_facing_up: `logs`
    * :file_folder: `.conf`
        * :page_facing_up: `dlc.json`
        * :page_facing_up: `ssh_storage.json`
    * :file_folder: `.db`
        * :file_folder: `network_infos`
        * :file_folder: `devices_infos`
## Structure Views
### `Project Explorer`
#### Réseaux
* :globe_with_meridians: `<Network Name 0>`
    * :computer: `<Device Name 0>`
    * :computer: `<Device Name X>`
* :globe_with_meridians: `<Network Name X>`
    * :computer: `<Device Name 0>`
    * :computer: `<Device Name X>`
### `Folder Explorer`
#### Dossiers
* :file_folder: `<Project Name>`
    * :page_facing_up: `lan_audacity.json`
    * :page_facing_up: `logs`
    * :file_folder: `.conf`
        * :page_facing_up: `dlc.json`
        * :page_facing_up: `ssh_storage.json`
    * :file_folder: `.db`
        * :file_folder: `network_infos`
        * :file_folder: `devices_infos`

## Structure Données
### Step 1: Open Project
- [ ] input: `Project Name`
- [ ] input: path to save a new project
- [ ] output: `Project Name` is created
    - [ ] output: `lan_audacity.json` is created
    - [ ] output: `logs` is created
    - [ ] output: `.conf` is created
        - [ ] output: `dlc.json` is created
        - [ ] output: `ssh_storage.json` is created
    - [ ] output: `.db` is created
        - [ ] output: `network_infos` is created
        - [ ] output: `devices_infos` is created
- [ ] output: `Project Name` is opened
### Step 2: Create Network
- [ ] input: `Network Name` can be None
- [ ] input: `Network Icon` can be None
- [ ] input: `Network IPv4 & Mask` can't be None

For Advanced Users (optional):
- [ ] input: `Network Ipv6 & Mask` can be None
- [ ] input: `Network Gateway` can be None
- [ ] input: `Network DNS` can be None
- [ ] input: `Network DHCP` can be None

- [ ] output: `Network Name` is created
    - [ ] output: `Network Name` is added to `network_infos`
    - [ ] output: `Network Name` is added to `Project Explorer`
    - [ ] output: `Network Name` is added to `Folder Explorer`
*Generate device*
- [ ] input: `Network IPv4 & Mask` => `CIDR`
- [ ] call: `generate_device`
    - [ ] output: `Device Name` is created
        - [ ] output: `Device Name` is added to `devices_infos`
        - [ ] output: `Device Name` is added to `Project Explorer`
        - [ ] output: `Device Name` is added to `Folder Explorer` 

### Step 3: Create Device
- [ ] select: `Network Name`
- [ ] input: `Device Name` can be None
- [ ] input: `Device Icon` can be None
- [ ] input: `Device IPv4 & Mask` can't be None

For Advanced Users (optional):
- [ ] input: `Device Type` can be None
- [ ] input: `Device OS` can be None
- [ ] input: `Device Model` can be None
- [ ] input: `Device Brand` can be None
- [ ] input: `Device MAC` can be None
- [ ] input: `Device Gateway` can be None
- [ ] input: `Device DNS` can be None
- [ ] input: `Device DHCP` can be None
- [ ] input: `Device SNMP` can be None
- [ ] input: `Device SSH` can be None
- [ ] input: `Device Logs` can be None
- [ ] input: `Device Data` can be None

- [ ] output: `Device Name` is created
    - [ ] output: `Device Name` is added to `devices_infos`
    - [ ] output: `Device Name` is added to `Project Explorer`
    - [ ] output: `Device Name` is added to `Folder Explorer`
### Step 4: Create Link
- [ ] select: `Network Name`
- [ ] select: `Device Name`
- [ ] input: `Link Name` can be None
- [ ] input: `Link Icon` can be None
- [ ] input: `Link IPv4 & Mask` can't be None

For Advanced Users (optional):
- [ ] input: `Link Ipv6 & Mask` can be None
- [ ] input: `Link Gateway` can be None
- [ ] input: `Link DNS` can be None
- [ ] input: `Link DHCP` can be None

- [ ] output: `Link Name` is created
    - [ ] output: `Link Name` is added to `devices_infos`
    - [ ] output: `Link Name` is added to `Project Explorer`
    - [ ] output: `Link Name` is added to `Folder Explorer`

### Step 5: Create Data
- [ ] select: `Device Name`
- [ ] input: `Data Name` can be None
- [ ] input: `Data Icon` can be None
- [ ] input: `Data Type` can be None
- [ ] input: `Data Size` can be None
- [ ] input: `Data Format` can be None
- [ ] input: `Data Path` can be None

- [ ] output: `Data Name` is created
    - [ ] output: `Data Name` is added to `data_storage`
    - [ ] output: `Data Name` is added to `Project Explorer`
    - [ ] output: `Data Name` is added to `Folder Explorer`

### Step 6: Create Logs
- [ ] select: `Device Name`
- [ ] input: `Log Name` can't be None
- [ ] input: `Log Icon` can be None
- [ ] input: `Log Type` can't be None
- [ ] input: `Log Size` can't be None
- [ ] input: `Log Format` can't be None
- [ ] input: `Log Path` can't be None

- [ ] output: `Log Name` is created
    - [ ] output: `Log Name` is added to `logs`
    - [ ] output: `Log Name` is added to `Project Explorer`
    - [ ] output: `Log Name` is added to `Folder Explorer`

## Structure Données
### Structure Version Software
<center><b>1.1.5</b></center>  
Le premier chiffre est la version majeure. (major)   
Le deuxième chiffre est la version mineure. (minor)  
Le troisième chiffre est la version de correctif. (patch)  

### :floppy_disk: `lan_audacity.json`
```json
[
    {
        "software": string<software name>,
        "version": string<software version>,
        "project_name": string<project_name>,
        "date_unix": int<timestamp>,
        "last_update_unix": int<timestamp>,
        "author": null | string<author>, 
        "abs_paths": {
            "conf": {
                "path": ".conf",
                "ls_file": [ string<file>, string<file>, ...]
            },
            "db": {
                "path": ".db",
                "ls_folder": [ string<folder>, string<folder>, ...]
            },
            "logs": "logs"
        },
        "networks": null |{
            "path": "network_infos",
            "obj_ls": [
                {
                    "uuid": uuid<network>,
                    "name": string<network_name>,
                    "path": "network_infos/<uuid>.json",
                    "ls_devices": [uuid<device>, uuid<device>, ...],
                }, ...
            ],
        },
        "links": null |{
            "path": "links_infos",
            "obj_ls": [
                {
                    "uuid": uuid<link>,
                    "name": string<link_name>,
                    "path": "links_infos/<uuid>.json"
                }, ...
            ],
        },
        "devices": null |{
            "path": "devices_infos",
            "obj_ls": [
                {
                    "uuid": uuid<device>,
                    "name": string<device_name>,
                    "path": "devices_infos/<uuid>.json"
                }, ...
            ],
        }
    }
]
```
### :floppy_disk: `.json`

## Python
### :snake: `lan_audacity.py`
```python
import json
import os
import time

class LanAudacity:
    def __init__(self, software_name: str, version_software: str, project_name: str, author: str = None):
        self.software = software_name
        self.version = version_software
        self.char_table = "utf-8"
        self.project_name = project_name
        self.date_unix: float = time.time()
        self.last_update_unix: float = time.time()
        self.author = author
        self.abs_paths = {
            "conf": {
                "path": ".conf",
                "ls_file": []
            },
            "db": {
                "path": ".db",
                "ls_folder": []
            },
            "logs": "logs"
        }
        self.networks = None
        self.links = None
        self.devices = None

    def create_project(self):
        if not os.path.exists(self.project_name):
            os.mkdir(self.project_name)
            with open(f"{self.project_name}/lan_audacity.json", "w") as f:
                json.dump(self.__dict__, f, indent=4)
            os.mkdir(f"{self.project_name}/logs")
            os.mkdir(f"{self.project_name}/.conf")
            os.mkdir(f"{self.project_name}/.db")
            os.mkdir(f"{self.project_name}/.db/network_infos")
            os.mkdir(f"{self.project_name}/.db/devices_infos")
            return f"{self.project_name} is created"
        else:
            return f"{self.project_name} already exists"
    
    def delete_project(self):
        if os.path.exists(self.project_name):
            os.rmdir(self.project_name)
            return f"{self.project_name} is deleted"
        else:
            return f"{self.project_name} doesn't exist"
    
    def add_network(self, network: Network):
        if self.networks is None:
            self.networks = {
                "path": "network_infos",
                "obj_ls": []
            }
        else:
            self.networks["obj_ls"].append({
            "uuid": network.uuid,
            "name": network.name,
            "path": network.abs_path,
            "ls_devices": []
        })
        self.last_update_unix = time.time()
        with open(f"{self.project_name}/lan_audacity.json", "w") as f:
            json.dump(self.__dict__, f, indent=4)
        return f"{network.name} is added to {self.project_name}"
    
    def remove_network(self, network: Network):
        if self.networks is not None:
            self.networks["obj_ls"].remove(network.uuid)
            self.last_update_unix = time.time()
            with open(f"{self.project_name}/lan_audacity.json", "w") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{network.name} is removed from {self.project_name}"
        else:
            return f"{network.name} doesn't exist in {self.project_name}"
    
    def open_project(self):
        if os.path.exists(self.project_name):
            with open(f"{self.project_name}/lan_audacity.json", "r") as f:
                return json.load(f)
        else:
            return f"{self.project_name} doesn't exist"
    
    def save_project(self):
        if os.path.exists(self.project_name):
            self.last_update_unix = time.time()
            with open(f"{self.project_name}/lan_audacity.json", "w") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.project_name} is saved"
        else:
            return f"{self.project_name} doesn't exist"
    
    def save_as_project(self, new_project_name: str):
        if os.path.exists(self.project_name):
            os.rename(self.project_name, new_project_name)
            self.project_name = new_project_name
            with open(f"{self.project_name}/lan_audacity.json", "w") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.project_name} is saved as {new_project_name}"
        else:
            return f"{self.project_name} doesn't exist"
```
### :snake: `network.py`
```python
import json
import os
import time
import uuid

class Network:
    def __init__(self, network_name: str = None, network_ipv4: str, network_ipv6: str = None, network_gateway: str = None, network_dns: str = None, network_dhcp: str = None):
        self.uuid = uuid.uuid4()
        self.name = network_name
        self.ipv4 = network_ipv4
        self.ipv6 = network_ipv6
        self.gateway = network_gateway
        self.dns = network_dns
        self.dhcp = network_dhcp
        self.date_unix: float = time.time()
        self.last_update_unix: float = time.time()
        self.abs_path = f"network_infos/{self.uuid}.json"
        self.devices = []
    
    def create_network(self):
        if not os.path.exists(self.abs_path):
            with open(self.abs_path, "w") as f:
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
    
    def save_as_network(self, new_network_name: str):
        if os.path.exists(self.abs_path):
            os.rename(self.abs_path, f"network_infos/{new_network_name}.json")
            self.name = new_network_name
            self.abs_path = f"network_infos/{new_network_name}.json"
            with open(self.abs_path, "w") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.name} is saved as {new_network_name}"
        else:
            return f"{self.name} doesn't exist"
    
    def ip_to_cidr(self):
        pass

    def cidr_to_ip(self):
        pass

    def generate_device(self):
        pass

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
```
### :snake: `device.py`
```python
import json
import os
import time
import uuid

class Device:
    def __init__(
        self, 
        device_name: str = None, 
        device_ipv4: str, 
        mask_ipv4: str, 
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
        device_data: str = None):
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
        self.abs_path = f"devices_infos/{self.uuid}.json"
    
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
    
    def save_as_device(self, new_device_name: str):
        if os.path.exists(self.abs_path):
            os.rename(self.abs_path, f"devices_infos/{new_device_name}.json")
            self.name = new_device_name
            self.abs_path = f"devices_infos/{new_device_name}.json"
            with open(self.abs_path, "w") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.name} is saved as {new_device_name}"
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
```
