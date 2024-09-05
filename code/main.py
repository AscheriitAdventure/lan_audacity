import logging
import logging.config
import sys
import os

from src.functionsExt import current_dir
from src.classes.mainApp import MainApp
from src.classes.configurationFile import ConfigurationFile

if __name__ == "__main__":
    softwareManager = ConfigurationFile(os.path.join(current_dir(), "conf", "config_app.yaml"))
    
    pathLog = os.path.join(current_dir(), softwareManager.data["software"]["conf"]["log_app"]["path"])

    logs_manager = ConfigurationFile(pathLog)

    logging.config.dictConfig(logs_manager.data)
    logger = logging.getLogger(__name__)

    logger.info(
        f"{softwareManager.data['system']['name']} - version {softwareManager.data['system']['version']}"
    )

    from qtpy.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setApplicationName(softwareManager.data["system"]["name"])
    app.setApplicationVersion(softwareManager.data["system"]["version"])
    app.setOrganizationName(softwareManager.data["system"]["organization"])

    main_window = MainApp(softwareManager)
    main_window.show()

    sys.exit(app.exec_())
