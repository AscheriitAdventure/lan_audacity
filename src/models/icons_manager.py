from qtpy.QtGui import QIcon
from typing import Optional
import qtawesome as qta

from .factory_conf_file import FactoryConfFile


class IconsManager(FactoryConfFile):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path, FactoryConfFile.RWX.READ)
        self.action_file(self.rw_mode)

    def get_icon(self, icon_name: str) -> Optional[QIcon]:
        for data in self.file_data:
            if data["name"] == icon_name:
                if data["options"] is None:
                    ico_obj = qta.icon(*data["platform_and_name"])
                else:
                    ico_obj = qta.icon(
                        *data["platform_and_name"], options=data["options"]
                    )
                return ico_obj
        return None
