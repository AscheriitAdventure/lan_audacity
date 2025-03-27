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
            logging.error(
                f"{network.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error loading network - {str(e)}")

        return network

