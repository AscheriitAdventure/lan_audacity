from src.models.conf_file import ConfigurationFile
import os
import sys
import logging
import logging.config
from qtpy.QtWidgets import QApplication


def current_dir():
    try:
        curr_path = os.getcwd()
        return curr_path
    except Exception as e:
        logging.error(
            f"Une erreur s'est produite lors de l'obtention du répertoire de travail actuel : {e}"
        )
        return "Analyse Erreur"


if __name__ == "__main__":
    softw_manager = ConfigurationFile(current_dir() + "/conf/config_app.yaml")
    path_log = f"{current_dir()}/{softw_manager.data['software']['configuration_logs']['path']}"
    logs_manager = ConfigurationFile(path_log)

    logging.config.dictConfig(logs_manager.data)
    logger = logging.getLogger(__name__)

    logger.info(f"{softw_manager.data['system']['name']} - version {softw_manager.data['system']['version']}")

    app = QApplication(sys.argv)
    app.setApplicationName(softw_manager.data['system']['name'])
    app.setApplicationVersion(softw_manager.data['system']['version'])
    app.setOrganizationName(softw_manager.data['system']['organization'])

    from src.views.main_view import MainView

    main_window = MainView(softw_manager)
    main_window.show()

    sys.exit(app.exec_())
