from qtpy.QtWidgets import QApplication, QListWidget, QListWidgetItem, QVBoxLayout, QWidget
import qtawesome as qta

class ListWidgetDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        list_widget = QListWidget()

        items = [
            ("Item 1", "fa5s.smile"),
            ("Item 2", "fa5s.frown"),
            ("Item 3", "fa5s.heart"),
            ("Item 4", "fa5s.star"),
        ]

        for text, icon_name in items:
            item = QListWidgetItem(text)
            icon = qta.icon(icon_name)
            item.setIcon(icon)
            list_widget.addItem(item)

        layout.addWidget(list_widget)
        self.setLayout(layout)
        self.setWindowTitle('List Widget with Icons')
        self.resize(300, 200)

if __name__ == '__main__':
    app = QApplication([])
    demo = ListWidgetDemo()
    demo.show()
    app.exec_()