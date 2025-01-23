from typing import Optional, List, Union
from dataclasses import dataclass


@dataclass
class IconApp:
    names: Union[str, List[str], tuple[str]]
    options: Optional[List[dict]] = None

@dataclass
class ActionObject:
    text: str
    slot: Optional[dict] = None
    shortcut: Optional[Union[str, List[str]]] = None
    icon: Optional[Union[str, IconApp]] = None
    tip: Optional[str] = None
    checkable: bool = False
    enabled: bool = True

@dataclass
class MenuBarObject:
    title: str
    icon: Optional[Union[str, IconApp]] = None
    actions: List[dict]