import ipaddress
import logging


class Network:
    def __init__(self, ipv4: str = None, mask: str = None, ip_cidr: str = None):
        if ip_cidr:
            self.__ipv4, self.__mask = self.cidr_to_ipv4(ip_cidr)
        elif ipv4 and mask:
            self.__ipv4 = ipv4
            self.__mask = mask
        else:
            logging.error(
                "Please provide either IPv4 address with subnet mask or CIDR notation."
            )
        self.__icon = None
    
    @property
    def ipv4(self):
        return self.__ipv4
    
    @property
    def mask(self):
        return self.__mask
    
    @property
    def iconLan(self):
        return self.__icon
    
    @iconLan.setter
    def iconLan(self, var: any):
        self.__icon = var
    
    @ipv4.setter
    def ipv4(self, var: str):
        if var:
            self.__ipv4 = var
    
    @mask.setter
    def mask(self, var: str):
        if var:
            self.__mask = var

    def nb_mask_bits(self):
        return sum(bin(int(x)).count("1") for x in self.mask.split("."))
    
    def setIconLan(self, icon: any):
        self.iconLan = icon

    @staticmethod
    def cidr_to_ipv4(cidr: str):
        ip_network = ipaddress.ip_network(cidr, strict=False)
        return str(ip_network.network_address), str(ip_network.netmask)

    @staticmethod
    def ipv4_mask_to_cidr(ip: str, mask: str):
        ip_cidr = ip + "/" + str(sum(bin(int(x)).count("1") for x in mask.split(".")))
        return ip_cidr
