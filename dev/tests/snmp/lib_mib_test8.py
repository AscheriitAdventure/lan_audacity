from pysnmp.smi import builder, view, compiler
from pysnmp.smi.rfc1902 import ObjectIdentity
from pysmi.reader.localfile import FileReader
from pysmi.parser.smi import parserFactory
from pysmi.writer.callback import CallbackWriter
from pysmi.compiler import MibCompiler
import logging
import os
from typing import Optional

from pysmi.codegen.symtable import SymtableCodeGen

# Configuration de la journalisation
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

VAR_SRC_MIBS = 'file://D:/lan_audacity/assets/snmp-mibs/mibs'
MIB_SRC_PATH = 'D:/lan_audacity/assets/snmp-mibs/mibs'

# Charger les fichiers MIB
mibBuilder = builder.MibBuilder()
#compiler.add_mib_compiler(mibBuilder, sources=['http://mibs.snmplabs.com/asn1/@mib@', VAR_SRC_MIBS])
compiler.add_mib_compiler(mibBuilder, sources=[VAR_SRC_MIBS])

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

def load_mib(mib):
    try:
        mibBuilder.load_modules(mib)
    except Exception as e:
        logging.error(f"Erreur lors du chargement du module {mib}\n")
        logging.error(e)

def find_mib_file(mib_name: str) -> Optional[str]:
        for root, _, files in os.walk(MIB_SRC_PATH):
            for file in files:
                if file.lower() == f"{mib_name.lower()}.mib":
                    logging.info(f"Fichier MIB trouvé : {file}")
                    return os.path.join(root, file)
        return None

def main():
    for mib in mib_list:
        load_mib(mib)

    # Construire un traducteur
    mibViewController = view.MibViewController(mibBuilder)
    # Check if the MIB file is found
    for mib in mib_list:
        try:
            mib_file = find_mib_file(mib)
            if mib_file is None:
                logging.error(f"Fichier MIB non trouvé : {mib}")
        except Exception as e:
            logging.error(f"Erreur lors de la recherche de la MIB {mib} : {e}")
            break
    
    # Initialiser les composants PySMI
    codeGen = ''
    parser = parserFactory()  # Usine pour récupérer le bon parser ASN.1
    writer = CallbackWriter(lambda m, s: logging.info(s))
    for mib in mib_list:
        compiler = MibCompiler(parser=parser, codegen=codeGen, writer=writer)
        result = compiler.compile(mib)
        logging.info(result)




    


main()
