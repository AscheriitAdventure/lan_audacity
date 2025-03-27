from dataclasses import dataclass

from .device import Device

# Classe pour la table OSAccuracy
@dataclass
class OSAccuracy:
    name_object: str
    accuracy_int: int
    device: Device

    @staticmethod
    def validate_accuracy_int(accuracy_int: int) -> bool:
        return 0 <= accuracy_int <= 100