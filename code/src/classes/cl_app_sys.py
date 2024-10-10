from dataclasses import dataclass, field
import os
import logging
import uuid
from typing import Optional

@dataclass
class OsSys:
    name: str
    version: str

    def exec_os(self) -> bool:
        if self.name in ['Windows', 'Linux', 'Darwin']:
            return True
        else:
            logging.error(f"Operating System '{self.name} {self.version}' not supported.")
            return False
        
    def exec_software(self) -> int:
        # search for nmap, docker, and python
        software_list = ['nmap', 'docker', 'python']
        var_i = 0
        if self.name == 'Windows':
            for software in software_list:
                if os.system(f"where {software} >nul 2>nul") == 0:
                    logging.info(f"{software} is installed.")
                else:
                    logging.warning(f"{software} is not installed.")
                    var_i += 1
        elif self.name in ['Linux', 'Darwin']:
            for software in software_list:
                if os.system(f"which {software} > /dev/null 2>&1") == 0:
                    logging.info(f"{software} is installed.")
                else:
                    logging.warning(f"{software} is not installed.")
                    var_i += 1
        else:
            logging.error(f"Operating System '{self.name}' not supported.")
            var_i += 1
        
        return var_i

@dataclass
class MariaDB_Docker:
    root_password: str
    database: str
    user: str
    password: str
    port: int

@dataclass
class MongoDB_Docker:
    user: str
    password: str
    port: int

@dataclass
class User:
    username: str = field(default_factory=os.getlogin())
    password: str = field(default_factory="")

@dataclass
class UserHistory:
    user: User = field(default_factory=User)
    history: list = field(default_factory=[])

    def addFolderPath(self, folder_path: str) -> None:
        # Si il existe dans l'historique
        if folder_path in self.history:
            self.history.remove(folder_path)
            self.history.append(folder_path)
        else:
            self.history.append(folder_path)
    
    def removeFolderPath(self, folder_path: str) -> None:
        self.history.remove(folder_path)
    
    def clearHistory(self) -> None:
        self.history.clear()
    
    def last10Folders(self) -> list:
        return self.history[-10:]


# Classe pour la table WebAddress
@dataclass
class WebAddress:
    ipv4: Optional[str] = None
    mask_ipv4: Optional[str] = None
    ipv4_public: Optional[str] = None
    cidr: Optional[str] = None
    ipv6_local: Optional[str] = None
    ipv6_global: Optional[str] = None


@dataclass
class Net_Object:
    uuid: str = field(default_factory=str(uuid.uuid4()))
    name: str = field(default_factory="Object Name Undefined")
    web_address: WebAddress = field(default_factory=WebAddress())