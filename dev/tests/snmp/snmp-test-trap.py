from pysnmp.hlapi.v3arch.asyncio import *
import logging
from enum import Enum
from typing import List, Any


class PysnmpForm:
    def __init__(self, port: int = 161, community: str = "public"):
        self.__port = port
        self.__community = community
        self.publicData: dict = {}
        self.privateData: dict = {}

    @property
    def portListened(self) -> int:
        return self.__port

    @property
    def communityPwd(self) -> str:
        return self.__community

    @portListened.setter
    def portListened(self, var: int) -> None:
        if 0 <= var <= 65535:
            self.__port = var
        else:
            logging.error("Port number must be between 0 and 65535")

    @communityPwd.setter
    def communityPwd(self, var: str) -> None:
        if var:
            self.__community = var
        else:
            logging.error("Community password must not be empty")


class Pysnmp:
    class Versions(Enum):
        SNMPv1 = 0
        SNMPv2c = 1
        SNMPv3 = 3

    class IPForm(Enum):
        IPV4 = 0
        IPV6 = 1

    def __init__(self, ip_address: str, port: int = 161, community: str = "public", version: Versions = Versions.SNMPv2c, ip_format: IPForm = IPForm.IPV4):
        self.__ip_address: str = ip_address
        self.__port: int = port
        self.__community: str = community
        self.__version = version
        self.__ip_format = ip_format
    
    @property
    def portListened(self) -> int:
        return self.__port

    @property
    def communityPwd(self) -> str:
        return self.__community

    @portListened.setter
    def portListened(self, var: int) -> None:
        if 0 <= var <= 65535:
            self.__port = var
        else:
            logging.error("Port number must be between 0 and 65535")

    @communityPwd.setter
    def communityPwd(self, var: str) -> None:
        if var:
            self.__community = var
        else:
            logging.error("Community password must not be empty")
    
    def setPort(self, port: int) -> None:
        self.portListened = port
    
    def setCommunity(self, community: str) -> None:
        self.communityPwd = community
    
    def setVersion(self, version: Versions) -> None:
        self.__version = version
    
    def setIPFormat(self, ip_format: IPForm) -> None:
        self.__ip_format = ip_format
    
    def readDeviceUptime(self) -> int:
        oid_sysUpTimeInstance = "1.3.6.1.2.1.1.3.0"
        sysUpTime: int = 0

        return sysUpTime
    
    def scanInterfaces(self) -> List[dict]:
        interfaceList: List[dict] = []

        return interfaceList
    
    def getCustomOID(self, oid: str) -> Any:
        customOID: Any = None

        return customOID
    
    def getWalkOID(self, oid: str) -> Any:
        walkOID: Any = None

        return walkOID

    

