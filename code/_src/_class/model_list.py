import configparser
import csv
import json
import netifaces
import os
import re
import socket
import string
import time
import xmltodict
import yaml
import nmap
from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity


class ClockManager:
    def __init__(self):
        self.__clock_created: float = time.time()
        self.__clock_list: list[float] = []
        self.__clock_list.append(self.clock_created)

    @property
    def clock_created(self):
        return self.__clock_created

    @property
    def clock_list(self):
        return self.__clock_list

    def add_clock(self):
        self.clock_list.append(time.time())

    def get_clock_list(self):
        return self.clock_list

    def get_clock_created(self):
        return self.clock_created

    def get_clock_last(self):
        return self.clock_list[-1]

    def get_clock_diff(self):
        return self.clock_list[-1] - self.clock_list[-2]

    @staticmethod
    def conv_unix_to_datetime(unix_time: float):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unix_time))

    def __str__(self) -> str:
        return f"ClockManager: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.clock_created))}"


class Device:
    def __init__(
        self,
        name: str = "Unknown",
        ip: str = "0.0.0.0",
        mac: str = "00:00:00:00:00:00",
        mask: str = "255.0.0.0",
    ):
        self.__name: str = name
        self.__ip: str = ip
        self.__mac: str = mac
        self.__mask: str = mask
        self.__clock_manager: ClockManager = ClockManager()

    @property
    def clocktime(self):
        return self.__clock_manager
    @property
    def name(self):
        return self.__name

    @property
    def ipv4(self):
        return self.__ip

    @property
    def mac(self):
        return self.__mac

    @property
    def mask(self):
        return self.__mask

    @name.setter
    def name(self, name: str):
        if name != "" or name is not None:
            self.__name = name

    @ipv4.setter
    def ipv4(self, ip: str):
        if self.true_ip(self, ipv4=ip):
            self.__ip = ip
        else:
            raise ValueError("IP address is not valid")

    @mac.setter
    def mac(self, mac: str):
        if self.true_mac(self, mac):
            self.__mac = mac
        else:
            raise ValueError("MAC address is not valid")

    @mask.setter
    def mask(self, mask: str):
        if self.true_ip(self, mask):
            self.__mask = mask
        else:
            raise ValueError("Mask address is not valid")

    def __str__(self) -> str:
        return f"NetDevice: {self.name}/{self.ipv4}/{self.mac}"

    def set_mask(self):
        interfaces = netifaces.interfaces()
        for interface in interfaces:
           if netifaces.AF_INET in netifaces.ifaddresses(interface):
               inet_info = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
               print(inet_info)
               self.mask = inet_info['netmask']
               break
        # self.mask = str(ipaddress.IPv4Network(self.ipv4).netmask)
           
    def set_name(self):
        self.name = socket.gethostname()

    def set_addrMac(self):
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            if netifaces.AF_LINK in netifaces.ifaddresses(interface):
                mac_info = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]
                self.mac = mac_info['addr']
                break

    @staticmethod
    def true_ip(self, ipv4: str) -> bool:
        ipv4_pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
        match = re.match(ipv4_pattern, ipv4)
        if match:
            if all(0 <= int(octet) <= 255 for octet in match.groups()):
                return True
        return False

    @staticmethod
    def true_mac(self, mac: str) -> bool:
        mac_pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
        match = re.match(mac_pattern, mac)
        if match:
            return True
        return False


class SNMP:
    def __init__(self, ip: str, community: str, port: int = 161):
        self.__ip: str = ip
        self.__community: str = community
        self.__port: int = port

    @property
    def ip(self):
        return self.__ip

    @property
    def community(self):
        return self.__community

    @property
    def port(self):
        return self.__port

    @staticmethod
    def true_ip(self: object, ipv4: str) -> bool:
        ipv4_pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
        match = re.match(ipv4_pattern, ipv4)
        if match:
            if all(0 <= int(octet) <= 255 for octet in match.groups()):
                return True
        return False

    @ip.setter
    def ip(self, ip: str):
        if self.true_ip(self, ipv4=ip):
            self.__ip = ip
        else:
            raise ValueError("IP address is not valid")

    @community.setter
    def community(self, community: str):
        if community != "" or community is not None:
            self.__community = community

    @port.setter
    def port(self, port: int):
        if 0 <= port <= 65535:
            self.__port = port
        else:
            raise ValueError("Port is not valid")

    def snmp_walk(target: str, oid: str):
        data: dict = {}
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(
                SnmpEngine(),
                CommunityData("public", mpModel=1),  # SNMPv2c
                UdpTransportTarget((target, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                lexicographicMode=False,
            )
        )
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print(
                "%s at %s"
                % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                )
            )
        else:
            for varBind in varBinds:
                name, value = varBind
                data[str(name)] = str(value)

        return data


