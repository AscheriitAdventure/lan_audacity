from typing import Optional, List, Union, Any
import typing
from dataclasses import dataclass, field
import os
import logging
import inspect
import time
from uuid import UUID
import uuid
import re
import enum
from dev.project.src.classes.switchFile import SwitchFile


@dataclass
class FileManagement:
    directory_path: str
    directory_name: str
    folders: List[str] = field(default_factory=list)
    files: List[Union[str, tuple]] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> "FileManagement":
        """Creates a FileManagement instance from a dictionary."""
        data.setdefault("directory_path", data.pop("abs_path", ""))
        data.setdefault("directory_name", os.path.basename(
            data["directory_path"]))
        return FileManagement(
            directory_path=data["directory_path"],
            directory_name=data["directory_name"],
            folders=data.get("folders", []),
            files=data.get("files", []),
        )

    def get_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        return {
            "directory_path": self.directory_path,
            "directory_name": self.directory_name,
            "folders": self.folders,
            "files": self.files,
        }

    ######## Native Function Folder Management ########
    def add_folder(self, folder_name: str) -> None:
        """Adds a folder to the folder list if it doesn't already exist."""
        if folder_name not in self.folders:
            self.folders.append(folder_name)

    def generate_folder(self, folder_name: str, absolute_path: str = os.getcwd()) -> None:
        """Creates a folder inside the project directory if it does not already exist."""
        if os.path.basename(absolute_path) != self.directory_name:
            project_path = os.path.join(absolute_path, self.directory_name)
        else:
            project_path = absolute_path
        folder_path = os.path.join(project_path, folder_name)

        if not os.path.isdir(project_path):
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe(
            ).f_code.co_name}: The path {project_path} does not exist or is not a directory.")
            return

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            self.add_folder(folder_name)
        else:
            logging.warning(f"{self.__class__.__name__}::{inspect.currentframe(
            ).f_code.co_name}: The folder {folder_name} already exists in {project_path}.")
            self.add_folder(folder_name)

    ####### Native Function File Management ########
    def add_file(self, file_info: tuple) -> None:
        """Adds a file to the file list if it doesn't already exist."""
        if file_info not in self.files:
            self.files.append(file_info)

    def generate_file(self, file_name: str, file_type: str, abs_path: str = os.getcwd()) -> None:
        """Creates a file inside the specified directory if it does not already exist."""
        project_path = os.path.join(abs_path, self.directory_path)

        if not os.path.isdir(abs_path):
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe(
            ).f_code.co_name}: The path {abs_path} does not exist or is not a directory.")
            return

        if not os.path.exists(project_path):
            os.mkdir(project_path)
        else:
            logging.warning(f"{self.__class__.__name__}::{inspect.currentframe(
            ).f_code.co_name}: The folder {self.directory_path} already exists in {abs_path}.")

        file_path = os.path.join(
            project_path, f"{file_name}.{file_type.lower()}")
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                pass
            self.add_file((file_name, file_type))
        else:
            logging.warning(f"{self.__class__.__name__}::{inspect.currentframe(
            ).f_code.co_name}: The file {file_name} already exists in {project_path}.")
            self.add_file((file_name, file_type))


@dataclass
class ClockManager:
    """Manages a list of timestamps to track time events."""
    clock_created: float = field(default_factory=time.time)
    type_time: str = field(default="Unix Timestamp Format")
    clock_list: List[float] = field(default_factory=list)  # Limit to 20 clocks

    @staticmethod
    def from_dict(data: dict) -> "ClockManager":
        """Creates a ClockManager instance from a dictionary."""
        return ClockManager(
            clock_created=data.get("clock_created", time.time()),
            type_time=data.get("type_time", "Unix Timestamp Format"),
            clock_list=data.get("clock_list", []),
        )

    def get_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        return {
            "clock_created": self.clock_created,
            "type_time": self.type_time,
            "clock_list": self.clock_list,
        }

    def add_clock(self) -> None:
        """Adds the current time to the clock list, ensuring a maximum of 20 entries."""
        if len(self.clock_list) >= 20:
            self.clock_list.pop(0)  # Maintain the latest 20 entries
        self.clock_list.append(time.time())

    def get_last_clock(self) -> float:
        """Returns the last recorded time or the creation time if the list is empty."""
        return self.clock_list[-1] if self.clock_list else self.clock_created

    def get_diff_clock(self) -> float:
        """Returns the time difference between the last two recorded timestamps."""
        if len(self.clock_list) < 2:
            return 0.0
        return self.clock_list[-1] - self.clock_list[-2]


