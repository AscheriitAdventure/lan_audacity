from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QImage, QPixmap


class Card(QWidget):
    def __init__(
        self,
        icon_card: QIcon = None,
        title: QLabel = None,
        image_path: QImage = None,
        corps_card: any = None,
        parent=None,
    ):
        super().__init__(parent)
        self.layoutCard = QGridLayout(self)
        self.setLayout(self.layoutCard)

        if icon_card or title:
            self.setTitleUI(icon_card, title)

        if image_path:
            self.setImageUI(image_path)

        if corps_card:
            self.setBodyUI(corps_card)

    def setTitleUI(self, icon_card: QIcon = None, title: QLabel = None):
        hbar_title = QHBoxLayout()
        if icon_card:
            icon_label = QLabel()
            icon_label.setPixmap(icon_card.pixmap(24, 24))
            hbar_title.addWidget(icon_label)

        if title:
            hbar_title.addWidget(title)

        hbar_title.addStretch(1)
        hbar_cnt = QWidget()
        hbar_cnt.setLayout(hbar_title)
        self.layoutCard.addWidget(hbar_cnt, 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop)

        # set the separator
        sep = QFrame(self)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        self.layoutCard.addWidget(sep)

    def setImageUI(self, image_path: QImage):
        image_label = QLabel()
        image_label.setPixmap(QPixmap.fromImage(image_path))
        image_label.setAlignment(Qt.AlignCenter)
        self.layoutCard.addWidget(
            image_label, 1, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter
        )

    def setBodyUI(self, corps_card: QWidget):
        self.layoutCard.addWidget(corps_card, 2, 0, 1, 2)
