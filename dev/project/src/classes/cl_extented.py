from typing import Optional, List, Union
from dataclasses import dataclass, field
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
        return IconApp(
            names=data["names"],
            options=data.get("options")
        )


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

    @staticmethod
    def from_dict(data: dict) -> "ActionObject":
        return ActionObject(
            text=data["text"],
            slot=data.get("slot"),
            shortcut=data.get("shortcut"),
            icon=IconApp.from_dict(data["icon"]) if isinstance(data.get("icon"), dict) else data.get("icon"),
            tip=data.get("tip"),
            checkable=data.get("checkable", False),
            enabled=data.get("enabled", True),
            separator=data.get("separator", False),
        )
    
    def get_dict(self) -> dict:
        return {
            "text": self.text,
            "slot": self.slot,
            "shortcut": self.shortcut,
            "icon": self.icon.get_qIcon() if isinstance(self.icon, IconApp) else self.icon,
            "tip": self.tip,
            "checkable": self.checkable,
            "enabled": self.enabled,
        }


@dataclass
class MenuBarObject:
    title: str
    icon: Optional[Union[str, IconApp]] = None
    actions: List[ActionObject] = field(default_factory=list)
    separator: bool = field(default=False)

    @staticmethod
    def from_dict(data: dict) -> "MenuBarObject":
        return MenuBarObject(
            title=data["title"],
            icon=IconApp.from_dict(data["icon"]) if isinstance(data.get("icon"), dict) else data.get("icon"),
            actions=[ActionObject.from_dict(action) for action in data.get("actions", [])],
            separator=data.get("separator", False),
        )

