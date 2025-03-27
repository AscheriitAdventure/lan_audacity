from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from typing import *
import logging
import inspect

class CardFooter(QWidget):
    def __init__(
            self,
            debug: bool = False,
            content: Optional[QWidget] = None,
            parent=None):
        super(CardFooter, self).__init__(parent)

        self.debug = debug
        self.contentWidget = content

        self.initUI()

    def initUI(self):
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)

        # set the separator
        sep = QFrame(self)
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        self.mainLayout.addWidget(sep)

        # set the content
        if self.contentWidget is not None:
            self.setContent(self.contentWidget)

    def setContent(self, content: QWidget):
        self.mainLayout.addWidget(content)

