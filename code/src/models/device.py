from src.models.network_mdl import Network
from src.models.nmap_form import NmapForm
from src.models.pysnmp_form import PysnmpForm
from src.models.clock import ClockManager
import logging
import nmap
import subprocess


class Device(Network):
    def __init__(
        self,
        ipv4: str = None,
        mask: str = None,
        ip_cidr: str = None,
        name: str = None,
        mac: str = None,
        vendor: str = None,
    ):
        super().__init__(ipv4, mask, ip_cidr)
        self.__is_connected = False
        if name:
            self.__name = name
        else:
            self.__name = self.ipv4
        if mac:
            self.__mac = mac
        if vendor:
            self.__vendor = vendor
        else:
            self.__vendor = "Unknown"

        self.__nmap_infos: NmapForm = NmapForm(self.ipv4)

        self.__pysnmp_infos: PysnmpForm = PysnmpForm()

        self.__clock_manager = ClockManager()

    @property
    def deviceName(self) -> str:
        return self.__name

    @property
    def clockManager(self):
        return self.__clock_manager

    @property
    def pysnmpInfos(self) -> PysnmpForm:
        return self.__pysnmp_infos

    @deviceName.setter
    def deviceName(self, var: str) -> None:
        if var:
            self.__name = var
        else:
            logging.error("Le nom de la machine est vide ou non-renseigné.")

    @property
    def macAddress(self) -> str:
        return self.__mac

    @macAddress.setter
    def macAddress(self, var: str) -> None:
        if var:
            self.__mac = var
        else:
            logging.error("L'adresse MAC est vide ou non-renseignée.")

    @property
    def isConnected(self) -> bool:
        return self.__is_connected

    @isConnected.setter
    def isConnected(self, var: bool) -> None:
        self.__is_connected = var

    @property
    def vendor(self) -> str:
        return self.__vendor

    @vendor.setter
    def vendor(self, var: str) -> None:
        if var:
            self.__vendor = var
        else:
            logging.error("Le nom du constructeur est vide ou non-renseigné.")

    @property
    def nmapInfos(self) -> NmapForm:
        return self.__nmap_infos

    def set_nmap_hostname(self) -> None:
        nm = nmap.PortScanner()
        nm.scan(hosts=self.ipv4, arguments="-sL")
        logging.info(nm.command_line())
        if self.ipv4 in nm.all_hosts():
            self.__name = nm[self.ipv4]["hostnames"][0]["name"]
        else:
            logging.error("Impossible de trouver le nom de la machine via DNS.")

    def set_nmap_mac(self) -> None:
        nm = nmap.PortScanner()
        nm.scan(hosts=self.ipv4, arguments="-sP")
        logging.info(nm.command_line())
        if self.ipv4 in nm.all_hosts():
            self.__mac = nm[self.ipv4]["addresses"]["mac"]
        else:
            logging.error("Impossible de trouver l'adresse MAC de la machine.")

    def set_nmap_vendor(self) -> None:
        nm = nmap.PortScanner()
        nm.scan(hosts=self.ipv4, arguments="-sP")
        logging.info(nm.command_line())
        if self.ipv4 in nm.all_hosts():
            self.__vendor = nm[self.ipv4]["vendor"]
        else:
            logging.error("Impossible de trouver le constructeur de la machine.")

    def set_isConnected(self) -> None:
        try:
            result = subprocess.run(
                ["ping", "-c4", self.ipv4],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
            if result.returncode == 0:
                self.isConnected = True
                logging.info("La machine est connectée.")
            else:
                self.isConnected = False
                logging.error("La machine n'est pas connectée.")
        except subprocess.TimeoutExpired:
            self.isConnected = False
            logging.error("Timeout lors de la tentative de connexion à la machine.")
