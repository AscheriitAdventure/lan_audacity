from typing import Any, Optional
import platform
import json
import logging
import os
import subprocess
import uuid
import nmap

from src.classes.clockManager import ClockManager
from src.classes.cl_deviceType import DeviceType
from src.components.nmap_forms import NmapForm
from src.components.pysnmp_forms import PysnmpForm
from src.components.eunum_lab import isConnected

VAR_STR_DEFAULT: str = "Unknown"

class Device:
    def __init__(
            self,
            device_ipv4: str,
            mask_ipv4: str,
            save_path: str,
            device_name: str = VAR_STR_DEFAULT,
            uuid_str: Optional[str] = None
            ) -> None:
        self.__uuid: str | None = uuid_str
        
        self.__is_connected: isConnected = isConnected.NOT_SETTED
        self.__clockManager = ClockManager()    # Gestionnaire de synchronisation
        self.__name = VAR_STR_DEFAULT
        self.__ipv4 = device_ipv4               # Adresse ipv4 de L'appareil
        self.__mask_ipv4 = mask_ipv4
        self.__ipv6: Optional[str] = None
        self.__type: DeviceType = DeviceType("general")
        self.__vendor: str = VAR_STR_DEFAULT     # Fournisseur
        self.__mac: Optional[str] = None        # Mac Adresse
        self.__snmp: PysnmpForm = PysnmpForm()
        self.__nmap_infos: NmapForm = NmapForm(self.ipv4)

        self.__links = []

        self.nameObj = device_name              # Nom de l'appareil
        if uuid_str is None:
            self.setUUIDObj(uuid_str)
            self.absPath = os.path.join(save_path, f"{self.uuid}.json")
            self.create_file()
        else:
            self.absPath = save_path
            self.open_file()


    @property
    def nameObj(self) -> str:
        return self.__name

    @nameObj.setter
    def nameObj(self, new_name: str):
        if new_name != "" and new_name is not None:
            self.__name = new_name

    @property
    def pysnmpInfos(self) -> PysnmpForm:
        return self.__snmp

    @property
    def nmapInfos(self) -> NmapForm:
        return self.__nmap_infos

    @property
    def macAddress(self) -> str | None:
        return self.__mac
    
    @macAddress.setter
    def macAddress(self, new_mac: str):
        self.__mac = new_mac

    @property
    def ipv6(self) -> str | None:
        return self.__ipv6
    
    @ipv6.setter
    def ipv6(self, new_ipv6: str):
        self.__ipv6 = new_ipv6
    
    @property
    def type(self) -> DeviceType:
        return self.__type
    
    @type.setter
    def type(self, new_type: dict | DeviceType):
        self.__type = new_type

    @property
    def isConnected(self):
        return self.__is_connected

    @isConnected.setter
    def isConnected(self, var: isConnected):
        self.__is_connected = var
    
    @property
    def ipv4(self) -> str:
        return self.__ipv4

    @property
    def uuid(self) -> str:
        return self.__uuid

    @uuid.setter
    def uuid(self, new_uuid: str):
        if new_uuid != "" and new_uuid is not None:
            self.__uuid = new_uuid

    def setUUIDObj(self, new_uuid: Optional[str] = None):
        if new_uuid == "" or new_uuid is None:
            self.uuid = str(uuid.uuid4())
        else:
            self.uuid = new_uuid

    @property
    def maskIpv4(self) -> str:
        return self.__mask_ipv4

    @property
    def clockManager(self) -> ClockManager:
        return self.__clockManager

    @clockManager.setter
    def clockManager(self, clock: ClockManager) -> None:
        self.__clockManager = clock

    @property
    def absPath(self):
        return self.__abs_path

    @absPath.setter
    def absPath(self, new_path: str) -> None:
        try:
            new_path = os.path.abspath(new_path)
            if not os.path.exists(new_path):
                raise ValueError("The path does not exist.")
        except (ValueError, FileNotFoundError) as e:
            logging.error(f"Invalid path: {new_path}. Error: {e}")
        self.__abs_path = new_path

    @property
    def linksList(self) -> list:
        return self.__links
    
    def create_file(self) -> None:
        if not os.path.exists(self.absPath):
            with open(self.absPath, "w+") as f:
                json.dump(self.dict_return(), f, indent=4, default=str)
            logging.info(f"{self.uuid} file is created")
        else:
            logging.info(f"{self.uuid} file already exists")

    def open_file(self) -> Any:
        if os.path.exists(self.absPath):
            with open(self.absPath, "r") as f:
                return json.load(f)
        else:
            logging.info(f"{self.nameObj} doesn't exist")
            return {}

    def save_file(self) -> None:
        if os.path.exists(self.absPath):
            self.clockManager.add_clock()
            with open(self.absPath, "w") as f:
                json.dump(self.dict_return(), f, indent=4, default=str)
            logging.info(f"{self.nameObj} is saved")
        else:
            logging.info(f"{self.nameObj} doesn't exist")

    def dict_return(self) -> dict:
        return {
            "uuid": self.uuid,
            "name": self.nameObj,
            "abs_path": self.absPath,
            "clock_manager": self.clockManager.dict_return(),
            "ipv4": self.ipv4,
            "mask_ipv4": self.maskIpv4,
            "ipv6": self.ipv6,
            "type": self.type.jsonData(),
            "vendor": self.vendor,
            "mac": self.macAddress,
            "snmp": self.pysnmpInfos.jsonData(),
            "nmap": self.nmapInfos.jsonData(),
            "links_list": self.linksList,
        }

    def keys(self) -> list:
        return list(self.dict_return().keys())
    
    def set_isConnected(self) -> None:
        # Vérifie l'OS et utilise le bon paramètre pour le ping
        param = "-n" if platform.system().lower() == "windows" else "-c"
        try:
            result = subprocess.run(
                ["ping", param, "4", self.ipv4],  # Utilise le paramètre en fonction de l'OS
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
            if result.returncode == 0:
                self.isConnected = isConnected.CONNECTED
                logging.info("La machine est connectée.")
            else:
                self.isConnected = isConnected.DISCONNECTED
                logging.warning("La machine n'est pas connectée.")
        except subprocess.TimeoutExpired:
            self.isConnected = isConnected.DISCONNECTED
            logging.warning("Timeout lors de la tentative de connexion à la machine.")
    
    def update_auto(self):
        self.set_nmap_macVendor()
        self.set_nmap_hostname()
        self.set_isConnected()
        self.save_file()

    def set_deviceName(self, new_name: Optional[str]) -> None:
        if new_name == "" or new_name is None:
            self.__name = f"Device_{self.ipv4}"
        else:
            self.__name = new_name

    def set_nmap_macVendor(self) -> None:
        nm = nmap.PortScanner()
        nm.scan(hosts=self.ipv4, arguments="-sP")
        logging.info(nm.command_line())
        if self.ipv4 in nm.all_hosts():
            if "mac" in nm[self.ipv4]["addresses"]:
                self.__mac = nm[self.ipv4]["addresses"]["mac"]
            else:
                logging.warning("Impossible de trouver l'adresse MAC de la machine.")
                self.__mac = VAR_STR_DEFAULT

            if "vendor" in nm[self.ipv4] and self.macAddress != VAR_STR_DEFAULT:
                self.__vendor = nm[self.ipv4]["vendor"][self.macAddress]
            else:
                logging.warning("Impossible de trouver le constructeur de la machine.")
                self.__vendor = VAR_STR_DEFAULT
        else:
            logging.warning("Impossible de trouver les informations de la machine.")

    def set_nmap_hostname(self) -> None:
        nm = nmap.PortScanner()
        nm.scan(hosts=self.ipv4, arguments="-sL")
        logging.info(nm.command_line())
        if self.ipv4 in nm.all_hosts():
            if "hostnames" in nm[self.ipv4]:
                self.__name = nm[self.ipv4]["hostnames"][0]["name"]
            else:
                self.__name = VAR_STR_DEFAULT
    
    @property
    def vendor(self) -> str:
        return self.__vendor
    
    @vendor.setter
    def vendor(self, new_vendor: str) -> None:
        self.__vendor = new_vendor
