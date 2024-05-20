import sys
from pysnmp.hlapi import *

def walk(host, oid):
    for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
            SnmpEngine(),
            CommunityData('ArteEyrein'),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False  # This caps the walk by the initial OID
    ):
        if errorIndication:
            print(errorIndication, file=sys.stderr)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
            break
        else:
            for varBind in varBinds:
                print(varBind)

walk('192.168.90.250', '1.3.6.1.4.1.9.1.503')
# response 0: SNMPv2-MIB::sysObjectID.0 = SNMPv2-SMI::enterprises.9.1.503
# ou
# response: 1.3.6.1.4.1.9.1.503
