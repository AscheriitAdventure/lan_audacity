import os
import logging
import inspect
from typing import Any, List, Tuple, Dict

from qtpy.QtWidgets import *
from qtpy.QtGui import QRegularExpressionValidator
from qtpy.QtCore import QRegularExpression

"""
    Remarques:
        Suites à la création de la classe FormDialog, on a pu créer deux classes filles NProject et DiscoveryMode qui héritent de FormDialog.
        Mais FormDialog est une classe trop fermée, elle ne permet pas de créer des formulaires dynamiques.
        Donc nous allons créer une classe plus ouverte qui permettra de créer des formulaires dynamiques.
    Outils:
        - nom complet: Dynamic Form Dialog
        - nom court: DynFormDialog
        - Qtpy(Pyqt6)
        - logging
    Reflexion pour load_form:
            dict => {
                window_title: str,
                title: Optional[str],
                separator: bool = False,
                fields: List[Dict[str, Any]],
                grid: Union[List[int], Tuple[int, int]],
            }
            field => {
                label: Optional[str],
                input: Any,
                required: bool = False,
                placeholder: Optional[str] = None,
                text: Optional[str] = None,
                tooltip: Optional[str] = None,
                readonly: bool = False,
                checkable: bool = False,
                checked: bool = False,
                enabled: bool = True,
                visible: bool = True,
                slot: Optional[Callable] = None,
                grid: Union[List[int], Tuple[int, int]],
            }
            input => {
                type: str,
                name: str,
                value: Any,
                options: Optional[List[Dict[str, Any]]] = None,
                min: Optional[int] = None,
                max: Optional[int] = None,
                step: Optional[int] = None,
                regex: Optional[str] = None,
                placeholder: Optional[str] = None,
                tooltip: Optional[str] = None,
                readonly: bool = False,
                checkable: bool = False,
                checked: bool = False,
                enabled: bool = True,
                visible: bool = True,
                slot: Optional[Callable] = None,
            }
    Validations:
        - load_form: OK
        - load_form_input: OK
        - load_form_field: OK
        - get_field_value: OK
        - get_form_data: OK
        - set_button_text: OK
        - set_button_enabled: OK
        - validation du remplissage des champs requis: NON
        - test: Presque OK

"""

