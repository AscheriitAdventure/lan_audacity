from dataclasses import dataclass, field
from typing import Union, List, Any
from uuid import UUID
import logging
import os
import inspect

from .clock_manager import ClockManager
from .interfaces import Interfaces
from .switch_file import SwitchFile
from .software_identity import SoftwareIdentity
from .network import Network
from .file_management import FileManagement


@dataclass
class LanAudacity(FileManagement):
    directory_name: str  # Nom du projet
    directory_path: str  # Chemin absolu du projet
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
                            logging.debug(
                                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {subfolder}")
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
