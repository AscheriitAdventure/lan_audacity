from pysmi.reader.localfile import FileReader
from pysmi.parser.smi import parserFactory
from pysmi.writer.callback import CallbackWriter
from pysmi.compiler import MibCompiler
from pysmi import debug
from pysmi.error import PySmiError
import os

# Chemin vers le fichier MIB
mib_file_path = "file://D:/lan_audacity/assets/snmp-mibs/mibs/RFC1213-MIB.mib"

# Fonction pour valider un fichier MIB
def validate_mib(file_path):
    try:
        # Activer les logs de débogage (facultatif)
        debug.set_logger(debug.Debug('reader', 'parser'))

        # Initialiser les composants PySMI
        reader = FileReader(os.path.dirname(file_path))
        parser = parserFactory()  # Usine pour récupérer le bon parser ASN.1

        # Writer de callback pour capturer les résultats sans écrire sur disque
        def write_callback(mib_name, processed_mib):
            print(f"MIB traitée: {mib_name}")
            print(f"Résultat: {processed_mib}")
        writer = CallbackWriter(write_callback)

        # Configurer le compilateur de MIB
        compiler = MibCompiler(parser, reader, writer)

        # Nom de la MIB à partir du chemin de fichier
        mib_name = os.path.basename(file_path)#.replace('.mib', '')

        # Lancer la validation
        results = compiler.compile(mib_name, rebuild=True, genTexts=True)

        # Vérifier les résultats
        if mib_name not in results or results[mib_name] != 'compiled':
            print(f"Validation échouée pour le fichier: {file_path}")
            if mib_name in results:
                print(str(results))
                print(f"Erreur: {mib_name} {results[mib_name]}")
            else:
                print("Aucune information d'erreur détaillée disponible.")
        else:
            print(f"Le fichier MIB '{mib_name}' est valide !")

    except PySmiError as e:
        print(f"Erreur lors de la validation du fichier MIB: {e}")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite: {e}")

# Valider le fichier MIB spécifié
validate_mib(mib_file_path)



# Initialize compiler infrastructure
""" 
mibdump --mib-source file://D:/lan_audacity/assets/snmp-mibs/mibs --destination-format pysnmp --destination-directory file://D:/lan_audacity/backup/dev/py_mibs --ignore-errors RFC1213-MIB
"""