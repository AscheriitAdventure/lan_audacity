from typing import Optional, Union, Callable, List, Any
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
import os
import logging



def newAction(
        parent: QWidget,
        text: str,
        slot: Optional[Callable],
        shortcut: Optional[Union[str, List[str]]],
        icon: Optional[str|QIcon],
        tip: Optional[str],
        checkable: bool = False,
        enabled: bool = True,
) -> Any:
    """Create a new action and assign callbacks, shortcuts, etc."""
    a = QAction(text, parent)

    if isinstance(icon, str):
        a.setIcon(QIcon(icon))
    elif isinstance(icon, QIcon):
        a.setIcon(icon)
    else:
        logging.warning(f"Icon {icon} is not a valid type. Must be str or QIcon")

    if isinstance(shortcut, str):
        a.setShortcut(shortcut)
    elif isinstance(shortcut, list):
        a.setShortcuts(shortcut)
    else:
        logging.warning(f"Shortcut {shortcut} is not a valid type. Must be str or List[str]")
    
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)

    if slot is not None:
        a.triggered.connect(slot)

    a.setCheckable(checkable)
    a.setEnabled(enabled)
    return a

def get_spcValue(liste_add: list, arg_1: str, obj_src: str) -> Optional[dict]:
    for obj_dict in liste_add:
        if obj_dict[arg_1] == obj_src:
            return obj_dict
    return None

