from typing import Optional, Union, Callable, List
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
):
    """Create a new action and assign callbacks, shortcuts, etc."""
    a = QAction(text, parent)

    if isinstance(icon, str):
        a.setIcon(QIcon(icon))
    elif isinstance(icon, QIcon):
        a.setIcon(icon)
    else:
        logging.warning(f"Icon {icon} is not a valid type. Must be str or QIcon")

    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            a.setShortcuts(shortcut)
        else:
            a.setShortcut(shortcut)
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)
    if slot is not None:
        a.triggered.connect(slot)
    if checkable:
        a.setCheckable(True)
    a.setEnabled(enabled)
    return a