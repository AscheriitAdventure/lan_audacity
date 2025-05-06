from typing import *
import logging
import inspect
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *

from src.views.widgets import *
from src.utils import prettyKeys
from .c_card_form import CustomCardForm as CCF


class CustomCardFormButton(CCF):
    """Custom Card Form with dynamic fields as CCF."""

    def __init__(self, *args, **kwargs) -> None:
        super(CustomCardFormButton, self).__init__(*args, **kwargs)

    def initForm(self, data_form: Dict[str, QPushButton]) -> None:
        """Initialize the form with the given data."""

        pretty_keys: dict = prettyKeys(data_form)

        for key, value in data_form.items():
            if isinstance(value, QPushButton):
                self.formLayout.addRow(pretty_keys[key], value)
            else:
                logging.warning(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name} - QPushButton type not supported: {key}: {value}")
        
        self.formLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
