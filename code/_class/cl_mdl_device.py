# Classe type Model
import subprocess
import uuid
import socket
import netifaces
from _class.cl_clock import ClockManager



class MDevice:
    def __init__(self, _hostname: str = 'Unknown',
                 _ipv4: str = '0.0.0.0', _mask: str = '0.0.0.0'):
        self.uuid = uuid.uuid4()
        self.__hostname: str = _hostname
        self.__ip: str = _ipv4
        self.__mask: str = _mask
    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, new_ip: str | None):
        if new_ip != '' or new_ip is not None:
            self.__ip = new_ip
        elif new_ip == '':
            self.__ip = socket.gethostbyname(self.hostname)
        else:
            raise ValueError('Invalid ip address')
    @property
    def hostname(self):
        return self.__hostname

    @hostname.setter
    def hostname(self, new_name: str | None):
        if new_name is not None or new_name != 'Unknown':
            if new_name != self.__hostname:
                self.__hostname = new_name
        elif new_name == 'Unknown':
            self.__hostname = socket.gethostname()

    @property
    def mask(self):
        return self.__mask
    @mask.setter
    def mask(self, new_mask: str):
        if new_mask != '0.0.0.0' or new_mask is not None:
            self.__mask = new_mask
        elif new_mask == '0.0.0.0':
            interfaces = netifaces.interfaces()
            for interface in interfaces:
                try:
                    if netifaces.AF_INET in netifaces.ifaddresses(interface):
                        addresses = netifaces.ifaddresses(interface)[netifaces.AF_INET]
                        for address in addresses:
                            if address['addr'] == self.ip:
                                self.__mask = address['netmask']
                                return
                except ValueError:
                    pass

    def mask_to_cidr(self):
        octets = self.mask.split('.')
        binaire = ''.join([bin(int(octet))[2:].zfill(8) for octet in octets])
        cidr = binaire.count('1')
        return f"/{cidr}"


class NetDevice(MDevice):
    def __init__(self, _ping: bool = False):
        super().__init__()
        self.datetime = ClockManager()
        self.__ping: bool = _ping

    @property
    def ping(self):
        return self.__ping
    @ping.setter
    def ping(self, value: str):
        if value == 'up':
            self.__ping = True
        elif value == 'down':
            self.__ping = False
        elif value == '' or value is None:
            result = subprocess.run(['ping', '-c', '4', self.ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.__ping = result.returncode == 0

class HostDevice(MDevice):
    def __init__(self):
        super().__init__()
        self.datetime = ClockManager()
