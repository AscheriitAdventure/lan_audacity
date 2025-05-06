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
    
    def get_dict(self) -> dict:
        """
        Returns a dictionary representation of the OSAccuracy instance.

        Returns:
            dict: Dictionary representation of the OSAccuracy instance.
        """
        return {
            "name_object": self.name_object,
            "accuracy_int": self.accuracy_int,
            "device": self.device.get_interface().get_dict(),
        }