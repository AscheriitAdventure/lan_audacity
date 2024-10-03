from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID

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
    name_object: str
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
    name_object: str
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
