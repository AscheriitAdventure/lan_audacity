from pysnmp.smi import builder, view, compiler
from pysnmp.smi.rfc1902 import ObjectIdentity
import sys

VAR_SRC_MIBS = 'D:/lan_audacity/assets/snmp-mibs/mibs'

# Charger les fichiers MIB
mibBuilder = builder.MibBuilder()
mibBuilder.add_mib_sources(builder.DirMibSource(VAR_SRC_MIBS))
compiler.add_mib_compiler(mibBuilder, sources=[
    'http://mibs.snmplabs.com/asn1/@mib@',
])

# Liste des MIBs à charger
mib_list = ['SNMPv2-MIB', 'SNMPv2-SMI', 'SNMPv2-TC', 'POWER-ETHERNET-MIB', 'IF-MIB', 'PETH-MIB']
for mib in mib_list:
    mibBuilder.load_modules(mib)

# Construire un traducteur MIB
mibViewController = view.MibViewController(mibBuilder)

# Objets de test
test_objects = [
    ('PETH-MIB', 'pethObjects'),
    ('POWER-ETHERNET-MIB', 'pethObjects'),
]

# Résolution des objets
for mib, obj in test_objects:
    try:
        a = ObjectIdentity(mib, obj)
        a.resolve_with_mib(mibViewController, False)
        print(f"{mib}.{obj}")
        print(f"OID: {a.get_oid()}")
        print(f"Label: {a.get_label()}\n")
    except Exception as e:
        print(f"Erreur pour {mib}.{obj}: {str(e)}")

sys.exit(0)
