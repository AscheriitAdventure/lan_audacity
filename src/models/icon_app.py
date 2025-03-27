from dataclasses import dataclass
from typing import Union, List, Optional
import qtawesome as qta
from qtpy.QtGui import QIcon


@dataclass
class IconApp:
    names: Union[str, List[str], tuple[str]]
    options: Optional[List[dict]] = None

    def get_qIcon(self) -> QIcon:
        if self.options is None:
            if isinstance(self.names, str):
                return qta.icon(self.names)
            elif isinstance(self.names, (list, tuple)):
                return qta.icon(*self.names)
        else:
            if isinstance(self.names, str):
                return qta.icon(self.names, options=self.options)
            elif isinstance(self.names, (list, tuple)):
                return qta.icon(*self.names, options=self.options)

    @staticmethod
    def from_dict(data: dict) -> "IconApp":
        return IconApp(names=data["names"], options=data.get("options"))
    
    def get_dict(self) -> dict:
        res: dict = {}
        res["names"] = self.names
        
        if self.options is not None:
            res["options"] = self.options
        
        return res

