import os
import sys
import platform
import uuid
import time
import subprocess
import logging
import nmap
from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity

class ClockManager:
    def __init__(self):
        self.__clock_created: float = time.time()
        self.__clock_list: list[float] = []
        self.__clock_list.append(self.clock_created)
        self.type_time = "Unix Timestamp Format"

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


class IconItem:
    def __init__(self, obj_ico: any, title: str):
        self.__obj_ico = obj_ico
        self.__label = title

    @property
    def objIcon(self):
        return self.__obj_ico

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, var: str):
        if var:
            self.__label = var

    @objIcon.setter
    def objIcon(self, var: any):
        self.__obj_ico = var


class KeyboardItem:
    def __init__(self, name_action: str, key_shortcut: str, icon_action=None):
        self.__name_action = name_action
        self.__key_shortcut = key_shortcut
        self.__icon_action = icon_action

    @property
    def nameAction(self):
        return self.__name_action

    @property
    def keyShortcut(self):
        return self.__key_shortcut

    @property
    def iconAction(self):
        return self.__icon_action

    @nameAction.setter
    def nameAction(self, var: str):
        if var:
            self.__name_action = var

    @keyShortcut.setter
    def keyShortcut(self, var: str):
        if var:
            self.__key_shortcut = var


class SoftwareParameters:
    def __init__(self):
        self.__version: str = '2.5.7'
        self.__type_app: str = 'Desktop'
        self.__dev_python_version: str = sys.version
        self.__dev_qt_version: str = os.environ['QT_API']
        self.__os: str = platform.system() or os.name
        self.__depot_platform: str = 'Aucune'

    @property
    def versionSftw(self):
        return self.__version

    @property
    def typeApp(self):
        return self.__type_app

    @property
    def pyUsed(self):
        return self.__dev_python_version

    @property
    def qtUsed(self):
        return self.__dev_qt_version

    @property
    def osPlatform(self):
        return self.__os

    @property
    def updatePlatform(self):
        return self.__depot_platform


class StatusDevice:
    def __init__(self, icon: any, flag: str, describe: str | None = None):
        self.__icon_status: any = icon
        self.__flag: str = flag
        self.__describe: str | None = describe

    @property
    def iconStatus(self):
        return self.__icon_status

    @iconStatus.setter
    def iconStatus(self, var: any):
        if var:
            self.__icon_status = var
        pass

    @property
    def flagStatus(self):
        return self.__flag

    @flagStatus.setter
    def flagStatus(self, var: str):
        if var:
            self.__flag = var
        pass

    @property
    def describeStatus(self):
        return self.__describe

    @describeStatus.setter
    def describeStatus(self, var: str):
        if var:
            self.__describe = var
        pass


class SnmpDevice:
    def __init__(self, port: int = 161, community: str = 'public'):
        self.__port = port
        self.__community = community
        self.publicData:dict = {}
        self.privateData:dict = {}

    @property
    def portListened(self):
        return self.__port

    @property
    def communityPwd(self):
        return self.__community

    @portListened.setter
    def portListened(self, var: int):
        if 0 <= var <= 65535:
            self.__port = var

    @communityPwd.setter
    def communityPwd(self, var: str):
        if var:
            self.__community = var
    
    def snmp_publicWalk(self, ipv4: str):
        data: dict = {}
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(
                SnmpEngine(),
                CommunityData(self.communityPwd, mpModel=1),  # SNMPv2c
                UdpTransportTarget((ipv4, 161)),
                ContextData(),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysObjectID', 0)),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysContact', 0)),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0)),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0)),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysServices', 0))
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

        self.publicData = data
    
    def snmp_privateWalk(self, ipv4: str):
        print(f'Hello World {ipv4}!')