class NetDevice(Device):
    def __init__(
        self,
        name: str = "Unknown",
        ip: str = "0.0.0.0",
        mac: str = "00:00:00:00:00:00",
        mask: str = "255.0.0.0",
        community: str = "public"
    ):
        super().__init__(name, ip, mac, mask)
        self.__snmp: SNMP = SNMP(ip, community)
        self.__nmap_info: dict = {}
        self.__snmp_info: dict = {}
        self.__ping: bool = False

    @property
    def snmp(self):
        return self.__snmp

    @property
    def nmap_info(self):
        return self.__nmap_info

    @property
    def snmp_info(self):
        return self.__snmp_info

    @property
    def ping(self):
        return self.__ping

    @ping.setter
    def ping(self, ping: bool):
        self.__ping = ping

    def init_nmap_info(self):
        nm = nmap.PortScanner()
        nm.scan(hosts=self.ipv4, arguments="-sP -p- -T4 -O -v")
        self.__nmap_info = nm[self.ipv4]

    def init_snmp_info(self, init_oid: str = "1.3.6.1.2.1.1"):
        print(f"get_public_oid: .iso.org.dod.internet.mgmt.mib-2.system. ou {init_oid}")
        self.__snmp_info = self.snmp.snmp_walk(self.ipv4, init_oid)


class DeviceManager:
    def __init__(self):
        self.__device_list: list[NetDevice] = []

    @property
    def device_list(self):
        return self.__device_list

    def add_device(self, device: NetDevice):
        self.device_list.append(device)

    def get_device_list(self):
        return self.device_list

    def __str__(self) -> str:
        return f"DeviceManager: {len(self.device_list)} devices"


class FileConf:
    def __init__(self, abs_path: str):
        self.__abs_path: str = abs_path
        self.__file: str = os.path.basename(abs_path)
        self.__data: any = None

    @property
    def abs_path(self):
        return self.__abs_path

    @property
    def file(self):
        return self.__file

    @property
    def data(self):
        return self.__data

    @file.setter
    def file(self, file: str):
        if isinstance(file, str):
            self.__file = os.path.basename(file)
        else:
            raise ValueError("Le nom du fichier doit être une chaîne de caractères.")

    def read_file(self):
        switch_file = SwitchFile()
        if os.path.exists(self.abs_path):
            return getattr(
                switch_file, FileConf.get_extension(self.abs_path), switch_file.txt
            )()

    @staticmethod
    def get_extension(abs_path: str) -> str:
        _, file_extension = os.path.splitext(abs_path)
        return file_extension.lower().strip(string.punctuation)


class SwitchFile:
    def json(self, abs_path: str) -> any:
        with open(abs_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def yaml(self, abs_path: str) -> any:
        with open(abs_path, "r", encoding="utf-8") as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def xml(self, abs_path: str):
        with open(abs_path, "r", encoding="utf-8") as file:
            return xmltodict.parse(file.read())

    def csv(self, abs_path: str) -> any:
        with open(abs_path, "r", encoding="utf-8") as file:
            return csv.DictReader(file)

    def txt(self, abs_path: str):
        with open(abs_path, "r", encoding="utf-8") as file:
            return file.read()

    def ini(self, abs_path: str) -> any:
        config = configparser.ConfigParser()
        config.read(abs_path, encoding="utf-8")
        return config

    def conf(self, abs_path: str) -> any:
        config = configparser.ConfigParser()
        config.read(abs_path)
        return config
