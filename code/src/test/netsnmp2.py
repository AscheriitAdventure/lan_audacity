from pysnmp.hlapi import *

# Configuration SNMP
community_string = 'ArteEyrein'
ip_address = '192.168.90.250'
snmp_port = 161  # Port SNMP par défaut
oid_routing_table = '1.3.6.1.2.1.4.21.1'  # OID pour la table de routage IPv4

# Fonction pour effectuer un SNMP walk
def snmp_walk(community_string, ip_address, oid):
    try:
        for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
                SnmpEngine(),
                CommunityData(community_string),
                UdpTransportTarget((ip_address, snmp_port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                lexicographicMode=False
        ):
            if errorIndication:
                print(f"Erreur SNMP : {errorIndication}")
                break
            elif errorStatus:
                print(f"Erreur dans la requête SNMP : {errorStatus}")
                break
            else:
                print('en0: '+len(varBinds))
                for varBind in varBinds:
                    print(f"{varBind[0]} = {varBind[1]}")
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête SNMP : {e}")

# Appel de la fonction pour récupérer la table de routage
snmp_walk(community_string, ip_address, oid_routing_table)
