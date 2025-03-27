from dataclasses import dataclass, field
from typing import Optional, List

from .osi_layer import OSILayer

# Classe pour la table DeviceType
@dataclass
class DeviceType:
    category_name: str
    osi_layer: OSILayer
    category_description: Optional[str] = None
    pixmap_path: Optional[str] = None
    sub_devices: List['DeviceType'] = field(default_factory=list)  # Liste de sous-périphériques
