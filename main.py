from src.utils import *
import os
import sys

from src.views import MainGUI

if __name__ == "__main__":
    tmpd: dict = {"app_path": os.getcwd(), "debug": False}
    scan_app = ScanApp(**tmpd)

    load_env_vars()
    configure_logs()

    logger = get_logger(__name__)
    logger.info("Application en cours de démarrage...")

    from qtpy.QtWidgets import QApplication

    log_function_call("Démarrage de l'interface graphique")
    app = QApplication(sys.argv)
    app.setApplicationName(get_app_name())
    app.setOrganizationName(get_app_organization())
    app.setApplicationVersion(get_app_version())

    mainWindow = MainGUI()
    mainWindow.show()
    sys.exit(app.exec_())
