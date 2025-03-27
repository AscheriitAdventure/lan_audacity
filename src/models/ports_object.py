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

