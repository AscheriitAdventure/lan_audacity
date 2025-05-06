from typing import *
import logging
import inspect
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import qtawesome as qta
import uuid
from dataclasses import asdict

from src.views.widgets import *
from src.utils import prettyKeys


class CustomCardForm(Card):
    """Custom Card Form with dynamic fields as CCF."""
    
    # Signal émis lorsque les données du formulaire sont modifiées
    formDataChanged: ClassVar[Signal] = Signal(dict)
    
    def __init__(
            self, 
            title: str = "Custom Card Form",
            data_form: Union[object, Dict[str, Any], None] = None,
            debug: Optional[bool] = False, 
            parent=None
        ) -> None:
        super().__init__(debug, parent)

        logging.info(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Initializing...")
        self.headerPanel: TitleWithActions = TitleWithActions(title=title, debug=self.debug, parent=self)
        self.setPositionCard("top", self.headerPanel)

        logging.info(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Initializing form...")
        self.formObject: QWidget = QWidget(self)
        self.formLayout: QFormLayout = QFormLayout()
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(1)
        self.formObject.setLayout(self.formLayout)
        self.setPositionCard("center", self.formObject)
        
        # Stocker les données originales
        self.original_data = None
        self.edit_widgets = {}  # Pour stocker les widgets d'édition
        self.is_editing = False  # Mode édition désactivé par défaut

        if data_form is not None:
            self.initForm(data_form)

        self.setMinimumHeight(200)
        self.setMinimumWidth(200)
        self.setMaximumWidth(400)
        self.setMaximumHeight(600)
    
    def initForm(self, data_form: Union[object, Dict[str, Any]]) -> None:
        """Initialize the form with the given data."""
        if hasattr(data_form, '__dataclass_fields__'):
            data_dict = asdict(data_form)
        elif isinstance(data_form, object) and hasattr(data_form, '__dict__'):
            data_dict = data_form.__dict__
        else:
            data_dict = data_form
        logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: {data_dict}")
        
        # Stocker les données originales
        self.original_data = data_dict.copy()

        pretty_keys: dict = prettyKeys(data_dict)
        self.field_mapping = {}  # Stockage pour la correspondance entre les clés affichées et originales

        for key, value in data_dict.items():
            pretty_key = pretty_keys[key]
            self.field_mapping[pretty_key] = key  # Enregistrer la correspondance
            
            if isinstance(value, dict):
                logging.warning(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Dict type not supported: {key}: {value}")
                # Affiche le nombre d'éléments dans le dictionnaire
                self.formLayout.addRow(f"{pretty_key} :", QLabel(f"{len(value)} elements"))

            elif isinstance(value, list):
                # Affiche le nombre d'éléments dans la liste
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - List type: {key} - {len(value)} elements")
                self.formLayout.addRow(f"{pretty_key} :", QLabel(f"{len(value)} elements"))
            
            elif isinstance(value, uuid.UUID):
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - UUID type: {key} - {value}")
                self.formLayout.addRow(f"{pretty_key} :", QLabel(str(value)))

            elif isinstance(value, str):
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - String type: {key} - {value}")
                edit_widget = QLineEdit(value)
                edit_widget.setEnabled(self.is_editing)
                self.edit_widgets[key] = edit_widget
                self.formLayout.addRow(f"{pretty_key} :", edit_widget)

            elif isinstance(value, int):
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Integer type: {key} - {value}")
                # Vérifier si c'est un timestamp
                is_ts, formatted_value = self.is_timestamp(value)
                
                if is_ts:
                    # Si c'est un timestamp, afficher comme texte
                    edit_widget = QLineEdit(formatted_value)
                else:
                    # Sinon, utiliser un QSpinBox
                    edit_widget = QSpinBox()
                    edit_widget.setRange(-999999999, 999999999)
                    edit_widget.setValue(value)
                
                edit_widget.setEnabled(False)
                self.edit_widgets[key] = edit_widget
                self.formLayout.addRow(f"{pretty_key} :", edit_widget)

            elif isinstance(value, float):
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Float type: {key} - {value}")
                # Vérifier si c'est un timestamp
                is_ts, formatted_value = self.is_timestamp(value)
                
                if is_ts:
                    # Si c'est un timestamp, afficher comme texte
                    edit_widget = QLineEdit(formatted_value)
                else:
                    # Sinon, utiliser un QDoubleSpinBox
                    edit_widget = QDoubleSpinBox()
                    edit_widget.setRange(-999999999.0, 999999999.0)
                    edit_widget.setDecimals(5)
                    edit_widget.setValue(value)
                
                edit_widget.setEnabled(False)
                self.edit_widgets[key] = edit_widget
                self.formLayout.addRow(f"{pretty_key} :", edit_widget)

            elif isinstance(value, bool):
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Boolean type: {key} - {value}")
                edit_widget = QCheckBox()
                edit_widget.setChecked(value)
                edit_widget.setEnabled(self.is_editing)
                self.edit_widgets[key] = edit_widget
                self.formLayout.addRow(f"{pretty_key} :", edit_widget)

            elif value is None:
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - None type: {key} - {value}")
                edit_widget = QLineEdit("")
                edit_widget.setPlaceholderText("Non Renseigné")
                edit_widget.setEnabled(self.is_editing)
                self.edit_widgets[key] = edit_widget
                self.formLayout.addRow(f"{pretty_key} :", edit_widget)

            elif isinstance(value, object):
                logging.warning(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Object type not supported: {key}: {value}")

            else:
                logging.warning(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Unknown type: {key} - {value}")
                self.formLayout.addRow(f"{pretty_key} :", QLabel(str(value)))
        
        # Zone pour les boutons de contrôle (masqués par défaut)
        self.controlsWidget = QWidget()
        self.controlsLayout = QHBoxLayout(self.controlsWidget)
        self.controlsLayout.setContentsMargins(0, 0, 0, 0)
        
        self.saveBtn = QPushButton("Enregistrer")
        self.saveBtn.setIcon(qta.icon("fa5s.save"))
        self.saveBtn.clicked.connect(self.saveFormChanges)
        
        self.cancelBtn = QPushButton("Annuler")
        self.cancelBtn.setIcon(qta.icon("fa5s.times"))
        self.cancelBtn.clicked.connect(self.cancelEditing)
        
        self.controlsLayout.addWidget(self.saveBtn)
        self.controlsLayout.addWidget(self.cancelBtn)
        
        self.controlsWidget.setVisible(False)
        self.formLayout.addRow("", self.controlsWidget)
        
        # Ajouter un spacer à la fin
        self.formLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    #### Setter Methods ####
    def setUpdateBtn(self, var: bool) -> None:
        """
        Ajouter un bouton de modification de valeur au panneau de titre.

        Args:
            var: True pour activer, False pour désactiver
        """
        if not var:
            return
        
        # Ajout du bouton de modification de valeur
        self.updateBtn = QPushButton(self)
        self.updateBtn.setIcon(qta.icon("fa5s.edit"))
        self.updateBtn.setToolTip("Modifier une ou plusieurs valeurs")
        self.updateBtn.setFlat(True)
        self.updateBtn.clicked.connect(self.toggleEditMode)  # Connecter au signal clicked

        self.headerPanel.addBtnAction(self.updateBtn)
    
    def setAlterTypePanel(self, var: bool) -> None:
        if not var:
            return
        pass
    
    def toggleEditMode(self):
        """Active ou désactive le mode édition du formulaire."""
        self.is_editing = not self.is_editing
        
        # Activer/Désactiver les widgets d'édition
        for widget in self.edit_widgets.values():
            widget.setEnabled(self.is_editing)
        
        # Afficher/Masquer les boutons de contrôle
        self.controlsWidget.setVisible(self.is_editing)
        
        # Changer l'icône du bouton d'édition
        if self.is_editing:
            self.updateBtn.setIcon(qta.icon("fa5s.lock"))
            self.updateBtn.setToolTip("Verrouiller les champs")
        else:
            self.updateBtn.setIcon(qta.icon("fa5s.edit"))
            self.updateBtn.setToolTip("Modifier une ou plusieurs valeurs")
    
    def cancelEditing(self):
        """Annule le mode édition et restaure les valeurs originales."""
        # Restaurer les valeurs d'origine
        for key, widget in self.edit_widgets.items():
            value = self.original_data.get(key)
            
            if isinstance(widget, QLineEdit):
                widget.setText("" if value is None else str(value))
            elif isinstance(widget, QSpinBox):
                widget.setValue(0 if value is None else value)
            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(0.0 if value is None else value)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False if value is None else value)
        
        # Désactiver le mode édition
        self.toggleEditMode()
    
    def saveFormChanges(self):
        """Enregistre les modifications apportées au formulaire."""
        # Dictionnaire pour stocker les valeurs modifiées
        updated_values = {}
        
        # Parcourir tous les widgets d'édition
        for key, widget in self.edit_widgets.items():
            # Récupérer la valeur d'origine et la nouvelle valeur
            original_value = self.original_data.get(key)
            
            if isinstance(widget, QLineEdit):
                new_value = widget.text()
                # Convertir en None si vide et que la valeur originale était None
                if not new_value and original_value is None:
                    new_value = None
            elif isinstance(widget, QSpinBox):
                new_value = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                new_value = widget.value()
            elif isinstance(widget, QCheckBox):
                new_value = widget.isChecked()
            else:
                continue
            
            # Vérifier si la valeur a changé
            if new_value != original_value:
                updated_values[key] = new_value
                self.original_data[key] = new_value
        
        # Émettre un signal pour informer des modifications (seulement s'il y a des changements)
        if updated_values:
            self.formDataChanged.emit(updated_values)
        
        # Désactiver le mode édition
        self.toggleEditMode()
    
    def is_timestamp(self, value: Union[int, float]) -> tuple[bool, Any]:
        """
        Tente de convertir une valeur en format date/heure si elle ressemble à un timestamp.
    
        Args:
            value: La valeur à formater (float ou int)
    
        Returns:
            str: La valeur formatée si c'est un timestamp, sinon la valeur d'origine
        """
        # Vérifier si la valeur pourrait être un timestamp
        # Un timestamp Unix valide devrait être entre ~20 ans dans le passé et ~20 ans dans le futur
        from datetime import datetime
        current_timestamp = datetime.now().timestamp()
        min_valid_timestamp = current_timestamp - (20 * 365 * 24 * 3600)  # ~20 ans dans le passé
        max_valid_timestamp = current_timestamp + (20 * 365 * 24 * 3600)  # ~20 ans dans le futur
    
        # Si la valeur est dans cette plage, c'est probablement un timestamp
        if isinstance(value, (int, float)) and min_valid_timestamp <= value <= max_valid_timestamp:
            try:
                dt = datetime.fromtimestamp(value)
                return (True, dt.strftime("%H:%M:%S %d/%m/%Y"))
            except (ValueError, OverflowError):
                # Si la conversion échoue, retourner la valeur d'origine
                logging.warning(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Timestamp conversion failed: {value}")
                return (False, value)
    
        # Sinon, retourner la valeur d'origine
        return (False, value)
        