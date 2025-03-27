from dataclasses import dataclass

@dataclass
class SoftwareIdentity:
    name: str = "Lan Audacity"
    version: str = "1.0.4"

    @staticmethod
    def from_dict(data: dict) -> "SoftwareIdentity":
        """Creates a SoftwareIdentity instance from a dictionary."""
        return SoftwareIdentity(
            name=data.get("name", "Lan Audacity"),
            version=data.get("version", "1.0.4"),
        )

    def get_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        return {
            "name": self.name,
            "version": self.version,
        }