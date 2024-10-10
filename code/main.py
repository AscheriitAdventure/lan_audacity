from src.classes.cl_app_sys import OsSys, MariaDB_Docker, MongoDB_Docker
import platform
import sys, logging, os
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
        os.system("docker-compose up -d")
        
        # Déverrouiller le conteneur MariaDB avec le fichier `.env`
        mariadb_docker = MariaDB_Docker()
        mariadb_username = os.getenv("MARIADB_USER")
        mariadb_password = os.getenv("MARIADB_PASSWORD")
        mariadb_database = os.getenv("MARIADB_DATABASE")
        
        if mariadb_username and mariadb_password and mariadb_database:
            if mariadb_docker.unlock_container(mariadb_username, mariadb_password, mariadb_database):
                logging.info("MariaDB container is successfully unlocked.")
            else:
                logging.error("Failed to unlock MariaDB container.")
                sys.exit(1)
        else:
            logging.error("Missing MariaDB credentials in `.env` file.")
            sys.exit(1)
        
        # Déverrouiller le conteneur MongoDB avec le fichier `.env`
        mongodb_docker = MongoDB_Docker()
        mongodb_username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        mongodb_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
        
        if mongodb_username and mongodb_password:
            if mongodb_docker.unlock_container(mongodb_username, mongodb_password):
                logging.info("MongoDB container is successfully unlocked.")
            else:
                logging.error("Failed to unlock MongoDB container.")
                sys.exit(1)
        else:
            logging.error("Missing MongoDB credentials in `.env` file.")
            sys.exit(1)
        
else:
    logging.info("Operating system not supported.")
    sys.exit(1)
