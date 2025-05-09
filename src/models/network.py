from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID
import uuid
import logging
import os
import inspect

from .web_address import WebAddress
from .clock_manager import ClockManager
from .interfaces import Interfaces
from .switch_file import SwitchFile
from .device import Device


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
        self.devices: list = list()
        self.dns_object: Optional[str] = None
        self.path: Optional[str] = None

        self.setPath(ospath)
        self.uuid = UUID(self._getUuidFile())
        if self.path is not None and os.path.exists(self.path):
            try:
                network_data = SwitchFile.json_read(abs_path=self.path)
                if "web_address" in network_data:
                    self.web_address = WebAddress(
                        **network_data["web_address"])
                if "clock_manager" in network_data:
                    self.clock_manager = ClockManager.from_dict(
                        network_data["clock_manager"])
                if "dns_object" in network_data:
                    self.dns_object = network_data["dns_object"]
                if "devices" in network_data:
                    self.devices = [Interfaces.from_dict(
                        device) for device in network_data["devices"]]
            except Exception as e:
                logging.error(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error loading network - {str(e)}")

        # Maintenant faire update_network
        self.update_network()

    def setPath(self, value: str) -> None:
        """Setter for the path attribute."""
        if os.path.isdir(value):
            self.path = os.path.join(value, f"{self.uuid}.json")
        elif os.path.exists(value):
            self.path = value
        else:
            self.path = None

    def get_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        return {
            # Convert UUID to string for JSON serialization
            "uuid": str(self.uuid),
            "name_object": self.name_object,
            # Problem dans la récupération des données
            "web_address": self.web_address.get_dict(),
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
            # Charger d'abord les données existantes
            if os.path.exists(self.path):
                try:
                    existing_data = SwitchFile.json_read(abs_path=self.path)
                    new_data = self.get_dict()

                    # Ne pas écraser les données web_address si elles sont None
                    if all(value is None for value in new_data["web_address"].values()):
                        new_data["web_address"] = existing_data.get(
                            "web_address", new_data["web_address"])

                    # Préserver d'autres valeurs importantes si nécessaire
                    if new_data["dns_object"] is None and "dns_object" in existing_data:
                        new_data["dns_object"] = existing_data["dns_object"]

                    logging.debug(
                        f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {new_data}")
                    SwitchFile.json_write(abs_path=self.path, data=new_data)
                except Exception as e:
                    logging.error(f"Error updating network: {str(e)}")
                    # Écrire quand même les données actuelles
                    logging.debug(
                        f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {self.get_dict()}")
                    SwitchFile.json_write(
                        abs_path=self.path, data=self.get_dict())
            else:
                # Fichier n'existe pas encore
                logging.debug(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {self.get_dict()}")
                SwitchFile.json_write(abs_path=self.path, data=self.get_dict())

    @staticmethod
    def from_dict(data: dict) -> "Network":
        """Creates a Network instance from a dictionary."""
        network = Network(
            name_object=data.get("alias", "Unknown Network"),
            ospath=data.get("path"),
        )

        try:
            # si le chemin fourni est vrai alors chareger les données
            if network.path is not None and os.path.exists(network.path):
                network_data = SwitchFile.json_read(abs_path=network.path)
                network.web_address = WebAddress(**network_data["web_address"])
                network.clock_manager = ClockManager.from_dict(
                    network_data["clock_manager"])
                network.dns_object = network_data["dns_object"]
                # Charger les périphériques (StandBy)
                network.devices = [Interfaces.from_dict(
                    device) for device in network_data["devices"]]

        except Exception as e:
            logging.error(
                f"{network.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error loading network - {str(e)}")

        network.clock_manager.add_clock()
        network.update_network()

        return network

    def get_devices(self) -> List[Device]:
        logging.debug(
            f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {len(self.devices)}")
        ls_d: List[Device] = [Device.from_dict(device.get_dict()) for device in self.devices]
        return ls_d

    def _getUuidFile(self) -> str:
        """Returns the UUID of the network file."""
        if self.path is not None:
            return (os.path.basename(self.path)).split(".")[0]
        else:
            return str(self.uuid)
