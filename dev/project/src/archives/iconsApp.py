from dev.project.src.archives.configurationFile import ConfigurationFile

import qtawesome as qta
from qtpy.QtGui import QIcon


class IconsApp:
    def __init__(self, file_manager: ConfigurationFile):
        self.data_manager = file_manager.data

    def get_icon(self, key: str) -> QIcon:
        for icon in self.data_manager:
            if icon["name"] == key:
                if icon["options"] is None:
                    ico_obj = qta.icon(*icon["platform_and_name"])
                else:
                    ico_obj = qta.icon(
                        *icon["platform_and_name"], options=icon["options"]
                    )
                return ico_obj