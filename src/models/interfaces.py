from dataclasses import dataclass


@dataclass
class Interfaces:
    name_file: str
    alias: str
    path: str

    @staticmethod
    def from_dict(data: dict) -> "Interfaces":
        """Creates an Interfaces instance from a dictionary."""
        return Interfaces(
            name_file=data.get("name_file" or "uuid", ""),
            alias=data.get("alias" or "name", ""),
            path=data.get("path", ""),
        )

    def get_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        return {
            "name_file": self.name_file,
            "alias": self.alias,
            "path": self.path,
        }
