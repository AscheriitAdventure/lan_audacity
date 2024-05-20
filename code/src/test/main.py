import sys
import qtawesome as qta
from qtpy.QtWidgets import *
from qtpy.QtGui import *


class WindowTest(QWidget):
    def __init__(self):
        super().__init__()

        self.myListWidget1 = QListWidget()
        self.myListWidget2 = QListWidget()
        self.myListWidget2.setViewMode(QListWidget.IconMode)
        self.myListWidget1.setAcceptDrops(True)
        self.myListWidget1.setDragEnabled(True)
        self.myListWidget2.setAcceptDrops(True)
        self.myListWidget2.setDragEnabled(True)
        self.setGeometry(300, 350, 500, 300)
        self.myLayout = QHBoxLayout()
        self.myLayout.addWidget(self.myListWidget1)
        self.myLayout.addWidget(self.myListWidget2)

        l1 = QListWidgetItem(QIcon(qta.icon('fa5b.cuttlefish', color='RoyalBlue')), "C")
        l2 = QListWidgetItem(QIcon(qta.icon('fa5b.docker', color='Cyan')), "Docker")
        l3 = QListWidgetItem(QIcon(qta.icon('fa5b.java', color='Grey')), "Java")
        l4 = QListWidgetItem(QIcon(qta.icon('fa5b.python', color='Grey')), "Python")

        self.myListWidget1.insertItem(1, l1)
        self.myListWidget1.insertItem(2, l2)
        self.myListWidget1.insertItem(3, l3)
        self.myListWidget1.insertItem(4, l4)

        QListWidgetItem(QIcon(qta.icon('fa5b.html5', color='Orange')), "HTLM", self.
                        myListWidget2)
        QListWidgetItem(QIcon(qta.icon('fa5b.css3-alt', color='Blue')), "CSS", self.
                        myListWidget2)
        QListWidgetItem(QIcon(qta.icon('fa5b.js', color='Yellow')), "Javascript", self.
                        myListWidget2)

        self.setLayout(self.myLayout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audacity - drag & drop")
        self.drag_drop_window = WindowTest()

        self.setCentralWidget(self.drag_drop_window)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
