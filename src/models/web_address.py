from dataclasses import dataclass, field
from typing import Optional
import re


# Classe pour la table WebAddress
@dataclass
class WebAddress:
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
        pattern = re.compile(
            r"^([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4})$|^::([0-9a-fA-F]{1,4}:){0,5}([0-9a-fA-F]{1,4})$|^([0-9a-fA-F]{1,4}:){1,6}:$|^([0-9a-fA-F]{1,4}:){1,7}:$")
        return bool(pattern.match(ipv6))

    @staticmethod
    def validate_cidr(cidr: str) -> bool:
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}$")
        if pattern.match(cidr):
            parts = cidr.split("/")
            if 0 <= int(parts[1]) <= 32:
                return WebAddress.validate_ipv4(parts[0])
        return False

    def get_dict(self) -> dict:
        """Returns a dictionary representation of the instance."""
        return {
            "ipv4": self.ipv4,
            "mask_ipv4": self.mask_ipv4,
            "ipv4_public": self.ipv4_public,
            "cidr": self.cidr,
            "ipv6_local": self.ipv6_local,
            "ipv6_global": self.ipv6_global,
        }

    def check_data(self) -> None:
        if self.ipv4:
            if not WebAddress.validate_ipv4(self.ipv4):
                self.ipv4 = None
        if self.mask_ipv4:
            if not WebAddress.validate_ipv4(self.mask_ipv4):
                self.mask_ipv4 = None
        if self.ipv4_public:
            if not WebAddress.validate_ipv4(self.ipv4_public):
                self.ipv4_public = None
        if self.cidr:
            if not WebAddress.validate_cidr(self.cidr):
                self.cidr = None
        if self.ipv6_local:
            if not WebAddress.validate_ipv6(self.ipv6_local):
                self.ipv6_local = None
        if self.ipv6_global:
            if not WebAddress.validate_ipv6(self.ipv6_global):
                self.ipv6_global = None

