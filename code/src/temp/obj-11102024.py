import os
from dotenv import load_dotenv
from src.classes.cl_app_sys import MariaDB_Docker

load_dotenv()

# Connexion à la bdd mariadb
mariadb = MariaDB_Docker(
    root_password=os.getenv("MARIADB_ROOT_PASSWORD"),
    database=os.getenv("MARIADB_DATABASE"),
    user=os.getenv("MARIADB_USER"),
    password=os.getenv("MARIADB_PASSWORD"),
    port=os.getenv("MARIADB_PORT"))

# Création de la requête
request = """"""
# Création des valeurs à Insérer
values = ()
mariadb
