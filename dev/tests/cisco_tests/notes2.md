# Nouvelle vue

il faut que j'arrive à passer de :

| OID             | TXT-END  | DSC                                             |
|:----------------|:---------|:------------------------------------------------|
| 1.3.6.1.2.1     |          |                                                 |
| 1.3.6.1.2.1.1   |          |                                                 |
| 1.3.6.1.2.1.1.1 | sysDescr | iso.org.dod.internet.mgmt.mib-2.system.sysDescr |

à

| OID             | DSC                                             | TXT-END  |
|:----------------|:------------------------------------------------|:---------|
| 1.3.6.1.2.1     | iso.org.dod.internet.mgmt.mib-2                 | mib-2    |
| 1.3.6.1.2.1.1   | iso.org.dod.internet.mgmt.mib-2.system          | system   |
| 1.3.6.1.2.1.1.1 | iso.org.dod.internet.mgmt.mib-2.system.sysDescr | sysDescr |

avec un csv qui a pour en-tête: OID, Data Type, Value
Extrait:

```csv
OID,Data Type,Value
1.3.6.1.2.1.1.2.0,ObjectIdentifier,1.3.6.1.4.1.9.1.503
1.3.6.1.2.1.1.3.0,TimeTicks,1687290511
1.3.6.1.2.1.1.4.0,OctetString,Artefact <noc@artewan.net>
1.3.6.1.2.1.1.5.0,OctetString,Cisco-4500-Eyrein-1
1.3.6.1.2.1.1.6.0,OctetString,Eyrein
1.3.6.1.2.1.1.7.0,Integer,6
1.3.6.1.2.1.1.8.0,TimeTicks,0
```

Réflexion :
Donc en premier lieu créer l'arborescence, pour avoir un tableau (certes vide mais avec de nouveaux en-têtes et de nouvelles lignes ainsi qu'un filtrage ordonné)
En un second temps remplir les cases vides.
Enfin lire le fichier csv et afficher l'arborescence (colonne TXT-END) avec qtpy.

```python
import pandas as pd
import os

from pysnmp.smi import builder, view, compiler
from pysnmp.smi.rfc1902 import ObjectIdentity

CSV_PATH = 'D:/lan_audacity/dev/tests/cisco_tests/snmp_data.csv'
MIB_PATH = 'D:/lan_audacity/backup/dev/py_mibs'
START_OID = "1.3.6.1.2"  # Filtrer à partir de mib-2

mibBuilder = builder.MibBuilder()
mibBuilder.add_mib_sources(builder.DirMibSource(MIB_PATH))
compiler.add_mib_compiler(mibBuilder, sources=['http://mibs.snmplabs.com/asn1/@mib@', f'file://{MIB_PATH}'])

mib_list = [
    'SNMPv2-MIB', 'IP-MIB', 'IP-FORWARD-MIB', 'IF-MIB', 'DISMAN-EXPRESSION-MIB',
    'DISMAN-EVENT-MIB', 'RFC1213-MIB', 'EtherLike-MIB', 'RMON-MIB', 'RMON2-MIB',
    'SMON-MIB', 'BRIDGE-MIB', 'POWER-ETHERNET-MIB'
]
for mib in mib_list:
    try:
        mibBuilder.load_modules(mib)
    except Exception as e:
        print(f"⚠️ Erreur lors du chargement du module {mib} : {e}")

mibViewController = view.MibViewController(mibBuilder)

def load_csv_data():
    """ Charge les OID depuis un fichier CSV et affiche ceux à partir de mib-2 """

    df = pd.read_csv(CSV_PATH, dtype=str)
    # Filtrer les OID qui commencent par START_OID
    filtered_df = df[df['OID'].str.startswith(START_OID)]
    
    # Créer un DataFrame avec tous les OID parents possibles
    all_oids = set()
    for oid in filtered_df['OID']:
        parts = oid.split('.')
        for i in range(len(parts)):
            all_oids.add('.'.join(parts[:i+1]))
    
    # Créer un nouveau DataFrame avec les colonnes requises
    result_df = pd.DataFrame({'OID': sorted(list(all_oids))})
    result_df['TXT-END'] = ''
    result_df['DSC'] = ''
    
    # Remplir les colonnes TXT-END et DSC
    for idx, row in result_df.iterrows():
        try:
            oid = ObjectIdentity(row['OID']).resolveWithMib(mibViewController)
            labels = [x[0] for x in oid.getMibNode().getName()]
            result_df.at[idx, 'TXT-END'] = labels[-1]
            result_df.at[idx, 'DSC'] = '.'.join(labels)
        except Exception:
            continue
    
    return result_df.sort_values('OID')
```
