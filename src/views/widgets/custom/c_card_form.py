from typing import *
import logging
import inspect
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import qtawesome as qta
import uuid

from src.views.widgets import *
from src.utils import prettyKeysList, prettyKeys


class CustomCardForm(Card):
    """Custom Card Form with dynamic fields as CCF."""
    def __init__(
            self, 
            title: str = "Custom Card Form",
            data_form: Union[object, Dict[str, Any], None] = None,
            debug: Optional[bool] = False, 
            parent=None
        ) -> None:
        super(CustomCardForm, self).__init__(debug, parent)

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

        if data_form is not None:
            self.initForm(data_form)

        self.setMinimumHeight(200)
        self.setMinimumWidth(200)
        self.setMaximumWidth(400)
        self.setMaximumHeight(600)
    
    def initForm(self, data_form: Union[object, Dict[str, Any]]) -> None:
        """Initialize the form with the given data."""
        data_dict: dict = data_form.__dict__ if isinstance(data_form, object) and hasattr(data_form, '__dict__') else data_form
        logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: {data_dict}")

        for key, value in data_dict.items():
            if isinstance(value, dict):
                logging.warning(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Dict type not supported: {key}: {value}")
                # Affiche le nombre d'éléments dans le dictionnaire
                self.formLayout.addRow(f"{key} :", QLabel(f"{len(value)} elements"))

            elif isinstance(value, list):
                # Affiche le nombre d'éléments dans la liste
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - List type: {key} - {len(value)} elements")
                self.formLayout.addRow(f"{key} :", QLabel(f"{len(value)} elements"))
            
            elif isinstance(value, uuid.UUID):
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - UUID type: {key} - {value}")
                self.formLayout.addRow(f"{key} :", QLabel(str(value)))

            elif isinstance(value, str):
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - String type: {key} - {value}")
                self.formLayout.addRow(f"{key} :", QLabel(value))

            elif isinstance(value, int):
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Integer type: {key} - {value}")
                self.formLayout.addRow(f"{key} :", QLabel(str(value)))

            elif isinstance(value, float):
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Float type: {key} - {value}")
                self.formLayout.addRow(f"{key} :", QLabel(str(value)))

            elif isinstance(value, bool):
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Boolean type: {key} - {value}")
                self.formLayout.addRow(f"{key} :", QLabel(str(value)))

            elif value is None:
                logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - None type: {key} - {value}")
                self.formLayout.addRow(f"{key} :", QLabel("Non Renseigné"))

            elif isinstance(value, object):
                logging.warning(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Object type not supported: {key}: {value}")

            else:
                logging.warning(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - Unknown type: {key} - {value}")
                self.formLayout.addRow(f"{key} :", QLabel(str(value)))
        

