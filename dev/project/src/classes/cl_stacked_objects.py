"""
    Remarques:
        Suite à la création de la classe GeneralSidePanel, nous avons pu créer différentes classes filles.
        Mais avec une vision d'évolution, cette classe est devenue embêtante à maintenir.
        Donc nous allons améliorer cette classe pour permettre une meilleure possibilité d'évolution.
        Pour cela nous allons créer une classe dynamique ou de type "Factory" qui va s'occuper de toute la partie GUI.
    Outils:
       - nom complet: Stacked Dynamic Factory Side Panel
       - nom court: SDFSP
       - Qtpy(Pyqt6)
       - logging
       - Python 3.12.1
    Réflexion pour load_stacked_widget:
        dict => {
            stacked_title: str,
            fields: List[Dict[str, Any]],
            stacked_widget: QWidget, 
            separator: bool = False, # separator = True => un séparateur est ajouté
            spacer: Optional[Dict], # spacer = None => pas de spacer
            enable: bool = True, # enable = True => le stacked_widget est activé
            visible: bool = True, # visible = True => le stacked_widget est visible
            collapsed: bool = False, # collapsed = True => le stacked_widget est caché
            movable: bool = False, # movable = True => l'icon dans la primary side bar est déplaçable
            slot: Optional[str] = None, # slot = None => pas de slot
            tooltip: Optional[str] = None, # tooltip = None => pas de tooltip
            shortcut: Optional[str] = None, # shortcut = None => pas de shortcut
            icon: Optional[Union[Dict, QIcon, str]] = None, # icon = None => pas d'icon
        }
        field => {
            field_name: str,
            field_type: str, # "tree", "list-btn", "list", "tree-file"
            widget: QWidget,
            slot: List[Callable] = [],
            tooltip: Optional[str] = None,
            actions: List[Callable],
        }
        icon: Dict => {
            names: List[str],
            options: Dict[str, Any]
        }
        spacer => {
            before: bool = False, # before = True => le spacer est ajouté avant le stacked_widget
            after: bool = False, # after = True => le spacer est ajouté après le stacked_widget
            north: bool = False, # north = True => le spacer est ajouté au nord du stacked_widget
            south: bool = False, # south = True => le spacer est ajouté au sud du stacked_widget
            east: bool = False, # east = True => le spacer est ajouté à l'est du stacked_widget
            west: bool = False, # west = True => le spacer est ajouté à l'ouest du stacked_widget
        }
"""
from typing import List, Dict, Any
import logging
import inspect

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *