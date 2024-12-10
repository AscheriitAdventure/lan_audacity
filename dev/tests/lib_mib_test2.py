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
        mibBuilder.loadModules(mib_name)
        logging.info(f"MIB {mib_name} compilée avec succès.")
        return True
    except Exception as e:
        logging.error(f"Erreur lors de la compilation de la MIB {mib_name} : {e}")
        return False

# Fonction pour résoudre un OID
def resolve_oid(oid: Any) -> None:
    obj_lab = ObjectIdentity(oid)
    obj_lab.resolve_with_mib(mibViewController)
    
    if len(obj_lab.get_label()) == 9:
        pretty_name = ".".join(map(str, obj_lab.get_label()))
        print(f"OID : {obj_lab.get_oid()}")
        print(f"Nom symbolique : {pretty_name}")

    else:
        # Récupère le nom de la mib
        mib_name, symbol_name, oid_tail = obj_lab.get_mib_symbol()
        logging.info(f"Résolution de l'OID {oid} avec la MIB {mib_name}")
        logging.info(f"Nom symbolique : {symbol_name}")
        logging.info(f"OID : {oid_tail}")

# Exemple d'utilisation
if __name__ == "__main__":
    test_oid = '1.3.6.1.2.1.4.24.3.0'  # Exemple d'OID
    resolve_oid(test_oid)


"""
Résultat:
2024-12-10 15:45:12,745 - INFO - Résolution de l'OID 1.3.6.1.2.1.4.24.3.0 avec la MIB ('SNMPv2-SMI', 'mib-2', (<ObjectName value object, tagSet <TagSet object, tags 0:0:6>, payload [4.24.3.0]>,))
"""