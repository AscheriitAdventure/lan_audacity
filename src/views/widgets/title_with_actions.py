from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from typing import *
import logging
import inspect


class TitleWithActions(QWidget):
    def __init__(
            self, 
            title: Union[str, QLabel] = "No Title", 
            btn_actions: Optional[List[QPushButton]] = None, 
            debug: bool = False, 
            parent=None):
        """
        Widget avec titre et boutons d'action alignés horizontalement.
        
        Args:
            title: Texte du titre ou widget QLabel
            btn_actions: Liste des boutons d'action
            debug: Active le mode débogage
            parent: Widget parent
        """
        super(TitleWithActions, self).__init__(parent)

        self.debug = debug
        self._title = QLabel(self) if isinstance(title, str) else title
        self._list_btn_action = btn_actions if btn_actions is not None else []
                
        self.initUI()
        
        # Définir le titre si un string est passé
        if isinstance(title, str) and title:
            self.setTitle(title)
    
    def initUI(self):
        """Initialise l'interface utilisateur."""
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Ajouter le titre
        self.mainLayout.addWidget(self._title)
        self._title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.mainLayout.addStretch(1)
        
        # Ajouter les boutons d'action
        if self._list_btn_action:
            self.addListBtnAction(self._list_btn_action)
    
    @property
    def btnActions(self) -> List[QPushButton]:
        """Retourne la liste des boutons d'action."""
        return self._list_btn_action
    
    def setTitle(self, title: Union[QLabel, str]) -> None:
        """
        Définit le titre du widget.
        
        Args:
            title: Texte du titre ou widget QLabel
        """
        try:
            if isinstance(title, QLabel):
                # Remplacer notre QLabel par celui fourni
                self.mainLayout.removeWidget(self._title)
                self._title = title
                self.mainLayout.insertWidget(0, self._title)
            elif isinstance(title, str):
                self._title.setText(title)
            else:
                if self.debug:
                    logging.warning(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: "
                                  f"Type non supporté: {type(title)}")
                return
                
            self._title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        except Exception as e:
            if self.debug:
                logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {str(e)}")
    
    def addBtnAction(self, btn: QPushButton) -> None:
        """
        Ajoute un bouton d'action.
        
        Args:
            btn: Bouton à ajouter
        """
        if not isinstance(btn, QPushButton):
            if self.debug:
                logging.warning(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: "
                              f"Type non supporté: {type(btn)}")
            return
            
        self._list_btn_action.append(btn)
        self.mainLayout.addWidget(btn)

    def addListBtnAction(self, list_btn: List[QPushButton]) -> None:
        """
        Ajoute une liste de boutons d'action.
        
        Args:
            list_btn: Liste des boutons à ajouter
        """
        if not list_btn:
            return
            
        for btn in list_btn:
            self.addBtnAction(btn)
            
    def clearActions(self) -> None:
        """Supprime tous les boutons d'action."""
        for btn in self._list_btn_action:
            self.mainLayout.removeWidget(btn)
            btn.setParent(None)
        
        self._list_btn_action.clear()

