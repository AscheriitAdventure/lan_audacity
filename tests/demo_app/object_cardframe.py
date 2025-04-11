from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from typing import *

from src.views.widgets import Card,TitleBlock


def obj_to_crdfrm(obj:Any, parent=None, titre:Optional[str]=None) -> List[QWidget]:
    lsqd: list[QWidget] = []

    if isinstance(obj, str):
        cf = Card(parent=parent)
        cf.setPositionCard("center",QLabel(obj))
        lsqd.append(cf)
    
    elif isinstance(obj, (int, float)):
        cf = Card(parent=parent)
        cf.setPositionCard("center",QLabel(str(obj)))
        lsqd.append(cf)
    
    elif isinstance(obj, (list, tuple)):
        cf = Card(parent=parent)
        if len(obj) == 0:
            cf.setPositionCard("center",QLabel("Liste vide"))
            lsqd.append(cf)
        # Si tous les éléments sont de type scalaire, on crée un tableau
        if all(isinstance(item, (str, int, float)) for item in obj):
            tbl = QTableWidget(len(obj), 1)
            tbl.setHorizontalHeaderLabels(["Valeurs"])
            for i, item in enumerate(obj):
                tbl.setItem(i, 0, QTableWidgetItem(str(item)))
            cf.setPositionCard("center",tbl)
            lsqd.append(cf)
        else:
            for i, item in enumerate(obj):
                cards = obj_to_crdfrm(item, parent, f"Item {i}")
                if isinstance(cards, list):
                    for a in cards:
                        lsqd.append(a)

    elif isinstance(obj, dict) or hasattr(obj, "__dict__"):
        cf = Card(parent=parent)
        
        if isinstance(obj, dict):
            attributes = obj
            class_name = "Dictionnaire" if titre is None else titre
        else:
            attributes = {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
            class_name = obj.__class__.__name__
        
        cf.setPositionCard("top",TitleBlock(text=class_name))

        c_wdt = QWidget()
        c_lyt = QVBoxLayout()
        c_wdt.setLayout(c_lyt)
        c_lyt.setContentsMargins(0, 0, 0, 0)

        for k, v in attributes.items():
            if isinstance(v, (str, int, float)):
                c_lyt.addWidget(QLabel(f"{k} : {v}"))
            elif isinstance(v, (list, tuple)):
                c_lyt.addWidget(QLabel(f"{k} : {len(v)} items"))
            elif isinstance(v, dict) or hasattr(v, "__dict__"):
                n_c = obj_to_crdfrm(v, parent, k)
                lsqd.append(n_c[0]) # On suppose qu'il n'y a qu'une seule carte pour les objets imbriqués
        cf.setPositionCard("center",c_wdt)
        lsqd.append(cf)
        
    else:   
        # Si l'objet n'est pas pris en charge, retourner un message d'erreur
        lsqd.append(QLabel(f"{obj} non pris en charge"))

    return lsqd