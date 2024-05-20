import sys
from PyQt6.QtWidgets import * # type: ignore
from PyQt6.QtCore import *  # type: ignore
from PyQt6.QtGui import *  # type: ignore
import qtawesome as qta


class IconObj:
    def __init__(
            self,
            icon: any = qta.icon('fa5r.question-circle'),
            flag: str = 'Objet Non-Identifié'):
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
        ico_home = IconObj(icon=qta.icon('fa5s.home'), flag='Accueil')
        btn_home = Btn(ico_home)
        layout.addWidget(btn_home, 0, 0)

        # Ajout d'un bouton Dossier avec une icône de dossier
        ico_folder = IconObj(icon=qta.icon('fa5s.folder', options=[{'active': 'fa5s.folder-open', 'color': 'orange'}]), flag='Dossier')
        btn_folder = Btn(ico_folder)
        layout.addWidget(btn_folder, 0, 1)

        # Ajout d'un bouton Cloud avec une icône de nuage et réseau
        ico_cloud = IconObj(icon=qta.icon('mdi6.cloud-outline', 'fa5s.network-wired',
                                          options=[{'scale_factor': 1.5, 'color': 'blue'}, {'scale_factor': 0.75}]),
                            flag='Objets Trouvés')
        btn_cloud = Btn(ico_cloud)
        layout.addWidget(btn_cloud, 1, 0)

        # Ajout d'un bouton Carte avec une icône de carte
        ico_map = IconObj(icon=qta.icon('fa5s.map', 'fa5s.map-signs',
                                        options=[{'scale_factor': 1.5, 'color': 'grey'}, {'scale_factor': 0.5, 'color': 'green'}]),
                          flag='Aperçu Carte')
        btn_map = Btn(ico_map)
        layout.addWidget(btn_map, 1, 1)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Créer la fenêtre principale
    window = MainWindow()
    window.show()
    # Démarrer la boucle d'événements
    sys.exit(app.exec())

