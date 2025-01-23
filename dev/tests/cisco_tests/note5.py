import pandas as pd
import os

from pysnmp.smi import builder, view, compiler
from pysnmp.smi.rfc1902 import ObjectIdentity

CSV_PATH = 'D:/lan_audacity/dev/tests/cisco_tests/snmp_data.csv'
START_OID = "1.3.6.1.2.1"  # Filtrer à partir de mib-2
VAR_SRC_MIBS = 'D:/lan_audacity/backup/dev/py_mibs'

# Charger les fichiers MIB
mibBuilder = builder.MibBuilder()
mibBuilder.add_mib_sources(builder.DirMibSource(VAR_SRC_MIBS))
compiler.add_mib_compiler(mibBuilder, sources=[
                          'http://mibs.snmplabs.com/asn1/@mib@',])

mib_list = ['POWER-ETHERNET-MIB','IP-MIB', 'IP-FORWARD-MIB', 'IF-MIB', 'DISMAN-EXPRESSION-MIB',
    'DISMAN-EVENT-MIB', 'RFC1213-MIB', 'EtherLike-MIB', 'RMON-MIB', 'RMON2-MIB',
    'SMON-MIB', 'BRIDGE-MIB',  'HC-RMON-MIB', 'UPS-MIB'
]
# 'POWER-ETHERNET-MIB', 'CISCO-SMI'
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
    
    # Créer un nouveau DataFrame en préservant les colonnes existantes
    result_df = pd.DataFrame({'OID': sorted(list(all_oids))})
    # Fusionner avec le DataFrame original pour garder les données existantes
    result_df = pd.merge(result_df, filtered_df, on='OID', how='left')
    
    # Ajouter les nouvelles colonnes
    result_df['TXT-END'] = ''
    result_df['DSC'] = ''
    
    # Dictionnaire pour vérifier l'unicité des valeurs de TXT-END
    seen_txt_ends = set()

    # Remplir les colonnes TXT-END et DSC
    for idx, row in result_df.iterrows():
        try:
            oid = ObjectIdentity(row['OID'])
            oid.resolve_with_mib(mibViewController)
            txt_end = oid.get_label()[-1]
            
            # Vérifier si TXT-END est déjà utilisé
            if txt_end in seen_txt_ends:
                txt_end = "#N/A"
            else:
                seen_txt_ends.add(txt_end)
            
            result_df.at[idx, 'TXT-END'] = txt_end
            result_df.at[idx, 'DSC'] = '.'.join(map(str, oid.get_label()))
        except Exception:
            result_df.at[idx, 'TXT-END'] = "#N/A"  # Marquer comme indisponible si résolution échoue
            continue
    
    # Ajouter dans la colonne Value le mot TABLE si Value et vide ainsi que TXT-END contient la suite de caractères "table" ou "Table" ou "TABLE"
    result_df['Value'] = result_df['Value'].fillna('')
    result_df['Value'] = result_df.apply(lambda row: 'TABLE' if row['Value'] == '' and 'table' in row['TXT-END'].lower() else row['Value'], axis=1)
    
    return result_df.sort_values('OID')

if __name__ == '__main__':
    data = load_csv_data()
    print(data)
    data.to_csv('D:/lan_audacity/dev/tests/cisco_tests/snmp_data_filtered.csv', index=False)