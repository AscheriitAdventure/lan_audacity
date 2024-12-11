from pysnmp.smi import builder, view, compiler
from pysnmp.smi.rfc1902 import ObjectIdentity


VAR_SRC_MIBS = 'file://D:/lan_audacity/backup/dev/py_mibs'

# Charger les fichiers MIB
mibBuilder = builder.MibBuilder()
compiler.add_mib_compiler(
    mibBuilder, sources=['http://mibs.snmplabs.com/asn1/@mib@', VAR_SRC_MIBS])

# Charger explicitement les modules MIB nécessaires
mib_list = [
    'SNMPv2-MIB',
    'IP-MIB',
    'IP-FORWARD-MIB',
    'IF-MIB',
    'DISMAN-EXPRESSION-MIB',
    'DISMAN-EVENT-MIB',
    'EXPRESSION-MIB',
    'RFC1213-MIB'
]
for mib in mib_list:
    try:
        mibBuilder.load_modules(mib)
    except Exception as e:
        # print(f"Erreur lors du chargement du module {mib} : {e}")
        print(f"Vérifiez que le module est bien installé dans le répertoire des MIBs")

# Construire un traducteur
mibViewController = view.MibViewController(mibBuilder)

# Exemple avec sysDescr
try:
    obj_lab = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)
    obj_lab.resolve_with_mib(mibViewController)
    pretty_name = ".".join(map(str, obj_lab.get_label()))
    print(obj_lab.get_oid())
    print(pretty_name)
except Exception as e:
    print(f"Erreur pour sysDescr : {e}")

# Exemple avec ipCidrRouteNumber
try:
    obj_lab = ObjectIdentity('IP-MIB', 'ipCidrRouteNumber', 0)
    obj_lab.resolve_with_mib(mibViewController)
    pretty_name = ".".join(map(str, obj_lab.get_label()))
    print(obj_lab.get_oid())
    print(pretty_name)
except Exception as e:
    print(f"Erreur pour ipCidrRouteNumber : {e}")

# Exemple avec un OID
try:
    obj_lab = ObjectIdentity('1.3.6.1.2.1.4.24.3.0')  # OID complet
    obj_lab.resolve_with_mib(mibViewController)
    pretty_name = ".".join(map(str, obj_lab.get_label()))
    print(obj_lab.get_oid())
    print(pretty_name)
except Exception as e:
    print(f"Erreur pour l'OID 1.3.6.1.2.1.4.24.3.0 : {e}")

# Exemple avec un chemin symbolique
try:
    obj_lab = ObjectIdentity("iso.org.dod.internet.mgmt.mib-2.system.sysUpTime.0")
    obj_lab.resolve_with_mib(mibViewController)
    pretty_name = ".".join(map(str, obj_lab.get_label()))
    print(obj_lab.get_oid())
    print(pretty_name)
except Exception as e:
    print(f"Erreur pour sysUpTime : {e}")
