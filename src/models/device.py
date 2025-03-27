from dataclasses import dataclass, field
from typing import Optional, Union, List
from uuid import UUID
import uuid
import logging
import os
import inspect

from .web_address import WebAddress
from .clock_manager import ClockManager
from .device_type import DeviceType
from .interfaces import Interfaces
from .switch_file import SwitchFile


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
            logging.error(
                f"{device.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error loading device - {str(e)}")

        return device

