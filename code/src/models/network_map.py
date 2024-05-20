from src.models.network_mdl import Network
from src.models.device import Device
import logging
import nmap


class NetworkMap(Network):
    def __init__(
        self, ipv4: str = None, mask: str = None, ip_cidr: str = None, name: str = None
    ):
        super().__init__(ipv4, mask, ip_cidr)
        if name:
            self.__name = name
        else:
            self.__name = self.ipv4_mask_to_cidr(self.ipv4, self.mask)

        self.__devices: list[Device] = []

    @property
    def networkName(self) -> str:
        return self.__name

    @property
    def devicesList(self) -> list[Device]:
        return self.__devices

    @networkName.setter
    def networkName(self, var: str) -> None:
        if var:
            self.__name = var
        else:
            logging.error("Le nom du réseau est vide ou non-renseigné.")

    def add_device(self, device: Device) -> None:
        self.__devices.append(device)

    def remove_device(self, device: Device) -> None:
        self.__devices.remove(device)

    def get_lenght_devices(self) -> int:
        return len(self.devicesList)

    def get_nb_addr_max(self) -> int:
        return 2 ** (32 - self.nb_mask_bits())

    def get_nb_addr_usable(self) -> int:
        return self.get_nb_addr_max() - 2

    def get_nb_addr_occuped(self) -> int:
        nm = nmap.PortScanner()
        nm.scan(hosts=self.ipv4_mask_to_cidr(self.ipv4, self.mask), arguments="-sP")
        return len(nm.all_hosts())

    def get_nb_addr_free(self) -> int:
        return self.get_nb_addr_usable() - self.get_nb_addr_occuped()


class NetworkMapManager:
    def __init__(self):
        self.__networks: list[NetworkMap] = []

    @property
    def networksList(self) -> list[NetworkMap]:
        return self.__networks

    def add_network(self, network: NetworkMap) -> None:
        self.__networks.append(network)

    def remove_network(self, network: NetworkMap) -> None:
        self.__networks.remove(network)

    def get_lenght_networks(self) -> int:
        return len(self.networksList)

    def get_network_by_name(self, name: str) -> NetworkMap:
        for network in self.networksList:
            if network.networkName == name:
                return network
        return None

    def get_network_by_ipv4(self, ipv4: str) -> NetworkMap:
        for network in self.networksList:
            if network.ipv4 == ipv4:
                return network
        return None

    def get_network_by_mask(self, mask: str) -> NetworkMap:
        for network in self.networksList:
            if network.mask == mask:
                return network
        return None

    def get_network_by_ip_cidr(self, ip_cidr: str) -> NetworkMap:
        for network in self.networksList:
            if network.ip_cidr == ip_cidr:
                return network
        return None
