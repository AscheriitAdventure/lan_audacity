from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from typing import *
import logging
import inspect


class CardHeader(QWidget):
    def __init__(
            self,
            title: Optional[Union[str, QWidget]] = None,
            icon: Optional[QIcon] = None,
            debug: Optional[bool] = False,
            parent=None):
        super(CardHeader, self).__init__(parent)

        self.debug = debug
        self.title = title
        self.icon = icon

        self.initUI()

    def initUI(self):
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)

        # set the title
        if (self.title or self.icon) is not None:
            self.setTitleUI(self.title, self.icon)
        else:
            logging.warning(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: No title or icon specified")

    def setTitleUI(self, title: Optional[Union[str, QWidget]] = None, icon: Optional[QIcon] = None):
        """Sets the title UI with a string or a widget."""
        if icon is not None:
            lbl = QLabel()
            lbl.setPixmap(icon.pixmap(24, 24))
            self.mainLayout.addWidget(lbl)

        if title is not None:
            if isinstance(title, str):
                lbl = QLabel(title)
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.mainLayout.addWidget(lbl)
            elif isinstance(title, QWidget):
                self.mainLayout.addWidget(title)

        self.mainLayout.addStretch(1)

