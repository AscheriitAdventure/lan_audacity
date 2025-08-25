# Librairy: core_program/:--:\python
from src.classes.configurationFile import ConfigurationFile
# Librairy: core_program/:--:\sql server
from src.core.sql_server import MySQLConnection as SQLServer
from src.core.db_def_prod import *


# Librairy: pip
import logging.config
from typing import List, Optional, Any


# Variables Globales
VAR_CONFIG_SQL_SERVER = "C:\\Users\\g.tronche\\Documents\\GitHub\\lan_audacity\\code\\conf\\config_db.yaml"
VAR_CONFIG_LOGS = "C:\\Users\\g.tronche\\Documents\\GitHub\\lan_audacity\\code\\conf\\config_logs.yaml"


# Lancement de la configuration des logs
logsManager = ConfigurationFile(VAR_CONFIG_LOGS)
# logging.config.dictConfig(logsManager.data)
logger = logging.getLogger(__name__)

# Lancement de la configuration de la base de données
configManager = ConfigurationFile(VAR_CONFIG_SQL_SERVER)
bdd = configManager.data["database"]
sqlServer = SQLServer(
    host=bdd["host"], 
    database=bdd["dbname"], 
    user=bdd["username"], 
    password=bdd["password"])
sqlServer.connect()

# Vérification du contenu de la base de données
if getAllUsers(sqlServer):
    print(getAllUsers(sqlServer))
    logger.info("Users table is not empty")
else:
    logger.info("Users table is empty")
    # Création des utilisateurs
    id_root = createUser(sqlServer, "root", "root@localhost", "Root846")
    id_admin = createUser(sqlServer, "admin", "admin@localhost", "Admin813+")
    id_user = createUser(sqlServer, "user", "user@localhost", "User792-")

    # Création des rôles
    addRoleToUser(sqlServer, id_root, 1)
    addRoleToUser(sqlServer, id_admin, 2)
    addRoleToUser(sqlServer, id_user, 3)

if len(getAllOSILayers(sqlServer)) != 7:
    logger.error("ERROR: OSI Layers table is not complete")
else:
    logger.info("OSI Layers table is complete")


