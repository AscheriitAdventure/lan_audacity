from dataclass import *
from sql_server import *

# Insérer l'adresse réseau inspectée au format CIDR
VAR_CIDR = ""

# Insérer le format de sortie de traitement des données
VAR_FORMAT = "" # "json", "csv", "xml", "terminal"

# [Optionnel] Insérer le chemin du fichier de sortie
VAR_OUTPUT_FILE = ""

# [Optionnel] Insérer le chemin du fichier de configuration
VAR_CONFIG_FILE = ""

# Connection à la base de données Docker
