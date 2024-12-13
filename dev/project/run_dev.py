import logging.config
import os
import sys
from dotenv import load_dotenv
import yaml
import inspect

# Librairies personnalisées
from dev.project.src.cl_short import SQLServer
from dev.project.core.db_def_prod import *
from dev.project.core.generate_deviceType_default import generateDeviceTypeDefault
from dev.project.src.classes.cl_mainGUI import MainGUI


# Variables d'environnement
VAR_GLOBAL_ENV = ".env"
VAR_RUN_ENV = os.path.join("dev",".env.dev")

# Chargement des ressources de l'application via git
def load_resources():
    git_repository = [
        "https://github.com/ecceman/affinity.git",
        "https://github.com/trevoro/snmp-mibs.git"
    ]
    # Check if the assets directory exists
    if not os.path.exists("assets/"):
        os.mkdir("assets/")

    for repo in git_repository:
        repo_name = repo.split('/')[-1].replace('.git', '')
        if os.path.exists(f"assets/{repo_name}"):
            logging.info(f"{inspect.currentframe().f_code.co_name}:Repository {repo_name} already cloned.")
        else:
            # placement du répertoire de ressources 'asssets' dans le répertoire de l'application
            os.system(f"git clone {repo} assets/")
            

# Load the environment variables
def load_env_vars():
    load_dotenv(VAR_GLOBAL_ENV)
    load_dotenv(VAR_RUN_ENV, override=True)
    load_dotenv(os.getenv("SQL_CONF"))


# Load and configure logs
def configure_logs():
    with open(os.getenv("APP_CONF_LOG"), "r") as file:
        log_config = yaml.safe_load(file)

    # Remplacer les placeholders dans la configuration par des valeurs d'environnement
    for handler_name, handler_config in log_config.get("handlers", {}).items():
        if "filename" in handler_config:
            handler_config["filename"] = os.getenv("APP_LOG")
        if "level" in handler_config:
            handler_config["level"] = os.getenv("LOG_LEVEL", "DEBUG").upper()

    # Appliquer la configuration des logs
    logging.config.dictConfig(log_config)


# Load the SQL Server
def load_sql_server():
    sqlServer = SQLServer(
        host=os.getenv("MARIADB_HOST"),
        database=os.getenv("MARIADB_DATABASE"),
        user=os.getenv("MARIADB_USER"),
        password=os.getenv("MARIADB_PASSWORD")
    )
    sqlServer.connect()

    # Check Users Table
    if getAllUsers(sqlServer):
        logging.info(f"{inspect.currentframe().f_code.co_name}:Users table is not empty")
    else:
        logging.error(f"{inspect.currentframe().f_code.co_name}:ERROR: Users table is empty")
        # CREATE Default Users
        id_root = createUser(sqlServer, "root", "root@localhost", "Root846")
        id_admin = createUser(sqlServer, "admin", "admin@localhost", "Admin813+")
        id_user = createUser(sqlServer, "user", "user@localhost", "User792-")

        # Add Roles to Default Users
        addRoleToUser(sqlServer, id_root, 1)
        addRoleToUser(sqlServer, id_admin, 2)
        addRoleToUser(sqlServer, id_user, 3)

    # Check OSILayer Table
    if len(getAllOSILayers(sqlServer)) != 7:
        logging.error(f"{inspect.currentframe().f_code.co_name}:ERROR: OSI Layers table is not complete")
    else:
        logging.info(f"{inspect.currentframe().f_code.co_name}:OSI Layers table is complete")
    
    # Check DeviceType Table
    if getAllDeviceTypes(sqlServer):
        logging.info(f"{inspect.currentframe().f_code.co_name}: Device Types table is not empty")
    else:
        logging.error(f"{inspect.currentframe().f_code.co_name}: ERROR: Device Types table is empty")
        logging.info(f"{inspect.currentframe().f_code.co_name}: Generate default Device Types")

        # CREATE Default Device Types
        logging.debug(f"{inspect.currentframe().f_code.co_name}: {os.getenv("DEVICETYPE_FILE_RSC")}")
        generateDeviceTypeDefault(sqlServer, os.getenv("DEVICETYPE_FILE_RSC"))
    
    # Check Language Table
    sqlServer.disconnect()

# Load the application GUI
def load_app():
    logging.info(f"{inspect.currentframe().f_code.co_name}: Chargement de l'interface graphique.")
    logging.info(f"{inspect.currentframe().f_code.co_name}: {os.getenv('APP_NAME')} démarrée.")

    from qtpy.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)
    app.setApplicationName(os.getenv("APP_NAME"))
    app.setOrganizationName(os.getenv("APP_ORGANIZATION"))
    app.setApplicationVersion(os.getenv("APP_VERSION"))
    # app.setStyle("Fusion")

    mainGUI = MainGUI()
    mainGUI.show()

    sys.exit(app.exec_())


def dev_main():
    load_env_vars()
    configure_logs()

    # Exemple de journalisation
    logger = logging.getLogger("app_logger")
    logger.info("Application démarrée.")
    logger.debug("Mode débogage activé.")
    logger.warning("Attention, ceci est un avertissement.")

    load_sql_server()
    load_app()