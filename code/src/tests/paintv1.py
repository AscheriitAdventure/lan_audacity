import sys
from qtpy.QtWidgets import QWidget, QApplication
from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter, QPen


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, e):
        qp = QPainter(self)

        # Dessiner un rectangle
        pen = QPen(Qt.red, 3)
        qp.setPen(pen)
        qp.drawRect(25, 15, 120, 60)

        # Dessiner un cercle
        pen = QPen(Qt.blue, 3)
        qp.setPen(pen)
        qp.drawEllipse(150, 15, 60, 60)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