class DynFormDialog(QDialog):
    def __init__(self, parent=None, debug: bool = False):
        super().__init__(parent)
        
        self.active_fields: List = []
        self.fields = {}
        self.title_form: str = ""
        self.title_window: str = "Setup"
        self.debug = debug
        
        self.loadUI()
    
    def loadUI(self):
        self.setWindowTitle(self.title_window)
        
        # Layout principal en vertical
        self.main_layout = QVBoxLayout(self)
        
        # Layout pour le formulaire
        self.form_widget = QWidget()
        self.layout = QGridLayout(self.form_widget)
        self.main_layout.addWidget(self.form_widget)
        
        # Layout pour les boutons
        self.button_layout = QHBoxLayout()
        
        # Création des boutons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Annuler")
        
        # Configuration des boutons
        self.ok_button.setDefault(True)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        # Ajout des boutons au layout avec un espacement à droite
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        
        # Ajout du layout des boutons au layout principal
        self.main_layout.addLayout(self.button_layout)
        
        if self.debug:
            logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: UI loaded")
    
    def load_form(self, form_data: Dict[str, Any]):
        """Charge un formulaire à partir d'un dictionnaire de configuration
        
        Args:
            form_data: Dictionnaire contenant la configuration du formulaire
        """
        if self.debug:
            logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Loading form...")
            
        # Configuration de la fenêtre
        self.title_window = form_data.get('window_title', self.title_window)
        self.setWindowTitle(self.title_window)
        
        current_row = 0
        
        # Titre du formulaire si présent
        if title := form_data.get('title'):
            title_label = QLabel(title)
            title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            self.layout.addWidget(title_label, current_row, 0, 1, -1)
            current_row += 1
        
        # Séparateur si demandé
        if form_data.get('separator', False):
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            self.layout.addWidget(separator, current_row, 0, 1, -1)
            current_row += 1
        
        # Chargement des champs
        for field in form_data.get('fields', []):
            current_row = self.load_form_field(field, current_row)
            if self.debug:
                logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Field added at row {current_row}")
    
    def load_form_input(self, input_config: Dict[str, Any], row: int) -> Tuple[QWidget, int]:
        """Crée un widget d'entrée selon la configuration fournie
        
        Args:
            input_config: Configuration du widget d'entrée
            row: Ligne courante dans la grille
            
        Returns:
            Tuple[QWidget, int]: Le widget créé et la nouvelle ligne courante
        """
        if self.debug:
            logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Creating input of type {input_config.get('type')} at row {row}")
            
        input_type = input_config.get('type', '').lower()
        widget = None

        if input_type == 'hidden':
            # Pour les champs cachés, on crée un QLineEdit invisible
            widget = QLineEdit()
            widget.setVisible(False)
            if value := input_config.get('value'):
                widget.setText(str(value))
        
        elif input_type == 'folder':
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            
            line_edit = QLineEdit()
            if value := input_config.get('value'):
                line_edit.setText(str(value))
            if placeholder := input_config.get('placeholder'):
                line_edit.setPlaceholderText(placeholder)
            line_edit.setReadOnly(input_config.get('readonly', True))
            
            browse_button = QPushButton("...")
            browse_button.setMaximumWidth(30)
            
            def browse_folder():
                current_path = line_edit.text()
                folder = QFileDialog.getExistingDirectory(
                    self,
                    input_config.get('dialog_title', 'Sélectionner un dossier'),
                    current_path if current_path else os.path.expanduser('~')
                )
                if folder:
                    line_edit.setText(folder)
                    if name in self.fields:
                        self.fields[name] = line_edit
                    if slot := input_config.get('slot'):
                        slot(folder)
            
            browse_button.clicked.connect(browse_folder)
            
            layout.addWidget(line_edit)
            layout.addWidget(browse_button)
            
            widget = container
            if name := input_config.get('name'):
                self.fields[name] = line_edit
                self.active_fields.append(line_edit)
        
        elif input_type == 'text':
            widget = QLineEdit()
            if value := input_config.get('value'):
                widget.setText(str(value))
            if placeholder := input_config.get('placeholder'):
                widget.setPlaceholderText(placeholder)
            if regex := input_config.get('regex'):
                validator = QRegularExpressionValidator(QRegularExpression(regex))
                widget.setValidator(validator)
                
        elif input_type == 'number':
            widget = QSpinBox()
            if 'min' in input_config:
                widget.setMinimum(input_config['min'])
            if 'max' in input_config:
                widget.setMaximum(input_config['max'])
            if 'step' in input_config:
                widget.setSingleStep(input_config['step'])
            if 'value' in input_config:
                widget.setValue(input_config['value'])
                
        elif input_type == 'combo':
            widget = QComboBox()
            if options := input_config.get('options', []):
                for option in options:
                    widget.addItem(str(option.get('label', '')), option.get('value'))
            if 'value' in input_config:
                index = widget.findData(input_config['value'])
                if index >= 0:
                    widget.setCurrentIndex(index)
                    
        elif input_type == 'check':
            widget = QCheckBox()
            if text := input_config.get('text'):
                widget.setText(text)
            widget.setChecked(input_config.get('checked', False))
            
        elif input_type == 'radio':
            widget = QRadioButton()
            if text := input_config.get('text'):
                widget.setText(text)
            widget.setChecked(input_config.get('checked', False))
            
        # Configuration commune
        if widget:
            widget.setEnabled(input_config.get('enabled', True))
            widget.setVisible(input_config.get('visible', True))
            if tooltip := input_config.get('tooltip'):
                widget.setToolTip(tooltip)
            if readonly := input_config.get('readonly', False):
                if hasattr(widget, 'setReadOnly'):
                    widget.setReadOnly(readonly)
            if slot := input_config.get('slot'):
                if hasattr(widget, 'textChanged'):
                    widget.textChanged.connect(slot)
                elif hasattr(widget, 'valueChanged'):
                    widget.valueChanged.connect(slot)
                elif hasattr(widget, 'currentIndexChanged'):
                    widget.currentIndexChanged.connect(slot)
                elif hasattr(widget, 'stateChanged'):
                    widget.stateChanged.connect(slot)
                    
            if name := input_config.get('name'):
                self.fields[name] = widget
                self.active_fields.append(widget)
        
        return widget, row + (0 if input_type == 'hidden' else 1)
    
    def load_form_field(self, field: Dict[str, Any], row: int) -> int:
        """Charge un champ du formulaire avec son label et son widget d'entrée
        
        Args:
            field: Configuration du champ
            row: Ligne courante dans la grille
            
        Returns:
            int: Nouvelle ligne courante
        """
        if self.debug:
            logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Loading field at row {row}")
        
        current_row = row
        
        # Création du label si nécessaire
        if label_text := field.get('label'):
            label = QLabel(label_text)
            if field.get('required', False):
                label.setText(f"{label_text} *")
            self.layout.addWidget(label, current_row, 0)
        
        # Création du widget d'entrée
        if input_config := field.get('input'):
            widget, next_row = self.load_form_input(input_config, current_row)
            if widget:
                # Positionnement selon la grille spécifiée ou par défaut
                grid = field.get('grid', [current_row, 1])
                if isinstance(grid, (list, tuple)) and len(grid) >= 2:
                    self.layout.addWidget(widget, grid[0], grid[1])
                    current_row = max(next_row, grid[0] + 1)
                else:
                    self.layout.addWidget(widget, current_row, 1)
                    current_row = next_row
        
        return current_row
    
    def get_field_value(self, field_name: str) -> Any:
        """Récupère la valeur d'un champ par son nom
        
        Args:
            field_name: Nom du champ
            
        Returns:
            Any: Valeur du champ
        """
        if widget := self.fields.get(field_name):
            if isinstance(widget, QLineEdit):
                return widget.text()
            elif isinstance(widget, QSpinBox):
                return widget.value()
            elif isinstance(widget, QComboBox):
                return widget.currentData()
            elif isinstance(widget, (QCheckBox, QRadioButton)):
                return widget.isChecked()
        return None
    
    def get_form_data(self) -> Dict[str, Any]:
        """Récupère toutes les valeurs du formulaire
        
        Returns:
            Dict[str, Any]: Dictionnaire des valeurs du formulaire
        """
        return {name: self.get_field_value(name) for name in self.fields}

    def set_button_text(self, ok_text: str = "OK", cancel_text: str = "Annuler"):
        """Change le texte des boutons
        
        Args:
            ok_text: Texte pour le bouton OK
            cancel_text: Texte pour le bouton Annuler
        """
        self.ok_button.setText(ok_text)
        self.cancel_button.setText(cancel_text)
    
    def set_button_enabled(self, ok_enabled: bool = True, cancel_enabled: bool = True):
        """Active/désactive les boutons
        
        Args:
            ok_enabled: État du bouton OK
            cancel_enabled: État du bouton Annuler
        """
        self.ok_button.setEnabled(ok_enabled)
        self.cancel_button.setEnabled(cancel_enabled)