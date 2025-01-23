from pysnmp.smi import builder, view, compiler
from pysnmp.smi.rfc1902 import ObjectIdentity
import os
import sys
import requests

# # Créer un dossier pour les MIBs s'il n'existe pas
mib_dir = os.path.expanduser('~/PySNMP Configuration/mibs')
os.makedirs(mib_dir, exist_ok=True)

# Liste des MIBs à télécharger
mib_files = [
    'POWER-ETHERNET-MIB',
    'SNMPv2-SMI',
    'SNMPv2-TC',
    'SNMPv2-CONF',
    'SNMP-FRAMEWORK-MIB'
]

# # Télécharger les MIBs
# base_url = 'https://raw.githubusercontent.com/cisco/cisco-mibs/main/v2/'
# for mib in mib_files:
#     mib_file = f"{mib}.my"
#     mib_path = os.path.join(mib_dir, mib_file)
    
#     if not os.path.exists(mib_path):
#         try:
#             print(f"Téléchargement de {mib_file}...")
#             response = requests.get(f"{base_url}{mib_file}")
#             if response.status_code == 200:
#                 with open(mib_path, 'w') as f:
#                     f.write(response.text)
#                 print(f"MIB {mib_file} téléchargée avec succès")
#             else:
#                 print(f"Erreur lors du téléchargement de {mib_file}")
#         except Exception as e:
#             print(f"Erreur: {str(e)}")

# Configuration de PySNMP
mibBuilder = builder.MibBuilder()

# Ajouter le dossier local des MIBs
mibBuilder.add_mib_sources(builder.DirMibSource(mib_dir))

# Charger les MIBs
for mib in mib_files:
    try:
        mibBuilder.load_modules(mib)
        print(f"MIB {mib} chargée avec succès")
    except Exception as e:
        print(f"Erreur lors du chargement de {mib}: {str(e)}")

mibViewController = view.MibViewController(mibBuilder)

# Test des OIDs
test_oids = [
    ('1.3.6.1.2.1.105.1', 'pethObjects'),
    ('POWER-ETHERNET-MIB', 'pethPsePortTable'),
    ('POWER-ETHERNET-MIB', 'pethMainPseTable')
]

for mib, obj in test_oids:
    try:
        test_object = ObjectIdentity(mib, obj)
        test_object.resolve_with_mib(mibViewController, False)
        print(f"\nTest pour {mib}::{obj}")
        print(f"OID: {test_object.get_oid()}")
        print(f"Label: {test_object.get_label()}")
    except Exception as e:
        print(f"\nErreur pour {mib}::{obj}: {str(e)}")

sys.exit(0)