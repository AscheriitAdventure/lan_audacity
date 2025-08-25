"""
    This is a test file for the object CardUI
"""

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

from typing import Optional, Any


class CardUI(QWidget):
    def __init__(
            self,
            icon_card: Optional[QIcon] = None,
            title_card: Optional[QWidget] = None,
            img_card: Optional[QImage] = None,
            corps_card: Any = None,
            parent=None
    ):
        super().__init__(parent=parent)
        self.layout = QGridLayout(self)  # Initialisation de l'attribut layout
        self.setLayout(self.layout)

        if icon_card or title_card:
            self.setTitleUI(icon_card, title_card)

        if img_card:
            self.setImageUI(img_card)

        if corps_card:
            self.setBodyUI(corps_card)

        self.set_cssParameters()

    def setTitleUI(self, icon_card: Optional[QIcon] = None, title: Optional[QWidget] = None):
        """Sets the title UI with an optional icon and title label."""
        hbar_title = QHBoxLayout()
        if icon_card:
            icon_label = QLabel()
            icon_label.setPixmap(icon_card.pixmap(24, 24))
            hbar_title.addWidget(icon_label)

        if title and isinstance(title, QWidget):
            hbar_title.addWidget(title)

        hbar_title.addStretch(1)
        hbar_cnt = QWidget()
        hbar_cnt.setLayout(hbar_title)
        self.layout.addWidget(hbar_cnt, 0, 0, 1, 2, Qt.AlignTop)

        # set the separator
        sep = QFrame(self)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(sep)

    def setImageUI(self, image_path: QImage, legend: Optional[QWidget] = None):
        """Sets the image UI with the provided QImage."""
        image_legend = legend
        image_label = QLabel()
        image_label.setPixmap(QPixmap.fromImage(image_path))
        # image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(image_label, 2, 0, 1, 2, Qt.AlignHCenter)

    def setBodyUI(self, corps_card: QWidget):
        """Sets the body UI with the provided QWidget."""
        self.layout.addWidget(corps_card, 3, 0, 1, 2)

    def set_cssParameters(self, css_params: Optional[list[str]] = None):
        """Sets the CSS parameters for the CardUI widget."""
        if css_params is None:
            css_params = [
                "background-color: #e7ebed;",
                # "border: 1px solid Black;",
                "border-radius: 4px;"
            ]
        self.setStyleSheet(" ".join(css_params))


class CardUI_V2(QWidget):
    def __init__(
            self,
            icon_card: Optional[QIcon] = None,
            title_card: Optional[QWidget] = None,
            img_card: Optional[QImage] = None,
            corps_card: Any = None,
            parent=None
    ):
        super().__init__(parent=parent)
        # Container for the card
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)

        # VARIABLES
        self.iconCardLabel = icon_card
        self.titleCardLabel = title_card
        self.imgCardLabel = img_card
        self.bodyCardLabel = corps_card

        # Head Title Layout
        self.titleLayout = QHBoxLayout()
        self.titleLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addLayout(self.titleLayout)

        # Image Card Layout
        self.imageLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.imageLayout)

        # Body Card Layout
        self.bodyLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.bodyLayout)

        # Set the card UI
        self.set_headTitle()
        self.set_imageCard()
        self.set_bodyCard()

        self.set_cssParameters()

    def set_headTitle(self, icon_card: Optional[QIcon] = None, title: Optional[QWidget] = None):
        
        if icon_card is not None:
            self.iconCardLabel = icon_card
        
        if title is not None:
            self.titleCardLabel = title
        
        if self.iconCardLabel or self.titleCardLabel:
            if self.iconCardLabel:
                icon_label = QLabel()
                icon_label.setPixmap(self.iconCardLabel.pixmap(24, 24))
                self.titleLayout.addWidget(icon_label)
            
            if self.titleCardLabel and isinstance(self.titleCardLabel, QWidget):
                self.titleLayout.addWidget(self.titleCardLabel)

            self.titleLayout.addStretch(1)

            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            self.mainLayout.addWidget(separator)
        
        else:
            self.titleLayout.hide()

    def set_imageCard(self, image_path: Optional[QImage] = None, legend: Optional[QWidget] = None):
        if image_path is not None:
            self.imgCardLabel = image_path
        
        legendImgLabel = legend
        
        if self.imgCardLabel:
            image_label = QLabel()
            image_label.setPixmap(QPixmap.fromImage(self.imgCardLabel))
            self.imageLayout.addWidget(image_label)
        
        else:
            self.imageLayout.hide()
            
    def set_bodyCard(self, corps_card: Optional[QWidget] = None):
        if corps_card is not None:
            self.bodyCardLabel = corps_card
            
        if self.bodyCardLabel:
            self.bodyLayout.addWidget(self.bodyCardLabel)
        
        else:
            self.bodyLayout.hide()

    def set_cssParameters(self, css_params: Optional[list[str]] = None):
        """Sets the CSS parameters for the CardUI widget."""
        if css_params is None:
            css_params = [
                "background-color: #e7ebed;",
                # "border: 1px solid;",
                "border-radius: 4px;"
            ]
        self.setStyleSheet(" ".join(css_params))
