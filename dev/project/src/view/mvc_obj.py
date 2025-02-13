from typing import Dict, List, Optional, Union
from qtpy.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget

from dev.project.src.classes.cl_extented import IconApp

class TitleBlock(QWidget):
    """Widget pour le bloc de titre avec actions optionnelles"""
    def __init__(self, text: Union[str, QLabel], collapse_btn: Optional[QPushButton] = None, actions: Optional[List[Union[QPushButton, Dict]]] = None):
        super().__init__()
        self.setFixedHeight(25)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        
        # Ajout du bouton collapse s'il existe
        if collapse_btn:
            self.layout.addWidget(collapse_btn)
        
        # Gestion du titre
        if isinstance(text, str):
            self.title_label = QLabel(text.upper())
        else:
            self.title_label = text
        self.title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.layout.addWidget(self.title_label)
        self.layout.addStretch()
        
        # Ajout des actions
        if actions:
            for action in actions:
                if isinstance(action, QPushButton):
                    self.layout.addWidget(action)
                elif isinstance(action, dict):
                    btn = QPushButton()
                    if isinstance(action.get('icon'), str):
                        btn.setText(action.get('icon', ''))
                    elif isinstance(action.get('icon'), dict):
                        btn.setIcon(IconApp.from_dict(action.get('icon')).get_qIcon())
                    btn.setFixedSize(16, 16)
                    btn.setStyleSheet("QPushButton { border: none; }")
                    if 'callback' in action and action['callback'] is not None:
                        btn.clicked.connect(action['callback'])
                    if 'tooltip' in action:
                        btn.setToolTip(action['tooltip'])
                    self.layout.addWidget(btn)

    def set_title(self, text: str):
        """Met à jour le texte du titre"""
        self.title_label.setText(text.upper())

    def add_action(self, action: Union[QPushButton, Dict]):
        """Ajoute une action au bloc de titre"""
        if isinstance(action, QPushButton):
            self.layout.addWidget(action)
        elif isinstance(action, dict):
            btn = QPushButton()
            if isinstance(action.get('icon'), str):
                btn.setText(action.get('icon', ''))
            elif isinstance(action.get('icon'), dict):
                btn.setIcon(IconApp.from_dict(action.get('icon')).get_qIcon())
            btn.setFixedSize(16, 16)
            btn.setStyleSheet("QPushButton { border: none; }")
            if 'callback' in action:
                btn.clicked.connect(action['callback'])
            if 'tooltip' in action:
                btn.setToolTip(action['tooltip'])
            self.layout.addWidget(btn)