@dataclass
class SoftwareIdentity:
    name: str = "Lan Audacity"
    version: str = "1.0.4"

    @staticmethod
    def from_dict(data: dict) -> "SoftwareIdentity":
        """Creates a SoftwareIdentity instance from a dictionary."""
        return SoftwareIdentity(
            name=data.get("name", "Lan Audacity"),
            version=data.get("version", "1.0.4"),
        )

    def get_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        return {
            "name": self.name,
            "version": self.version,
        }


@dataclass
class Interfaces:
    name_file: str
    alias: str
    path: str

    @staticmethod
    def from_dict(data: dict) -> "Interfaces":
        """Creates an Interfaces instance from a dictionary."""
        return Interfaces(
            name_file=data.get("name_file" or "uuid", ""),
            alias=data.get("alias" or "name", ""),
            path=data.get("path", ""),
        )
    
    def get_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        return {
            "name_file": self.name_file,
            "alias": self.alias,
            "path": self.path,
        }

# Classe pour la table OSILayer
class OSILayer(enum.Enum):
    APPLICATION = 7
    PRESENTATION = 6
    SESSION = 5
    TRANSPORT = 4
    NETWORK = 3
    DATA_LINK = 2
    PHYSICAL = 1

# Classe pour la table WebAddress
@dataclass
class WebAddress:
    ipv4: Optional[str] = None
    mask_ipv4: Optional[str] = None
    ipv4_public: Optional[str] = None
    cidr: Optional[str] = None
    ipv6_local: Optional[str] = None
    ipv6_global: Optional[str] = None

    @staticmethod
    def validate_ipv4(ipv4: str) -> bool:
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if pattern.match(ipv4):
            parts = ipv4.split(".")
            for part in parts:
                if not 0 <= int(part) <= 255:
                    return False
            return True
        return False
    
    @staticmethod
    def validate_ipv6(ipv6: str) -> bool:
        pattern = re.compile(r"^([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4})$|^::([0-9a-fA-F]{1,4}:){0,5}([0-9a-fA-F]{1,4})$|^([0-9a-fA-F]{1,4}:){1,6}:$|^([0-9a-fA-F]{1,4}:){1,7}:$")
        return bool(pattern.match(ipv6))
    
    @staticmethod
    def validate_cidr(cidr: str) -> bool:
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}$")
        if pattern.match(cidr):
            parts = cidr.split("/")
            if 0 <= int(parts[1]) <= 32:
                return WebAddress.validate_ipv4(parts[0])
        return False

    def get_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        return {
            "ipv4": self.ipv4,
            "mask_ipv4": self.mask_ipv4,
            "ipv4_public": self.ipv4_public,
            "cidr": self.cidr,
            "ipv6_local": self.ipv6_local,
            "ipv6_global": self.ipv6_global,
        }
    
    def check_data(self) -> None:
        if self.ipv4:
            if not WebAddress.validate_ipv4(self.ipv4):
                self.ipv4 = None
        if self.mask_ipv4:
            if not WebAddress.validate_ipv4(self.mask_ipv4):
                self.mask_ipv4 = None
        if self.ipv4_public:
            if not WebAddress.validate_ipv4(self.ipv4_public):
                self.ipv4_public = None
        if self.cidr:
            if not WebAddress.validate_cidr(self.cidr):
                self.cidr = None
        if self.ipv6_local:
            if not WebAddress.validate_ipv6(self.ipv6_local):
                self.ipv6_local = None
        if self.ipv6_global:
            if not WebAddress.validate_ipv6(self.ipv6_global):
                self.ipv6_global = None


# Classe pour la table DeviceType
@dataclass
class DeviceType:
    category_name: str
    osi_layer: OSILayer
    category_description: Optional[str] = None
    pixmap_path: Optional[str] = None
    sub_devices: List['DeviceType'] = field(default_factory=list)  # Liste de sous-périphériques

