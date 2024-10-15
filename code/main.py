from src.classes.cl_app_sys import OsSys, MariaDB_Docker, MongoDB_Docker
import platform
import sys
import logging
import os
from dotenv import load_dotenv

# Charger les variables d'environnement du fichier `.env`
load_dotenv()

# Créer une instance de la classe OsSys
os_sys = OsSys(platform.system(), platform.version())

# Exécuter le système d'exploitation
if os_sys.exec_os():
    # Exécuter le scan des logiciels
    if os_sys.exec_software() > 0:
        logging.warning("Some software is missing.")
        sys.exit(1)
    else:
        # Lancer le fichier docker-compose
        result = os.system("docker-compose ps")
        # Vérifier si le docker-compose n'est pas déjà lancé
        if result != 0:
            os.system("docker-compose build")
            os.system("docker-compose up -d")
        else:
            os.system("docker-compose up -d")
            logging.info("Docker-compose is already running.")

        # Déverrouiller le conteneur MariaDB avec le fichier `.env`
        mariadb_docker = MariaDB_Docker(
            root_password=os.getenv("MARIADB_ROOT_PASSWORD"),
            database=os.getenv("MARIADB_DATABASE"),
            user=os.getenv("MARIADB_USER"),
            password=os.getenv("MARIADB_PASSWORD"),
            port=int(os.getenv("MARIADB_PORT")),
        )

        # Déverrouiller le conteneur MongoDB avec le fichier `.env`
        mongodb_docker = MongoDB_Docker(
            user=os.getenv("MONGODB_USER"),
            password=os.getenv("MONGODB_PASSWORD"),
            port=int(os.getenv("MONGODB_PORT")),
        )

else:
    logging.info("Operating system not supported.")
    sys.exit(1)
