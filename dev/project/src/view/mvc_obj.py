from typing import Dict, List, Optional, Union, Any
from qtpy.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget

from dev.project.src.classes.cl_extented import IconApp

class TitleBlock(QWidget):
    """Widget pour le bloc de titre avec actions optionnelles"""
    def __init__(
            self, 
            text: Union[str, QLabel], 
            collapse_btn: Optional[QPushButton] = None, 
            actions: Optional[List[Union[QPushButton, Dict[str, Any]]]] = None):
        super().__init__()
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.setFixedHeight(25)

        self.mainLayout.setContentsMargins(2,2,2,2)

        if collapse_btn is not None:
            self.mainLayout.addWidget(collapse_btn)
        
        # Gestion du titre
        if isinstance(text, str):
            self.title_label = QLabel(text.upper())
        else:
            self.title_label = text

        self.title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Policy.Fixed)
        self.mainLayout.addWidget(self.title_label)
        self.mainLayout.addStretch()
        
        # Ajout des actions
        if actions is not None and len(actions) > 0:
            for action in actions:
                self.add_action(action)

    def set_title(self, text: str):
        """Met à jour le texte du titre"""
        self.title_label.setText(text.upper())

    def add_action(self, action: Union[QPushButton, Dict]):
        """Ajoute une action au bloc de titre"""
        if isinstance(action, QPushButton):
            self.mainLayout.addWidget(action)

        elif isinstance(action, dict):
            btn = QPushButton()
            if isinstance(action.get('icon'), str):
                btn.setText(action.get('icon', ''))

            elif isinstance(action.get('icon'), dict):
                ico = IconApp.from_dict(action.get('icon'))
                btn.setIcon(ico.get_qIcon())

            btn.setFixedSize(16, 16)
            btn.setStyleSheet("QPushButton { border: none; }")

            if 'callback' in action and action['callback'] is not None:
                btn.clicked.connect(action['callback'])

            if 'tooltip' in action and action['tooltip'] is not None:
                btn.setToolTip(action['tooltip'])

            self.mainLayout.addWidget(btn)
        
