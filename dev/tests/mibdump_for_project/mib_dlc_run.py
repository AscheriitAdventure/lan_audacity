"""
    Ce module permet de charger les MIBs nécessaire pour traduire les OIDs récupérer avec snmpwalk.

    Donc en entrée, on a un fichier de configuration de type JSON qui contient les informations suivantes:
    [
        {
            "uuidLink": "Suite de caractères alphanumériques déterminant l'identifiant unique de l'extension réutilisable dans 'packageLinkExtension'",
            "nameObject": "Nom de l'extension",
            "versionObject": "Version de l'extension",
            "newsUpdate": "Journal des modifications vers un fichier CHANGELOG",
            "readMeObject": "Description de l'extension ou chemin vers un fichier README",
            "vendor": "Nom du constructeur",
            "nameAuthors": ["Nom de l'auteur", "Nom de l'auteur", ...],
            "keyWords": ["MIB", "OID", "SNMP"],
            "packageLinkExtension": ["Lien vers une extension", "Lien vers une autre extension", ...],
            "categoryExtension": ["Catégorie de l'extension", "Catégorie de l'extension", ...],
            "cerficateObject": ["Chemin vers un certificat", "Chemin vers un certificat", ...],
            "pathObject": {
                "pathIcon": "Chemin vers une icône",
                "pathUrlLocal": "chemin vers le dossier local",
                "pathUrlWeb": ["chemin vers le serveur web", "chemin vers le serveur web", ...],
                "pathUrlGit": ["chemin vers le dépôt Git", "chemin vers le dépôt Git", ...]

            }
        }
    ]
    En étape: 
        récupérer le dlc si il existe, "sinon le télécharger" si c'est possible
        récupérer le fichier de configuration dans le dossier local
        lire le fichier de configuration
        récupérer la variable qui a pour nom "MIB_NAME_REF_LIST"
        Décomposer la variable en liste de nom de MIB

        Récupérer via la variable d'environnement le chemin vers le dossier contenant les MIBs en '.mib' ou '.my'
        Récupérer via la variable d'environnement le chemin vers le dossier contenant les MIBs en  '.py'

        Exécuter le script de conversion des MIBs en '.py'

        Supprimer dans le pysnmp/smi/mibs/ tous les fichiers qui ont le même nom que les MIBs
        qui se trouve dans le fichier des MIBs en '.py' puis copier les fichiers '.py' dans le dossier pysnmp/smi/mibs/

        garder en mémoire la liste des nom de MIB pour les utiliser dans le script de traduction des OIDs

"""

import os
import csv
import logging


# Chemins de fichiers et dossiers
LIST_MIB_NAME_CSV = r"D:/lan_audacity/dev/tests/mibdump_for_project/mib-compile-pysnmp.csv"
ORIGIN_MIB_MIB = r"D:/lan_audacity/assets/snmp-mibs/mibs/"
ORIGIN_MIB_PY = r"D:/lan_audacity/assets/snmp-mibs/mibs-py/"


# Ouverture du fichier CSV
with open(LIST_MIB_NAME_CSV, 'r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # Lecture des lignes du fichier CSV
    for row in csv_reader:
        # exemple de print {'TXT-NAME': 'TN3270E-MIB'}
        shell_query = f"mibdump.exe --mib-source=file:///{ORIGIN_MIB_MIB} --destination-directory={ORIGIN_MIB_PY} --destination-format=pysnmp --rebuild {row['TXT-NAME']}"
        logging.debug(shell_query)
        os.system(shell_query)

# ok ce programme fonctionne parfaitement