# Classe pour la table Device
@dataclass
class Device:
    uuid: UUID
    name_object: str = "Unknown Device"
    web_address: Optional[WebAddress] = None
    clock_manager: ClockManager = field(default_factory=ClockManager)
    type_device: Optional[DeviceType] = None
    vendor: Optional[str] = None
    mac_address: Optional[str] = None
    path: Optional[str] = None

    def __init__(self, name_object: str = "Unknown Device", ospath: Optional[str] = None):
        """
        Initialize a Device instance.
        
        Args:
            name_object (str): Name of the device object. Defaults to "Unknown Device".
            ospath (Optional[str]): Path where the device file should be stored. If provided,
                                  creates a JSON file at this location.
        """
        self.name_object = name_object
        self.uuid = uuid.uuid4()
        self.web_address = WebAddress()
        self.clock_manager = ClockManager()
        self.type_device = None
        self.vendor = None
        self.mac_address = None
        
        if ospath is not None:
            self.path = os.path.join(ospath, f"{self.uuid}.json")
            self.update_device()
        else:
            self.path = None

    def get_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        return {
            "uuid": self.uuid,
            "name_object": self.name_object,
            "web_address": self.web_address.get_dict(),
            "clock_manager": self.clock_manager.get_dict(),
            "type_device": self.type_device,
            "vendor": self.vendor,
            "mac_address": self.mac_address,
        }

    def get_interface(self) -> Interfaces:
        """Returns an Interfaces instance representing this device."""
        return Interfaces(
            name_file=str(self.uuid),  # Convert UUID to string
            alias=self.name_object,
            path=self.path
        )
    
    def update_device(self) -> None:
        """Updates the device file with the current data."""
        if self.path is not None:
            SwitchFile.json_write(abs_path=self.path, data=self.get_dict())

    @staticmethod
    def from_dict(data: dict) -> "Device":
        """Creates a Device instance from a dictionary."""
        device = Device(
            name_object=data.get("alias", "Unknown Device"),
            ospath=data.get("path"),
        )
        device.uuid = UUID(data["name_file"])

        try:
            # si le chemin fourni est vrai alors chareger les données
            if device.path is not None and os.path.exists(device.path):
                device_data = SwitchFile.json_read(abs_path=device.path)
                device.web_address = WebAddress(**device_data["web_address"])
                device.clock_manager = ClockManager.from_dict(device_data["clock_manager"])
                device.type_device = device_data["type_device"]
                device.vendor = device_data["vendor"]
                device.mac_address = device_data["mac_address"]
            
        except Exception as e:
            logging.error(f"{device.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error loading device - {str(e)}")

        return device

# Classe pour la table Network
@dataclass
class Network:
    uuid: UUID
    name_object: str = "Unknown Network"
    web_address: Optional[WebAddress] = None
    clock_manager: ClockManager = field(default_factory=ClockManager)
    dns_object: Optional[str] = None
    devices: List[Interfaces] = field(default_factory=list)
    path: Optional[str] = None

    def __init__(self, name_object: str = "Unknown Network", ospath: Optional[str] = None):
        """
        Initialize a Network instance.
        
        Args:
            name_object (str): Name of the network object. Defaults to "Unknown Network".
            ospath (Optional[str]): Path where the network file should be stored. If provided,
                                  creates a JSON file at this location.
        """
        self.name_object = name_object
        self.uuid = uuid.uuid4()
        self.web_address = WebAddress()
        self.clock_manager = ClockManager()
        self.devices = []
        self.dns_object = None
        
        if ospath is not None:
            self.path = os.path.join(ospath, f"{self.uuid}.json")
            self.update_network()
        else:
            self.path = None

    def get_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        return {
            "uuid": str(self.uuid),  # Convert UUID to string for JSON serialization
            "name_object": self.name_object,
            "web_address": self.web_address.get_dict() if self.web_address else None,
            "clock_manager": self.clock_manager.get_dict(),
            "dns_object": self.dns_object,
            "devices": [device.get_dict() for device in self.devices],
            "path": self.path,
        }
    
    def get_interface(self) -> Interfaces:
        """Returns an Interfaces instance representing this network."""
        return Interfaces(
            name_file=str(self.uuid),  # Convert UUID to string
            alias=self.name_object,
            path=self.path
        )
    
    def update_network(self) -> None:
        """Updates the network file with the current data."""
        if self.path is not None:
            SwitchFile.json_write(abs_path=self.path, data=self.get_dict())
    
    @staticmethod
    def from_dict(data: dict) -> "Network":
        """Creates a Network instance from a dictionary."""
        network = Network(
            name_object=data.get("alias", "Unknown Network"),
            ospath=data.get("path"),
        )
        network.uuid = UUID(data["name_file"])

        try:
            # si le chemin fourni est vrai alors chareger les données
            if network.path is not None and os.path.exists(network.path):
                network_data = SwitchFile.json_read(abs_path=network.path)
                network.web_address = WebAddress(**network_data["web_address"])
                network.clock_manager = ClockManager.from_dict(network_data["clock_manager"])
                network.dns_object = network_data["dns_object"]
                # Charger les périphériques (StandBy)
            
        except Exception as e:
            logging.error(f"{network.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error loading network - {str(e)}")

        return network

