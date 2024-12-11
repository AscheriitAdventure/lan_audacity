from typing import Optional, Any, List
import typing
from enum import Enum
import logging
import ipaddress
from pysnmp.hlapi.v3arch.asyncio import *  # Connexion avec SNMP

from pysnmp.smi import builder, view, compiler, rfc1902  # Gestion des OID


VAR_MIB_SRC = 'http://mibs.snmplabs.com/asn1/@mib@'

class PrettyData:
    def __init__(self, oid: str, value: Any, data_type: str) -> None:
        self.__oid = oid
        self.__raw_value = value
        self.__data_type = data_type

    @property
    def oid(self) -> str:
        return self.__oid

    @property
    def rawValue(self) -> Any:
        return self.__raw_value

    @property
    def data_type(self) -> str:
        return self.__data_type

    def getOIDText(self) -> str:
        mibBuilder = builder.MibBuilder()
        compiler.add_mib_compiler(mibBuilder, sources=[VAR_MIB_SRC])
        mibViewController = view.MibViewController(mibBuilder)

        obj_name = rfc1902.ObjectIdentity(self.oid)
        obj_name.resolve_with_mib(mibViewController)

        pretty_name = ".".join(map(str, obj_name.get_label()))
        logging.debug(f"PrettyData::getOIDText: {pretty_name}")

        return pretty_name

    def getPrettyValue(self) -> str:
        """
        Cette fonction permet de convertir la valeur brute en une valeur lisible.
        0. On propose une liste de types de données SNMP.
        1. Grâce à la variable data_type, on peut déterminer le type de la valeur brute.
        2. Vérification de la valeur brute et du type de données.
        3. On convertit la valeur brute en une valeur lisible.

        Returns:
            str: prettyValue
        """
        return self.rawValue


class SnmpForm:
    class SnmpVersion(Enum):
        SNMPv1 = 0
        SNMPv2c = 1
        SNMPv3 = 2

    class IpVersion(Enum):
        Unknown = 99
        IPv4 = 4
        IPv6 = 6

    # @typing.overload
    def __init__(self, ip_address: str, port: int, version: SnmpVersion, community: str) -> None:
        self.__ip_address = ip_address
        self.__port = port
        self.__snmp_version = version
        self.__community = community
        self.__ip_version = None
        self.setIPVersion()

    @property
    def ipAddress(self) -> str:
        return self.__ip_address

    @ipAddress.setter
    def ipAddress(self, ip_address: str) -> None:
        self.__ip_address = ip_address
        self.setIPVersion()

    @property
    def portListened(self) -> int:
        return self.__port

    @property
    def communityPwd(self) -> str:
        return self.__community

    @portListened.setter
    def portListened(self, var: int) -> None:
        if 0 <= var <= 65535:
            self.__port = var
        else:
            logging.error("Port number must be between 0 and 65535")

    @communityPwd.setter
    def communityPwd(self, var: str) -> None:
        if var:
            self.__community = var
        else:
            logging.error("Community password must not be empty")

    @property
    def ipVersion(self) -> IpVersion:
        return self.__ip_version

    @ipVersion.setter
    def ipVersion(self, version: IpVersion) -> None:
        self.__ip_version = version

    @property
    def snmpVersion(self) -> SnmpVersion:
        return self.__snmp_version

    @snmpVersion.setter
    def snmpVersion(self, version: SnmpVersion) -> None:
        self.__snmp_version = version

    def getIPVersion(self, instance: str) -> Any:
        """Transforme la classe IpVersion en une valeur, qui peux être: hex, int, str.

        Args:
            instance (_type_): valeur attendu en sortie de la fonction.
            les types de sortie peuvent être: hex, int, str, bin

        Returns:
            Any: dépend du type de sortie attendu.
        """
        result_value = None
        if instance == 'int':
            logging.debug(f"ipVersion: int")
            result_value = self.ipVersion.value
        elif instance == 'str':
            logging.debug(f"ipVersion: str")
            result_value = self.ipVersion.name
        elif instance == 'hex':
            logging.debug(f"ipVersion: hex")
            result_value = hex(self.ipVersion.value)
        elif instance == 'bin':
            logging.debug(f"ipVersion: bin")
            result_value = bin(self.ipVersion.value)
        else:
            logging.error("Invalid instance type")
        return result_value

    def setIPVersion(self) -> None:
        try:
            ip_obj = ipaddress.ip_address(self.ipAddress)
            if isinstance(ip_obj, ipaddress.IPv4Address):
                self.ipVersion = self.IpVersion.IPv4
            elif isinstance(ip_obj, ipaddress.IPv6Address):
                self.ipVersion = self.IpVersion.IPv6
            else:
                self.ipVersion = self.IpVersion.Unknown
        except ValueError as e:
            logging.error(f"Invalid IP address: {self.ipAddress}")
            raise e

    def readDeviceUptime(self) -> Optional[Any]:
        oid_str = ""
        data: Any = []
        return data

    def scanIterfaces(self) -> Optional[Any]:
        data: Any = []
        return data

    def getCustomOID(self, oid: str) -> Optional[Any]:
        data: Any = []
        return data

    async def getWalkOID(self, oid: str) -> Optional[List[PrettyData]]:
        """ Cette fonction permet de récupérer les données d'un OID en utilisant la méthode SNMP Walk.
        1. On vérifie si l'OID est valide.
        2. On utilise la méthode SNMP Walk pour récupérer les données.
        3. On enregistre les données dans une liste. grace à la fonction PrettyData, on peut convertir les données brutes en données lisibles.
        4. On retourne la liste des données.

        Returns:
        data: List[PrettyData] = []
        PrettyData: oid, raw_value, data_type
        data =[
            PrettyData(oid="1.3.6.1.2.1.1.2.0", raw_value="1.3.6.1.4.1.9.1.503", data_type="OBJECT IDENTIFIER"),
            ...
            ]
        """
        data: List[PrettyData] = []
        snmp_engine = SnmpEngine()

        iterator = walk_cmd(
            snmp_engine,
            CommunityData(self.communityPwd, mpModel=self.snmpVersion.value),
            await UdpTransportTarget.create((self.ipAddress, self.portListened)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )

        async for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication:
                logging.error(errorIndication)
                break

            elif errorStatus:
                logging.error(
                    "{} at {}".format(
                        errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                    )
                )
                break
            else:
                for varBind in varBinds:
                    if str(varBind[0]).startswith(oid):
                        oid_str = varBind[0].get_oid()
                        value = varBind[1]
                        data_type = value.__class__.__name__
                        data.append(PrettyData(oid_str, value, data_type))
                    else:
                        continue
        return data

    def getListCustomOID(self, oid_list: list) -> Optional[Any]:
        data: Any = []
        return data

    def getListWalkOID(self, oid_list: list) -> Optional[Any]:
        data: Any = []
        return data


