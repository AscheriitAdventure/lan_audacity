from dataclasses import dataclass, field
from typing import Optional, Union, List

from .icon_app import IconApp
from .action_object import ActionObject


@dataclass
class MenuBarObject:
    title: str
    icon: Optional[Union[str, IconApp]] = None
    actions: List[ActionObject] = field(default_factory=list)
    separator: bool = field(default=False)

    @staticmethod
    def from_dict(data: dict) -> "MenuBarObject":
        tmp_dict: dict = {}
        tmp_dict["title"] = data["title"]
        tmp_dict["icon"] = IconApp.from_dict(data["icon"]) if isinstance(data.get("icon"), dict) else data.get("icon")
        tmp_dict["actions"] = [ActionObject.from_dict(action) for action in data.get("actions", [])]
        tmp_dict["separator"] = data.get("separator", False)
        
        tmp2_dict = {k: v for k, v in tmp_dict.items() if v is not None}

        return MenuBarObject(**tmp2_dict)
