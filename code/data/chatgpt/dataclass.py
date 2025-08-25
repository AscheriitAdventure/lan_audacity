from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID
import re

# Classe pour la table OSILayer
@dataclass
class OSILayer:
    osi_layer_id: int
    layer_name: str

# Classe pour la table ClockManager
@dataclass
class ClockManager:
    clock_manager_id: int
    created_at: float
    updated_at: float
    type_time: str

# Classe pour la table UpdateAtList
@dataclass
class UpdateAtList:
    update_at_id: int
    clock_manager_id: int
    update_at: float

# Classe pour la table WebAddress
@dataclass
class WebAddress:
    web_address_id: int
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
    device_type_id: int
    pixmap_path: Optional[str]
    osi_layer: OSILayer
    category_description: Optional[str]
    category_name: str
    sub_devices: List['DeviceType'] = field(default_factory=list)  # Liste de sous-périphériques

# Classe pour la table Device
@dataclass
class Device:
    device_id: int
    uuid: UUID
    name_object: str = "Unknown Device"
    web_address: Optional[WebAddress]
    clock_manager: Optional[ClockManager]
    type_device: Optional[DeviceType]
    vendor: Optional[str]
    mac_address: Optional[str]

# Classe pour la table Network
@dataclass
class Network:
    network_id: int
    uuid: UUID
    name_object: str = "Unknown Network"
    web_address: Optional[WebAddress]
    clock_manager: Optional[ClockManager]
    dns_object: Optional[str]
    devices: List[Device] = field(default_factory=list)

# Classe pour la table OSAccuracy
@dataclass
class OSAccuracy:
    os_accuracy_id: int
    name_object: str
    accuracy_int: int
    device: Device

    @staticmethod
    def validate_accuracy_int(accuracy_int: int) -> bool:
        return 0 <= accuracy_int <= 100

# Classe pour la table PortsObject
@dataclass
class PortsObject:
    port_id: int 
    port_number: int
    protocol: Optional[str]
    port_status: Optional[str]
    port_service: Optional[str]
    port_version: Optional[str]
    device: Device

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
