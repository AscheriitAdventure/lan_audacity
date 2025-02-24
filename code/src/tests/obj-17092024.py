from src.classes.clockManager import ClockManager
from src.classes.cl_deviceType import DeviceType
from src.components.nmap_forms import NmapForm
from src.components.pysnmp_forms import PysnmpForm
from typing import Any, Optional

import uuid
import ipaddress

VAR_ADDRESS_IP = {
    "ipv4": "",
    "mask_ipv4": "",
    "ipv4_public": "",
    "cidr": "",
    "ipv6_local": "",
    "ipv6_global": ""
}

def _parse_cidr(cidr: str) -> tuple:
    """
        Parses the CIDR string into network address and prefix length.

        :param cidr: CIDR string in the format 'address/prefix'
        :return: A tuple of (network_address, prefix_length)
    """
    try:
        network, prefix = cidr.split('/')
        prefix = int(prefix)
        return network, prefix
    except ValueError:
        raise ValueError("Invalid CIDR format")

def _derive_subnet_mask(self, prefix: int) -> str:
        """
        Derives the subnet mask from the prefix length.

        :param prefix: The prefix length (e.g., 24 for '/24')
        :return: Subnet mask corresponding to the prefix length (e.g., '255.255.255.0')
        """
        # Convert prefix to netmask using ipaddress module
        return str(ipaddress.IPv4Network(f"0.0.0.0/{prefix}").netmask)

def ip_and_mask_to_cidr(ipv4: str, mask_ipv4: str) -> str:
    """
        Converts an IPv4 address and subnet mask into CIDR notation.
        
        :param ipv4: The IP address (e.g., '192.168.0.1')
        :param mask_ipv4: The subnet mask (e.g., '255.255.255.0')
        :return: CIDR notation (e.g., '192.168.0.0/24')
    """
    # Create an IPv4 network object using the ip address and the mask
    network = ipaddress.IPv4Network(f"{ipv4}/{mask_ipv4}", strict=False)
    # Return the CIDR notation
    return str(network)

class NetObject:
    def __init__(self):
        self._name: str = "Unknown"        # eth0, wlan0, ...
        self._type: Optional[DeviceType] = None     # DeviceType object
        self._is_connected: bool = False  # {True, False}
        self._is_active: bool = False     # {True, False}
        self._address_ip: dict = VAR_ADDRESS_IP      # {ipv4, ipv6,...}

    @property
    def addressIp(self) -> dict:
        return self._address_ip

    @addressIp.setter
    def addressIp(self, address_ip) -> None:
        self._address_ip = address_ip

    @property
    def isActive(self) -> bool:
        return self._is_active

    @isActive.setter
    def isActive(self, is_active) -> None:
        self._is_active = is_active

    @property
    def isConnected(self) -> bool:
        return self._is_connected

    @isConnected.setter
    def isConnected(self, is_connected) -> None:
        self._is_connected = is_connected

    @property
    def type(self) -> DeviceType:
        return self._type

    @type.setter
    def type(self, type) -> None:
        self._type = type

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name) -> None:
        self._name = name
    
    def set_ipv4(self, ipv4: str) -> None:
        self.addressIp["ipv4"] = ipv4
    
    def set_ipv6_local(self, ipv6_local: str) -> None:
        self.addressIp["ipv6_local"] = ipv6_local
    
    def set_ipv6_global(self, ipv6_global: str) -> None:
        self.addressIp["ipv6_global"] = ipv6_global
    
    def set_mask_ipv4(self, mask_ipv4: str) -> None:
        self.addressIp["mask_ipv4"] = mask_ipv4
    
    def set_cidr(self, cidr: str) -> None:
        self.addressIp["cidr"] = cidr
    

class NetDevice(NetObject):
    def __init__(self, ipv4: str, mask_ipv4: str, uuid_str: Optional[str] = None):
        super().__init__()
        self.addressIp["ipv4"] = ipv4
        self.addressIp["mask_ipv4"] = mask_ipv4
        self.addressIp["cidr"] = ip_and_mask_to_cidr(ipv4, mask_ipv4)

        if uuid_str is not None:
            self._uuid = uuid_str
        else:
            self.setUUIDObj(uuid_str)
        
        self._clock_manager: ClockManager = ClockManager()  # ClockManager object
        self._mac: str = ""                 # MAC address
        self._vendor: str = "Unknown"       # Vendor name
        self._nmap_infos: NmapForm = NmapForm(self.addressIp["cidr"])   # NmapForm object
        self._snmp: PysnmpForm = PysnmpForm()       # PysnmpForm object
    
    @classmethod
    def from_cidr(cls, cidr: str) -> Any:
        network, prefix = _parse_cidr(cidr)
        mask = _derive_subnet_mask(prefix)
        return cls(network, mask)
    
    @classmethod
    def from_jsonfile(cls, jsonfile: Any) -> Any:
        pass

    @property
    def snmpInfos(self) -> PysnmpForm:
        return self._snmp
    
    @property
    def nmapInfos(self) -> NmapForm:
        return self._nmap_infos
    
    @property
    def macAddress(self) -> str:
        return self._mac
    
    @macAddress.setter
    def macAddress(self, mac) -> None:
        self._mac = mac
    
    @property
    def vendor(self) -> str:
        return self._vendor
    
    @vendor.setter
    def vendor(self, vendor) -> None:
        self._vendor = vendor
    
    @property
    def uuid(self) -> str:
        return self._uuid
    
    @uuid.setter
    def uuid(self, uuid) -> None:
        self._uuid = uuid
    
    @property
    def clockManager(self) -> ClockManager:
        return self._clock_manager
    
    @clockManager.setter
    def clockManager(self, clock_manager) -> None:
        self._clock_manager = clock_manager
    
    def setUUIDObj(self, var: Optional[str] = None) -> None:
        if var is None or var == "":
            self.uuid = str(uuid.uuid4())
        else:
            self.uuid = var
    
    def get_dict_object(self) -> dict:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "type": self.type,
            "clock_manager": self.clockManager.dict_return(),
            "address_ip": self.addressIp,
            "mac": self.macAddress,
            "vendor": self.vendor,
            "nmap_infos": self.nmapInfos,
            "snmp_infos": self.snmpInfos
        }
        

