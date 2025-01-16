from qtpy.QtGui import QKeySequence
from qtpy.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QMenuBar
import json
import sys
# FORMAT_QMENU_PATH = "D:\\lan_audacity\\dev\\tests\\qt_menu\\format.json"
FORMAT_QMENU_PATH = "D:\\lan_audacity\\dev\\tests\\qt_menu\\format_prod_test.json"

def load_menu_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        menu_data = json.load(file)
    return menu_data


def create_menu(menu_bar, menu_data, parent=None):
    for menu_item in menu_data:
        if menu_item["separator"]:
            menu.addSeparator()
        menu = QMenu(menu_item["title"], menu_bar)
        if menu_item["icon"]:
            menu.setIcon(menu_item["icon"])

        for action_item in menu_item.get("actions", []):
            action = QAction(action_item["text"], menu)
            if action_item["shortcut"]:
                action.setShortcut(QKeySequence(action_item["shortcut"]))
            if action_item["tip"]:
                action.setStatusTip(action_item["tip"])
            action.setCheckable(action_item["checkable"])
            action.setEnabled(action_item["enabled"])
            menu.addAction(action)
            if action_item["separator"]:
                menu.addSeparator()
        
        menu_bar.addMenu(menu)
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic QMenu from JSON")
        menu_bar = self.menuBar()
        menu_data = load_menu_from_json(FORMAT_QMENU_PATH)
        create_menu(menu_bar, menu_data, self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
