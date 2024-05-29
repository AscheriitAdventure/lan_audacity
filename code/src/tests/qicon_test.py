# Standard library imports
import sys

# Third party imports
from qtpy.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout
from qtpy.QtCore import QTimer

# Local imports
import qtawesome as qta


class QtAwesomeTest(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.setLayout(layout)

        btn_spin = QPushButton(self)
        anm1 = qta.Spin(btn_spin)
        icon_spin = qta.icon("mdi6.account-settings", color='red', animation=anm1)
        btn_spin.setIcon(icon_spin)

        time_spin = QTimer(self)
        time_spin.singleShot(6000, anm1.start)

        layout.addWidget(btn_spin)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QtAwesomeTest()
    window.show()  # You need to call the show method to display the window
    sys.exit(app.exec_())  # Note the correct method name, it's exec_()
