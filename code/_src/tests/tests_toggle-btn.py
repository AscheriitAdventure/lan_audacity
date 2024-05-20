from qtpy.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import qtawesome as qta

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Bouton avec icône et texte')

        # Layout vertical pour organiser les widgets
        layout = QVBoxLayout()

        # Définit le layout principal de la fenêtre
        self.setLayout(layout)
        label_ls_btn: list[str] = ['Font Awesome! (regular)', 'Elusive Icons!', 'Material Design Icons!',
                                   'Phosphor!', 'Remix Icon!', 'Codicons!']

        # Création du bouton avec icône et texte
        fa5_icon = qta.icon('fa5.flag')
        self.btn_toggle = QPushButton(fa5_icon, label_ls_btn[0], self)
        self.btn_toggle.setCheckable(True)  # Rend le bouton basculable (on/off)
        self.btn_toggle.setToolTip(label_ls_btn[0])
        layout.addWidget(self.btn_toggle)

        # Connecte le signal "clicked" du bouton à la méthode "toggle_text_visibility"
        self.btn_toggle.clicked.connect(lambda: self.toggle_text_visibility(label_ls_btn))

        # or Elusive Icons:
        asl_icon = qta.icon('ei.asl')
        self.elusive_button = QPushButton(asl_icon, label_ls_btn[1])
        layout.addWidget(self.elusive_button)

        # or Material Design Icons:
        apn_icon = qta.icon('mdi6.access-point-network')
        self.mdi6_button = QPushButton(apn_icon, label_ls_btn[2])
        layout.addWidget(self.mdi6_button)

        # or Phosphor:
        mic_icon = qta.icon('ph.microphone-fill')
        self.ph_button = QPushButton(mic_icon, label_ls_btn[3])
        layout.addWidget(self.ph_button)

        # or Remix Icon:
        truck_icon = qta.icon('ri.truck-fill')
        self.ri_button = QPushButton(truck_icon, label_ls_btn[4])
        layout.addWidget(self.ri_button)

        # or Microsoft's Codicons:
        squirrel_icon = qta.icon('msc.squirrel')
        self.msc_button = QPushButton(squirrel_icon, label_ls_btn[5])
        layout.addWidget(self.msc_button)

        # Affiche la fenêtre
        self.show()

    def toggle_text_visibility(self, name_label: list):
        # Récupère l'état actuel du bouton (coché ou non)
        checked = self.btn_toggle.isChecked()

        # Modifie la visibilité du texte du bouton en fonction de son état
        if checked:
            self.btn_toggle.setText('')
            self.btn_toggle.setFixedSize(32, 32)
            self.elusive_button.setText('')
            self.elusive_button.setFixedSize(32, 32)
            self.ri_button.setText('')
            self.ri_button.setFixedSize(32, 32)
            self.msc_button.setText('')
            self.msc_button.setFixedSize(32, 32)
            self.ph_button.setText('')
            self.ph_button.setFixedSize(32, 32)
            self.mdi6_button.setText('')
            self.mdi6_button.setFixedSize(32, 32)
        else:
            self.btn_toggle.setText(name_label[0])
            self.btn_toggle.setFixedSize(180, 32)
            self.elusive_button.setText(name_label[1])
            self.elusive_button.setFixedSize(180, 32)
            self.mdi6_button.setText(name_label[2])
            self.mdi6_button.setFixedSize(180, 32)
            self.ph_button.setText(name_label[3])
            self.ph_button.setFixedSize(180, 32)
            self.ri_button.setText(name_label[4])
            self.ri_button.setFixedSize(180, 32)
            self.msc_button.setText(name_label[5])
            self.msc_button.setFixedSize(180, 32)


if __name__ == '__main__':
    app = QApplication([])  # Crée l'application Qt
    widget = MyWidget()  # Crée une instance de la classe MyWidget
    app.exec_()  # Exécute l'application
