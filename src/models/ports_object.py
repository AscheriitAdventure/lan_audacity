from dataclasses import dataclass
from typing import Optional

from .device import Device

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

    def get_dict(self) -> dict:
        """
        Returns a dictionary representation of the PortsObject instance.

        Returns:
            dict: Dictionary representation of the PortsObject instance.
        """
        return {
            "port_number": self.port_number,
            "device": self.device.get_interface().get_dict(),
            "protocol": self.protocol,
            "port_status": self.port_status,
            "port_service": self.port_service,
            "port_version": self.port_version,
        }