# Classe pour la table OSAccuracy
@dataclass
class OSAccuracy:
    name_object: str
    accuracy_int: int
    device: Device

    @staticmethod
    def validate_accuracy_int(accuracy_int: int) -> bool:
        return 0 <= accuracy_int <= 100
    
# Classe pour la table PortsObject
@dataclass
class PortsObject:
    port_number: int
    device: Device
    protocol: Optional[str] = None
    port_status: Optional[str] = None
    port_service: Optional[str] = None
    port_version: Optional[str] = None

    @staticmethod
    def validate_port_number(port_number: int) -> bool:
        """
        Validate if the port number is within the valid range for TCP/UDP ports.
        
        Args:
            port_number (int): The port number to validate.
        
        Returns:
            bool: True if the port number is valid, False otherwise.
        """
        return 0 <= port_number <= 65535


@dataclass
class LanAudacity(FileManagement):
    directory_name: str     # Nom du projet
    directory_path: str     # Chemin absolu du projet
    folders: List[str] = field(default_factory=list)
    files: List[Union[str, tuple]] = field(default_factory=list)

    clock_manager: ClockManager = field(default_factory=ClockManager)
    software_id: SoftwareIdentity = field(default_factory=SoftwareIdentity)
    authors: List[Any] = field(default_factory=list)  # Liste des auteurs
    encode_file: str = "UTF-8"  # Type de caractère du fichier lu

    # Liste des extensions liées au projet
    extensions: List[Any] = field(default_factory=list)
    # Liste des réseaux liés au projet
    networks: List[Union[Interfaces, dict]] = field(default_factory=list)
    # Liste des cartes générées par le projet
    pixmaps: List[Any] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> "LanAudacity":
        """Creates a LanAudacity instance from a dictionary."""
        data.setdefault("directory_path", data.pop("abs_path", ""))
        data.setdefault("directory_name", os.path.basename(
            data["directory_path"]))
        if co := data.get("clock_manager"):
            co2 = ClockManager().from_dict(co)
        else:
            co2 = ClockManager()
        if si := data.get("software_id"):
            si2 = SoftwareIdentity().from_dict(si)
        else:
            si2 = SoftwareIdentity()
        return LanAudacity(
            directory_path=data["directory_path"],
            directory_name=data["directory_name"],
            folders=data.get("folders", []),
            files=data.get("files", []),
            clock_manager=co2,
            software_id=si2,
            authors=data.get("authors", []),
            encode_file=data.get("encode_file", "UTF-8"),
            extensions=data.get("extensions", []),
            networks=data.get("networks", []),
            pixmaps=data.get("pixmaps", []),
        )

    def get_dict(self) -> dict:
        """
        Returns an optimized dictionary representation of the LanAudacity instance.
    
        Returns:
            dict: A dictionary containing all serializable instance data.
        
        Note:
            - Utilise dict comprehension pour de meilleures performances
            - Traite efficacement la sérialisation des objets networks
            - Hérite des attributs de FileManagement via super()
        """
        # Récupérer les attributs de base de FileManagement
        base_dict = super().get_dict()
    
        # Préparer la liste des réseaux avec une seule compréhension de liste
        networks_data = [
            obj.get_dict() if isinstance(obj, Interfaces) else obj 
            for obj in self.networks
        ]
    
        # Combiner les données de base avec les attributs spécifiques
        return {
            **base_dict,
            "clock_manager": self.clock_manager.get_dict(),
            "software_id": self.software_id.get_dict(),
            "authors": self.authors,
            "encode_file": self.encode_file,
            "extensions": self.extensions,
            "networks": networks_data,
            "pixmaps": self.pixmaps
        }

    ######## Class Methods ########
    def generate_environment(self, debug: bool = False) -> bool:
        """
        Generate the project environment.

        Args:
            debug (bool, optional): Enable debug logging. Defaults to False.

        Returns:
            bool: True if environment generation was successful, False otherwise.
        """
        try:
            # Create project directory
            if os.path.exists(self.directory_path):
                logging.info(f"{self.__class__.__name__}::{inspect.currentframe(
                ).f_code.co_name}: The project {self.directory_name} already exists.")
            else:
                os.mkdir(self.directory_path)
                logging.info(f"{self.__class__.__name__}::{inspect.currentframe(
                ).f_code.co_name}: The project {self.directory_name} has been created.")

            # Generate the "lan_audacity.json" configuration file
            self.generate_file("lan_audacity", "json", self.directory_path)
            self.update_lan_audacity()

            # Define the folder and file tree structure
            data_tree = [
                {
                    "name": "conf"
                },
                {
                    "name": "db",
                    "folders": ["interfaces", "desktop"]
                },
                {
                    "name": "logs",
                    "files": [("lan_audacity", "log")]
                },
                {
                    "name": "pixmap"
                }
            ]

            # Create folders and files
            for item in data_tree:
                folder_path = os.path.join(self.directory_path, item["name"])

                if debug:
                    logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {folder_path}")

                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                    self.add_folder(item["name"])
                    if debug:
                        logging.info(f"{self.__class__.__name__}::{inspect.currentframe(
                        ).f_code.co_name}: The folder {item['name']} has been created.")

                file_manager = FileManagement(
                    directory_path=folder_path, directory_name=item["name"])

                # Create subfolders
                if "folders" in item and item["folders"]:
                    for subfolder in item["folders"]:
                        if debug:
                            logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {subfolder}")
                        file_manager.generate_folder(subfolder, folder_path)

                # Create files
                if "files" in item and item["files"]:
                    for file in item["files"]:
                        file_manager.generate_file(
                            file[0], file[1], folder_path)

            return True

        except Exception as e:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe(
            ).f_code.co_name}: Error generating environment - {str(e)}")
            return False

    def update_lan_audacity(self) -> None:
        """Update the project file "lan_audacity.json"."""
        os_path = os.path.join(self.directory_path, "lan_audacity.json")
        logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {os_path}")
        data = self.get_dict()
        SwitchFile.json_write(abs_path=os_path, data=data)

    ######## Native Function Format File Management ########
    def set_file_encoding(self, encoding: str) -> None:
        self.encode_file = encoding

    ######## Native Function Authors Management ########
    def add_author(self, author: Any) -> None:
        """Adds an author to the list of authors."""
        if author not in self.authors:
            self.authors.append(author)

    def remove_author(self, author: Any) -> None:
        """Removes an author from the list of authors."""
        if author in self.authors:
            self.authors.remove(author)

    ######## Native Function Extensions Management ########
    def add_extension(self, extension: Any) -> None:
        """Adds an extension to the list of extensions."""
        if extension not in self.extensions:
            self.extensions.append(extension)

    def remove_extension(self, extension: Any) -> None:
        """Removes an extension from the list of extensions."""
        if extension in self.extensions:
            self.extensions.remove(extension)

    ######## Native Function Networks Management ########
    def add_network(self, network: Union[Interfaces, dict]) -> None:
        """Adds a network to the list of networks."""
        if network not in self.networks:
            self.networks.append(network)

    def remove_network(self, network: Union[Interfaces, dict]) -> None:
        """Removes a network from the list of networks."""
        if network in self.networks:
            self.networks.remove(network)
    
    def get_network(self, network_data: Union[UUID, str]) -> Union[Network, None]:
        """Returns the network object with the specified UUID."""
        for network in self.networks:
            if isinstance(network, Interfaces):
                if network_data == UUID(network.name_file):
                    return Network(name_object=network.alias, ospath=network.path)
                elif network_data == network.alias:
                    return Network(name_object=network.alias, ospath=network.path)
                elif network_data == network.name_file:
                    return Network(name_object=network.alias, ospath=network.path)
                
            elif isinstance(network, dict):
                if network_data == UUID(network["uuid"]):
                    return Network.from_dict(network)
                elif network_data == network["alias"]:
                    return Network.from_dict(network)
                elif network_data == network["name_file"]:
                    return Network.from_dict(network)
                            
        return None

    ######## Native Function Pixmaps Management ########

