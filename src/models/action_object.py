from dataclasses import dataclass, field
from typing import Optional, Union, List

from .icon_app import IconApp


@dataclass
class ActionObject:
    text: str
    slot: Optional[dict] = None
    shortcut: Optional[Union[str, List[str]]] = None
    icon: Optional[Union[str, IconApp]] = None
    tip: Optional[str] = None
    checkable: bool = False
    enabled: bool = True
    separator: bool = field(default=False)
    type: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> "ActionObject":
        tmp_dict: dict = {}
        tmp_dict["text"] = data["text"]
        tmp_dict["slot"] = data.get("slot", None)
        tmp_dict["shortcut"] = data.get("shortcut", None)
        tmp_dict["icon"] = IconApp.from_dict(data["icon"]) if isinstance(data.get("icon"), dict) else data.get("icon")
        tmp_dict["tip"] = data.get("tip", None)
        tmp_dict["checkable"] = data.get("checkable", False)
        tmp_dict["enabled"] = data.get("enabled", True)
        tmp_dict["separator"] = data.get("separator", False)
        tmp_dict["type"] = data.get("type", None)

        # Supprimer les valeurs None pour nettoyer le dictionnaire
        tmp2_dict = {k: v for k, v in tmp_dict.items() if v is not None}
        
        return ActionObject(**tmp2_dict)

    def get_dict(self) -> dict:
        res: dict = {
            "text": self.text,
            "slot": self.slot,
            "tip": self.tip,
            "enabled": self.enabled,
            "separator": self.separator,
        }

        if self.type is None:
            res["shortcut"] = self.shortcut
            res["icon"] = self.icon.get_dict() if isinstance(self.icon, IconApp) else self.icon
            res["checkable"] = self.checkable

        else:
            res["type"] = self.type
        
        return {k: v for k, v in res.items() if v is not None}

