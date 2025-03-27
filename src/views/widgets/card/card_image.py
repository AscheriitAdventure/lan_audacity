from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from typing import *
import logging
import inspect


class CardImage(QWidget):
    def __init__(
            self,
            list_image: Optional[Union[List[QImage], QImage]] = None,
            debug: bool = False,
            parent=None):
        super(CardImage, self).__init__(parent)

        self.debug = debug
        self.listPicture: List[QImage] = list_image if list_image is not None else [
        ]

        self.initUI()

    def initUI(self):
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)

        if len(self.listPicture) == 1:
            self.setImageUI(self.listPicture[0])
        elif len(self.listPicture) > 1:
            self.setListImageUI(self.listPicture)

    def setImageUI(self, image_card: QImage):
        """Sets the image UI with an image."""
        self.mainLayout.addStretch(1)
        lbl = QLabel()
        lbl.setPixmap(QPixmap.fromImage(image_card))
        self.mainLayout.addWidget(lbl)
        self.mainLayout.addStretch(1)

    def setListImageUI(self, image_card: list[QImage], orientation: Qt.LayoutDirection = Qt.LayoutDirection.LeftToRight):
        """
            Sets the image UI with a list of images.
            Set a carousel of images.
        """
        if self.debug:
            logging.debug(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Setting list of images")
            logging.warning(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Not implemented yet")
