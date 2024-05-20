import uuid
import nmap
from _class.cl_clock import ClockManager


class NetworkManager:
    def __init__(self, adressecidr: str):
        self.__uuid = uuid.uuid4()
        self.__adressecidr: str = adressecidr
        self.__lsaddr: list = []
        self.__clock = ClockManager()

    @property
    def clock(self):
        return self.__clock

    @property
    def uuid(self):
        return self.__uuid

    @property
    def addrCIDR(self):
        return self.__adressecidr

    @addrCIDR.setter
    def addrCIDR(self, value: str):
        self.__adressecidr = value
        self.clock.set_lastUpdate()


    @property
    def lsaddr(self):
        return self.__lsaddr

    @lsaddr.setter
    def lsaddr(self, value: list):
        if len(value) > 0 or value is not None:
            self.__lsaddr = value
            self.clock.set_lastUpdate()

    def set_addr(self):
        try:
            nm = nmap.PortScanner()
            nm.scan(hosts=self.__adressecidr, arguments='-sn')
            self.lsaddr = nm.all_hosts()
            self.clock.set_lastUpdate()
        except nmap.PortScannerError:
            print('Erreur lors du scan du réseau.')
