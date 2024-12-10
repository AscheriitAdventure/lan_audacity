import os
import logging
from urllib.parse import urljoin
from urllib.request import pathname2url
from typing import Optional, Any
from pysnmp.smi import builder, view, compiler
from pysnmp.smi.rfc1902 import ObjectIdentity

# Configuration des chemins
MIB_SRC_PATH = 'D:\\lan_audacity\\assets\\snmp-mibs\\mibs'
MIB_SRC_URL = 'http://mibs.snmplabs.com/asn1/@mib@'
MIB_COMPILED_PATH = 'D:\\lan_audacity\\backup\\dev\\py_mibs'

# Convertir le chemin local des MIB compilées en URL compatible
MIB_COMPILED_URL = urljoin('file:', pathname2url(MIB_COMPILED_PATH))

# Configuration de la journalisation
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuration du MIB Builder
mibBuilder = builder.MibBuilder()
compiler.add_mib_compiler(
    mibBuilder,
    sources=[MIB_COMPILED_URL, MIB_SRC_URL]
)
mibViewController = view.MibViewController(mibBuilder)

# Fonction pour rechercher et compiler une MIB
def fetch_and_compile_mib(mib_name: str) -> bool:
    def find_mib_file(mib_name: str) -> Optional[str]:
        for root, _, files in os.walk(MIB_SRC_PATH):
            for file in files:
                if file.lower() == f"{mib_name.lower()}.mib":
                    logging.info(f"Fichier MIB trouvé : {file}")
                    return os.path.join(root, file)
        return None

    logging.debug(f"Récupération et compilation de la MIB : {mib_name}")

    # Recherche du fichier MIB brut
    mib_file = find_mib_file(mib_name)
    if not mib_file:
        logging.error(f"Fichier MIB non trouvé : {mib_name}")
        return False

    # Chemin du fichier compilé
    compiled_mib_path = os.path.join(MIB_COMPILED_PATH, f"{mib_name}.py")

    # Vérifier si le fichier MIB compilé existe déjà
    if os.path.exists(compiled_mib_path):
        logging.info(f"Fichier MIB compilé déjà présent : {compiled_mib_path}")
        return True

    # Compiler la MIB
    try:
        logging.info(f"Compilation du fichier MIB : {mib_file}")
        compiler.MibCompiler.compile(mib_name, mib_file, compiled_mib_path)
        logging.info(f"MIB {mib_name} compilée avec succès.")
        return True
    except Exception as e:
        logging.error(f"Erreur lors de la compilation de la MIB {mib_name} : {e}")
        return False

mib_list = [
    'IP-MIB',
    'IP-FORWARD-MIB',
    'IF-MIB',
    'DISMAN-EXPRESSION-MIB',
    'DISMAN-EVENT-MIB',
    'EXPRESSION-MIB',
]

for mib in mib_list:
    fetch_and_compile_mib(mib)

print("Compilation des MIB terminée.")

""" 
OUTPUT:
2024-12-10 16:10:11,372 - DEBUG - Récupération et compilation de la MIB : IP-MIB
2024-12-10 16:10:11,398 - INFO - Fichier MIB trouvé : IP-MIB.mib
2024-12-10 16:10:11,398 - INFO - Compilation du fichier MIB : D:\lan_audacity\assets\snmp-mibs\mibs\IP-MIB.mib
2024-12-10 16:10:11,398 - ERROR - Erreur lors de la compilation de la MIB IP-MIB : 'str' object has no attribute '_sources'
2024-12-10 16:10:11,398 - DEBUG - Récupération et compilation de la MIB : IP-FORWARD-MIB
2024-12-10 16:10:11,422 - INFO - Fichier MIB trouvé : IP-FORWARD-MIB.mib
2024-12-10 16:10:11,422 - INFO - Compilation du fichier MIB : D:\lan_audacity\assets\snmp-mibs\mibs\IP-FORWARD-MIB.mib
2024-12-10 16:10:11,422 - ERROR - Erreur lors de la compilation de la MIB IP-FORWARD-MIB : 'str' object has no attribute '_sources'
2024-12-10 16:10:11,422 - DEBUG - Récupération et compilation de la MIB : IF-MIB
2024-12-10 16:10:11,449 - INFO - Fichier MIB trouvé : IF-MIB.mib
2024-12-10 16:10:11,449 - INFO - Compilation du fichier MIB : D:\lan_audacity\assets\snmp-mibs\mibs\IF-MIB.mib
2024-12-10 16:10:11,450 - ERROR - Erreur lors de la compilation de la MIB IF-MIB : 'str' object has no attribute '_sources'
2024-12-10 16:10:11,450 - DEBUG - Récupération et compilation de la MIB : DISMAN-EXPRESSION-MIB
2024-12-10 16:10:11,472 - INFO - Fichier MIB trouvé : DISMAN-EXPRESSION-MIB.mib
2024-12-10 16:10:11,473 - INFO - Compilation du fichier MIB : D:\lan_audacity\assets\snmp-mibs\mibs\DISMAN-EXPRESSION-MIB.mib
2024-12-10 16:10:11,474 - ERROR - Erreur lors de la compilation de la MIB DISMAN-EXPRESSION-MIB : 'str' object has no attribute '_sources'
2024-12-10 16:10:11,474 - DEBUG - Récupération et compilation de la MIB : DISMAN-EVENT-MIB
2024-12-10 16:10:11,497 - INFO - Fichier MIB trouvé : DISMAN-EVENT-MIB.mib
2024-12-10 16:10:11,499 - INFO - Compilation du fichier MIB : D:\lan_audacity\assets\snmp-mibs\mibs\DISMAN-EVENT-MIB.mib
2024-12-10 16:10:11,500 - ERROR - Erreur lors de la compilation de la MIB DISMAN-EVENT-MIB : 'str' object has no attribute '_sources'
2024-12-10 16:10:11,500 - DEBUG - Récupération et compilation de la MIB : EXPRESSION-MIB
2024-12-10 16:10:11,520 - INFO - Fichier MIB trouvé : EXPRESSION-MIB.mib
2024-12-10 16:10:11,520 - INFO - Compilation du fichier MIB : D:\lan_audacity\assets\snmp-mibs\mibs\EXPRESSION-MIB.mib
2024-12-10 16:10:11,520 - ERROR - Erreur lors de la compilation de la MIB EXPRESSION-MIB : 'str' object has no attribute '_sources'
Compilation des MIB terminée.
"""