class Device:
    def __init__(self, ipv4: str, mask: str):
        self.__ipv4: str = ipv4 # Adresse IPv4
        self.__mask = mask # Masque de sous-réseau IPv4
        self.__ipv6_lc: str | None = None # Adresse IPv6 locale
        self.__ipv6_glb: str | None = None # Adresse IPv6 globale
        self.__mac_address: str | None = None # Adresse MAC
        self.__hostname: str = 'Unknown' # Nom d'hôte
        self.__is_connected: bool = False # Ping
        self.__vendor: str | None = None # Fournisseur du matériel
        self.__dns_name: str | None = None # Nom DNS
        self.__mdns_name: str | None = None # Nom mDNS
        self.__smb_name: str | None = None # Nom SMB
        self.__smb_domain: str | None = None # Domaine SMB
        self.__ls_ports: list[dict] = [] # Liste des ports découverts

        self.__clock_manager = ClockManager() # Gestionnaire de synchronisation
        self.__status_obj: StatusDevice | None = None # Statut de l'appareil
        self.__ls_os: list[dict] = [] 
        self.__snmp_info: SnmpDevice | None = None 
        self.__link_network: list | None = None

    @property
    def ipv4Address(self):
        return self.__ipv4
    @property
    def ipv6Local(self):
        return self.__ipv6_lc
    @property
    def ipv6Global(self):
        return self.__ipv6_glb
    @property
    def macAddress(self):
        return self.__mac_address
    @property
    def hostnameDevice(self):
        return self.__hostname
    @property
    def vendorDevice(self):
        return self.__vendor
    @property
    def dnsName(self):
        return self.__dns_name
    @property
    def mdnsName(self):
        return self.__mdns_name
    @property
    def smbName(self):
        return self.__smb_name
    @property
    def smbDomain(self):
        return self.__smb_domain
    @property
    def clockManager(self):
        return self.__clock_manager
    @property
    def isConnected(self):
        return self.__is_connected
    @isConnected.setter
    def isConnected(self, var: bool):
        self.__is_connected = var
        self.clockManager.add_clock()
    @property
    def statusDevice(self):
        return self.__status_obj
    @property
    def snmpDevice(self):
        return self.__snmp_info
    @property
    def linkNetwork(self):
        return self.__link_network
    @property
    def maskAddress(self):
        return self.__mask
    @property
    def lsPorts(self):
        return self.__ls_ports
    @lsPorts.setter
    def lsPorts(self, var: list[dict]):
        if len(var) > 0:
            self.__ls_ports = var
    @property
    def lsOS(self):
        return self.__ls_os
    @lsOS.setter
    def lsOS(self, var: list[dict]):
        if len(var) > 0:
            self.__ls_os = var

    def set_statusDevice(self, icon, name, dsc: str = None):
        self.__status_obj = StatusDevice(icon, name, dsc)

    def get_cidrAddress(self) -> str:
        bits = sum(bin(int(x)).count('1') for x in self.maskAddress.split('.'))
        return f"{self.ipv4Address}/{bits}"
  
    def set_ports(self):
        nm = nmap.PortScanner()
        nm.scan(hosts=self.ipv4Address, arguments='-sS -p 1-65535')
        self.lsPorts = nm[self.ipv4Address].items()
    
    def set_os(self):
        nm = nmap.PortScanner()
        nm.scan(hosts=self.ipv4Address, arguments='-O')
        self.lsOS = nm[self.ipv4Address].items()

    def setIsConnected(self) -> None:
        self.clockManager.add_clock()
        try:
            result = subprocess.run(['ping', '-a -c4', self.ipv4Address], stdout=subprocess.PIPE)
            self.isConnected = result.returncode == 0
        except Exception as e:
            logging.warning(f"Subprocess Error with ping for {self.ipv4Address}: {e}")

    def setStatusDevice(self, icon: any, label: str, describe: str | None = None) -> None:
        self.__status_obj = StatusDevice(icon, label, describe)

    def setSnmpDevice(self):
        self.__snmp_info = SnmpDevice()
    
    def set_ipv6_local(self):
        nm = nmap.PortScanner()
        nm.scan(hosts=self.ipv4Address, arguments='-6')
        self.__ipv6_lc = nm[self.ipv4Address].get('addresses').get('ipv6')
    
    def set_ipv6_global(self):
        nm = nmap.PortScanner()
        nm.scan(hosts=self.ipv4Address, arguments='-6')
        self.__ipv6_glb = nm[self.ipv4Address].get('addresses').get('ipv6')
    
    def set_mac_address(self):
        nm = nmap.PortScanner()
        nm.scan(hosts=self.ipv4Address, arguments='-sP')
        self.__mac_address = nm[self.ipv4Address].get('addresses').get('mac')


class TextTranslate:
    def __init__(self, ref_lang: str | int, ref_expression: str | int, text: str):
        self.uuid = uuid.uuid4()
        self.__ref_lang = ref_lang
        self.__ref_expression = ref_expression
        self.__translate = text

    @property
    def referenceLangue(self):
        return self.__ref_lang

    @referenceLangue.setter
    def referenceLangue(self, var: str|int):
        if var:
            self.__ref_lang = var

    @property
    def referenceExpression(self):
        return self.__ref_expression

    @referenceExpression.setter
    def referenceExpression(self, var: str|int):
        if var:
            self.__ref_expression = var

    @property
    def textTranslate(self):
        return self.__translate

    @textTranslate.setter
    def textTranslate(self, var: str):
        if var:
            self.__translate = var
    
class Network:
    def __init__(self, ipv4: str, mask: str, name: str=None, description: str=None):
        self.__name = name
        self.__description = description
        self.__ipv4 = ipv4
        self.__mask = mask
        self.__ls_devices: list[Device] = []
        self.__clock_manager = ClockManager()
        self.__status_obj: StatusDevice | None = None
    
    @property
    def nameNetwork(self):
        return self.__name
    @nameNetwork.setter
    def nameNetwork(self, var: str):
        if var:
            self.__name = var
    @property
    def descriptionNetwork(self):
        return self.__description
    @descriptionNetwork.setter
    def descriptionNetwork(self, var: str):
        if var:
            self.__description = var
    @property
    def ipv4Network(self):
        return self.__ipv4
    @property
    def maskNetwork(self):
        return self.__mask
    @property
    def lsDevices(self):
        return self.__ls_devices
    @property
    def clockManager(self):
        return self.__clock_manager
    @property
    def statusNetwork(self):
        return self.__status_obj
    def set_statusNetwork(self, icon, name, dsc: str = None):
        self.__status_obj = StatusDevice(icon, name, dsc)

class NetworkManager:
    def __init__(self):
        self.__ls_networks: list[Network] = []
    
    @property
    def lsNetworks(self):
        return self.__ls_networks
    def add_network(self, network: Network):
        self.__ls_networks.append(network)
    def remove_network(self, network: Network):
        self.__ls_networks.remove(network)
    def remove_network_index(self, index: int):
        self.__ls_networks.pop(index)
    def get_network(self, index: int):
        return self.__ls_networks[index]
    def get_network_by_name(self, name: str):
        for network in self.__ls_networks:
            if network.nameNetwork == name:
                return network
        return None
    def get_network_by_ipv4(self, ipv4: str):
        for network in self.__ls_networks:
            if network.ipv4Network == ipv4:
                return network
        return None
    
    
