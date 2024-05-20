from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag


class DragButton(QPushButton):

    def mouseMoveEvent(self, e):

        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        self.blayout = QHBoxLayout()
        for l in ['A', 'B', 'C', 'D']:
            btn = DragButton(l)
            self.blayout.addWidget(btn)

        self.setLayout(self.blayout)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()

        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            if pos.x() < w.x() + w.size().width() // 2:
                # We didn't drag past this widget.
                # insert to the left of it.
                self.blayout.insertWidget(n-1, widget)
                break

        e.accept()


app = QApplication([])
w = Window()
w.show()

app.exec_()