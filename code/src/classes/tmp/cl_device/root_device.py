from src.classes.tmp import *
from typing import *
from enum import Enum, auto
import uuid
import logging
import inspect
import ipaddress


class RootDevice:
    class ConnexionStatus(Enum):
        CONNECTED = auto()
        DISCONNECTED = auto()
        NOT_SETTED = auto()
        UNREACHABLE = auto()
    
    def __init__(
            self, 
            ip_address:str, 
            mask_ip_address: Optional[str] = None,
            name: str = "Central Unit ",
            uuid_str: Optional[str] = None
            ):
        self.__uuid: str = uuid_str if uuid_str is not None else str(uuid.uuid4())

        self.__connexion_status: RootDevice.ConnexionStatus = self.ConnexionStatus.NOT_SETTED
        self.__name: str = name
        self.__web_address: WebAddress = WebAddress()
        self.__clock_manager: ClockManager = ClockManager()

        a = ipaddress.ip_address(ip_address)
        if a.version == 4:
            self.__web_address.ipv4 = ip_address
            self.__web_address.mask_ipv4 = mask_ip_address
            self.__web_address.cidr = ip_address + "/" + str(ipaddress.ip_network(ip_address, strict=False).prefixlen)
        elif a.version == 6:
            self.__web_address.ipv6_local = ip_address
        
    @property
    def uuidStr(self) -> str:
        return self.__uuid
    
    @uuidStr.setter
    def uuidStr(self, var: str, check: Optional[bool] = False) -> Optional[bool]:
        try:
            uuid_obj = uuid.UUID(var)
            self.__uuid = str(uuid_obj)
            
            return True if check else None
         
        except ValueError as e:
            a = f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: "
            logging.error(a+f"value error: {e}")

            return False if check else None
    
    @property
    def connexionStatus(self):
        return self.__connexion_status
    
    @connexionStatus.setter
    def connexionStatus(self, var: ConnexionStatus, check: Optional[bool]) -> Optional[bool]:
        try:
            if not isinstance(var, self.ConnexionStatus):
                raise ValueError(f"Variable must be of type ConnexionStatus, got {type(var)}")
        
            self.__connexion_status = var
            return True if check else None
        
        except ValueError as e:
            a = f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: "
            logging.error(a+f"value error: {e}")

            return False if check else None

    @property
    def nameObj(self) -> str:
        return self.__name

    @nameObj.setter
    def nameObj(self, var: str, check: Optional[bool] = False) -> Optional[bool]:
        try:
            if not isinstance(var, str):
                raise ValueError(f"Variable must be of type str, got {type(var)}")
        
            self.__name = var
            return True if check else None
        
        except ValueError as e:
            a = f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: "
            logging.error(a+f"value error: {e}")

            return False if check else None
    
    @property
    def webAddressObj(self) -> WebAddress:
        return self.__web_address
    
    @webAddressObj.setter
    def webAddressObj(self, var: WebAddress, check: Optional[bool] = False) -> Optional[bool]:
        try:
            if not isinstance(var, WebAddress):
                raise ValueError(f"Variable must be of type WebAddress, got {type(var)}")
        
            self.__web_address = var
            return True if check else None
        
        except ValueError as e:
            a = f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: "
            logging.error(a+f"value error: {e}")

            return False if check else None
    
    @property
    def clockManagerObj(self) -> ClockManager:
        return self.__clock_manager
    
    @clockManagerObj.setter
    def clockManagerObj(self, var: ClockManager, check: Optional[bool] = False) -> Optional[bool]:
        try:
            if not isinstance(var, ClockManager):
                raise ValueError(f"Variable must be of type ClockManager, got {type(var)}")
        
            self.__clock_manager = var
            return True if check else None
        
        except ValueError as e:
            a = f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: "
            logging.error(a+f"value error: {e}")

            return False if check else None

    def getKeys(self) -> List[str]:
        keys = []
        for key in self.__dict__:
            if not key.startswith("_"):
                keys.append(key)
        return keys
    
    def getDict(self) -> Dict[str, Any]:
        return {key: getattr(self, key) for key in self.getKeys()}
