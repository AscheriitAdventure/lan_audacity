import sys
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import qtawesome as qta


class IconObj:
    def __init__(self, icon: any = qta.icon('fa5r.question-circle'),flag: str = 'Objet Non-Identifié'):
        self.__pix_icon = icon
        self.__pix_flag = flag

    @property
    def pix_icon(self):
        return self.__pix_icon

    @pix_icon.setter
    def pix_icon(self, value: any):  # type: ignore
        self.__pix_icon = value

    @property
    def flag_icon(self):
        return self.__pix_flag

    @flag_icon.setter
    def flag_icon(self, value: str):
        if value != '' or value is not None:
            self.__pix_flag = value


class Btn(QPushButton):
    def __init__(self, icon: IconObj, parent=None):
        super(Btn, self).__init__(parent)
        self.setIcon(icon.pix_icon)
        self.setIconSize(QSize(16, 16))
        self.setFixedSize(self.sizeHint())
        self.setToolTip(icon.flag_icon)  # Utilisation de setToolTip pour l'infobulle


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('PyQt QPushButton Widget')
        self.setGeometry(100, 100, 400, 300)

        layout = QGridLayout(self)

        # Ajout d'un bouton Accueil avec une icône de maison
        # ico_home = IconObj(icon=qta.icon('fa5s.times'), flag='Accueil')
        obj_icon = qta.icon('fa5s.times')
        btn_home = QPushButton(obj_icon, 'Accueil')
        layout.addWidget(btn_home, 0, 0)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Créer la fenêtre principale
    window = MainWindow()
    window.show()
    # Démarrer la boucle d'événements
    sys.exit(app.exec())

