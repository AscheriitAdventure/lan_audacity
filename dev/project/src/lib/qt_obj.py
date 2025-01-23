from typing import Optional, Union, Callable, List, Any
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
import os
import logging
import inspect

SLOT_REGISTRY = {
    "new_text_file": lambda parent: print("New Text File"),
    "new_project": lambda parent: print("New Project"),
    "open_new_window": lambda parent: print("Open New Window"),
    "open_text_file": lambda parent: print("Open Text File"),
    "open_folder_project": lambda parent: print("Open Folder Project"),
    "action_open_recent": lambda parent: print("Open Recent"),
    "action_save": lambda parent: print("Save"),
    "action_save_as": lambda parent: print("Save As"),
    "close_current_window": lambda parent: print("Close Current Window"),
    "close_all_windows": lambda parent: print("Close All Windows"),
    "end_application": lambda parent: print("End Application"),
    "action_undo": lambda parent: print("Undo"),
    "action_redo": lambda parent: print("Redo"),
    "action_cut": lambda parent: print("Cut"),
    "action_copy": lambda parent: print("Copy"),
    "action_paste": lambda parent: print("Paste"),
    "action_find": lambda parent: print("Find"),
    "action_replace": lambda parent: print("Replace"),
    "action_select_all": lambda parent: print("Select All"),
    "file_explorer_show": lambda parent: print("File Explorer Show"),
    "network_explorer_show": lambda parent: print("Network Explorer Show"),
    "extensions_show": lambda parent: print("Extensions Show"),
    "preferences_open": lambda parent: print("Preferences Open"),
    "user_settings_open": lambda parent: print("User Settings Open"),
    "new_terminal": lambda parent: print("New Terminal"),
    "welcome_open": lambda parent: print("Welcome Open"),
    "documentation_open": lambda parent: print("Documentation Open"),
    "show_update_notes": lambda parent: print("Show Update Notes"),
    "search_updates": lambda parent: print("Search Updates"),
    "about_open": lambda parent: print("About Open"),
}


def newAction(
        parent: QWidget,
        text: str,
        slot: Optional[Callable] = None,
        shortcut: Optional[Union[str, List[str]]] = None,
        icon: Optional[str|QIcon] = None,
        tip: Optional[str] = None,
        checkable: bool = False,
        enabled: bool = True,
        write_log: bool = False
) -> Any:
    """Create a new action and assign callbacks, shortcuts, etc."""
    if write_log:
        logging.debug(f"{inspect.currentframe().f_code.co_name}: {slot, shortcut, icon, tip}")
    a = QAction(text, parent)

    if isinstance(icon, str):
        """ si le retour est une string alors on a deux solutions soit on a un chemin absolu soit on a un chemin relatif
        si on a un chemin absolu alors on peut utiliser QIcon(icon) sinon on doit utiliser QIcon(os.path.join(os.path.dirname(__file__), icon))"""
        if os.path.isabs(icon):
            a.setIcon(QIcon(icon))
        else:
            a.setIcon(QIcon(os.path.join(os.path.dirname(__file__), icon)))
    elif isinstance(icon, QIcon):
        a.setIcon(icon)
    else:
        logging.warning(f"Icon {icon} is not a valid type. Must be str or QIcon")

    if isinstance(shortcut, str):
        a.setShortcut(shortcut)
    elif isinstance(shortcut, (list, tuple)):
        a.setShortcuts(shortcut)
    else:
        logging.warning(f"Shortcut {shortcut} is not a valid type. Must be str or List[str]")
    
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)

    if slot and "name" in slot and slot["name"] in SLOT_REGISTRY:
        a.triggered.connect(lambda _: SLOT_REGISTRY[slot["name"]](parent))

    a.setCheckable(checkable)
    a.setEnabled(enabled)
    return a


def get_spcValue(liste_add: list, arg_1: str, obj_src: str, write_log: bool = False) -> Optional[dict]:
    for obj_dict in liste_add:
        if obj_dict[arg_1] == obj_src:
            if write_log:
                logging.debug(f"{inspect.currentframe().f_code.co_name}: {obj_dict}")
            return obj_dict
    return None


def createMenu(menu_bar, menu_data, parent=None):
    for a in menu_data:
        if a["separator"]:
            menu_bar.addSeparator()
        b = QMenu(a["title"], menu_bar)
        if a["icon"]:
            b.setIcon(a["icon"])
        menu_bar.addMenu(b)

        if a["actions"]:
            for c in a["actions"]:
                c["parent"] = parent
                if c.get("separator"):
                    b.addSeparator()
                c.pop("separator", None)
                logging.debug(f"{inspect.currentframe().f_code.co_name}: {c}")
                d = newAction(**c)
                b.addAction(d)
        else:
            b.addSeparator()

