from dataclasses import dataclass, field
import mysql.connector
import os
import logging
import time
import uuid
from typing import Optional

from src.components.functionsExt import ip_to_cidr, cidr_to_ip

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

    def 

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

@dataclass
class WebAddress:
    ipv4: Optional[str] = None
    mask_ipv4: Optional[str] = None
    ipv4_public: Optional[str] = None
    cidr: Optional[str] = None
    ipv6_local: Optional[str] = None
    ipv6_global: Optional[str] = None
    domain_name: Optional[str] = None

    def addressIPv4_values(self) -> None:
        if self.ipv4 and self.mask_ipv4:
            self.cidr = ip_to_cidr(self.ipv4, self.mask_ipv4)
        else:
            self.cidr = None
        
        if self.cidr:
            self.ipv4, self.mask_ipv4 = cidr_to_ip(self.cidr)
        else:
            self.ipv4 = None
            self.mask_ipv4 = None

@dataclass
class ClockManager:
    clock_created: float = field(default_factory=time.time())
    clock_list: Optional[list[float]] = field(default_factory=[])
    type_time:str = field(default_factory="Unix Timestamp Format")

    def addClock(self) -> None:
        self.clock_list.append(time.time())
    
    def clearClock(self) -> None:
        self.clock_list.clear()
    
    def lastClock(self) -> float:
        if not self.clock_list:
            return self.clock_created
        else:
            return self.clock_list[-1]

@dataclass
class Net_Object:
    uuid: str = field(default_factory=str(uuid.uuid4()))
    name: str = field(default_factory="Object Name Undefined")
    web_address: WebAddress = field(default_factory=WebAddress())
    clock_manager: ClockManager = field(default_factory=ClockManager())

