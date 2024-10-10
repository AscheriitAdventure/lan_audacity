import os
import logging
import platform

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
