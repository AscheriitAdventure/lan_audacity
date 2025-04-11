from typing import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import inspect

from tests.cardframe_tests import *

tmp_d: dict = {
    "style_sheet": "border: 3px solid #E7E9EB; border-radius: 10px;"
}

class TestFrame(QFrame):
    def __init__(self, debug: Optional[bool] = False, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setLineWidth(10)
        self.setMidLineWidth(5)
        self.setStyleSheet("background-color: lightblue; border-radius: 10px;")
        # self.debug = debug
        self.setContentsMargins(5, 5, 5, 5)

class DemoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Démo Tests Frame")
        self.setGeometry(100, 100, 800, 600)

        c_widget = QWidget()
        c_layout = QGridLayout(c_widget)
        c_layout.setContentsMargins(1, 1, 1, 1)
        c_layout.setSpacing(3)
        self.setCentralWidget(c_widget)
        # self.setStyleSheet("background-color: Black;")

        # Créer quelques objets de test
        test_frame1 = TestFrame(debug=True)
        c_layout.addWidget(test_frame1, 0, 0)
        test_frame2 = Card_2(debug=False)

        # Ajouter des labels de test avec des couleurs distinctes
        top = QLabel("TOP")
        top.setStyleSheet("background-color: red; color: white;")
        top.setMinimumHeight(40)

        left = QLabel("LEFT")
        left.setStyleSheet("background-color: green; color: white;")
        left.setMinimumWidth(60)

        test_frame2.setAllParts(top, left, QLabel("center"), QLabel("right"), QLabel("bottom"))
        c_layout.addWidget(test_frame2, 1, 0)
        test_frame3 = CardFrame(debug=True)
        test_frame3.setStyleSheet("border: 3px solid red; border-radius: 10px;")
        test_frame3.setAllCards(top, left, QLabel("center"), QLabel("right"), QLabel("bottom"))
        c_layout.addWidget(test_frame3, 0, 1)


if __name__ == "__main__":
    app = QApplication([])
    window = DemoApp()
    window.show()
    app.exec_()
