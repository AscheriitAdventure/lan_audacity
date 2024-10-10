import os
import logging
import platform
from dotenv import load_dotenv

# Charger les variables d'environnement du fichier `.env`
load_dotenv()

# Configurer le niveau de logging
logging.basicConfig(level=logging.INFO)

# Liste des logiciels à vérifier
software_list = ['nmap', 'docker', 'python']

# Déterminer la commande à utiliser en fonction du système d'exploitation
if platform.system() in ['Linux', 'Darwin']:
    command = 'which'
elif platform.system() == 'Windows':
    command = 'where'
else:
    logging.warning("Unsupported operating system.")
    exit()

for software in software_list:
    # Utiliser 'which' pour vérifier la présence du logiciel
    result = os.system(f"{command} {software} > /dev/null 2>&1")
    if result == 0:
        logging.info(f"{software} is installed.")
    else:
        logging.warning(f"{software} is not installed.")


# Récupérer les informations de l'utilisateur de session
user_info = {
    'username': os.getlogin(),
    'home_directory': os.path.expanduser('~'),
    'current_directory': os.getcwd()
}

print("\nUser information:")
for key, value in user_info.items():
    print(f"{key}: {value}")

# test
print(os.getenv("MARIADB_USER"))

