from pysnmp.hlapi import *
import logging


class PysnmpForm:
    def __init__(self, port: int = 161, community: str = "public"):
        self.__port = port
        self.__community = community
        self.publicData: dict = {}
        self.privateData: dict = {}

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

    def snmp_publicWalk(self, ipv4: str) -> None:
        data: dict = {}
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(
                SnmpEngine(),
                CommunityData(self.communityPwd, mpModel=1),  # SNMPv2c
                UdpTransportTarget((ipv4, 161)),
                ContextData(),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysObjectID", 0)),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysUpTime", 0)),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysContact", 0)),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysName", 0)),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysLocation", 0)),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysServices", 0)),
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

    def snmp_privateWalk(self, ipv4: str, sysObjectID: str) -> None:
        # Pour lancer cette fonction il faut posséder le mot de passe de la communauté privée
        # Pour lancer cette fonction il faut posséder le sysObjectID de l'agent
        # Cette fonction a pour objectif de récupérer les informations de l'agent SNMP
        if not sysObjectID:
            logging.error("sysObjectID must be provided to walk the private SNMP MIB.")
            return

        data: dict = {}
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(
                SnmpEngine(),
                CommunityData(self.communityPwd, mpModel=1),  # SNMPv2c
                UdpTransportTarget((ipv4, self.portListened)),
                ContextData(),
                ObjectType(ObjectIdentity("IP-MIB", "ipRouteEntry")),
                ObjectType(ObjectIdentity("IP-MIB", "ipCidrRouteEntry")),
            )
        )
        if errorIndication:
            logging.error(errorIndication)
        elif errorStatus:
            logging.error(
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

        self.privateData = data
