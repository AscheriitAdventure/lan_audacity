from typing import Optional, List, Union, Any
from dataclasses import dataclass, field
import os
import logging
import inspect
import time
from uuid import UUID
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

# Classe pour la table Network
@dataclass
class Network:
    uuid: UUID
    name_object: str = "Unknown Network"
    web_address: Optional[WebAddress] = None
    clock_manager: ClockManager = field(default_factory=ClockManager)
    dns_object: Optional[str] = None
    devices: List[Device] = field(default_factory=list)

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
        """Returns a dictionary representation of the instance."""
        return {
            "directory_path": self.directory_path,
            "directory_name": self.directory_name,
            "folders": self.folders,
            "files": self.files,
            "clock_manager": self.clock_manager.get_dict(),
            "software_id": self.software_id.get_dict(),
            "authors": self.authors,
            "encode_file": self.encode_file,
            "extensions": self.extensions,
            "networks": self.networks,
            "pixmaps": self.pixmaps,
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
    ######## Native Function Pixmaps Management ########

