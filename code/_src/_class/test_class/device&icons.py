import qtawesome as qta
import sys
from qtpy.QtWidgets import *


class IconQta:
    def __init__(self, name: str = "Objet Non Identifié"):
        self.__icon = qta.icon("fa5s.question", color="blue")
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, var: str):
        if var != "" or var is not None:
            self.__name = var

    @property
    def icon(self):
        return self.__icon

    @icon.setter
    def icon(self, var: any):
        if var is not None:
            self.__icon = var

    def __str__(self):
        return self.name

class MainBtn(QPushButton):
    def __init__(self, *args, **kwargs):
        super(MainBtn, self).__init__(*args, **kwargs)
        self.initUI()
    
    def initUI(self):
        self.setFixedSize(100, 100)
        self.setIconSize(self.size())
        self.setIcon(qta.icon("fa5s.question", color="blue"))

class App(QApplication):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.window = QWidget()
        self.window.setWindowTitle("Network Device")
        self.window.setGeometry(100, 100, 400, 100)

        self.layout = QVBoxLayout()
        self.window.setLayout(self.layout)

        self.device = IconQta()
        self.device.icon = qta.icon(
            "fa5s.dice-d20",
            "fa5s.spider",
            options=[
                {"color": "black"},
                {"scale_factor": 0.85, "color": "gold"},
            ],
        )
        self.label = QLabel(str(self.device))
        self.label.setPixmap(self.device.icon.pixmap(32, 32))
        self.layout.addWidget(self.label)

        self.window.show()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())
