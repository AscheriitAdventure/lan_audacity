from dev.project.src.classes.cl_stacked_objects import SDFSP
from dev.project.src.lib.template_tools_bar import *
import sys
import os
import logging
import inspect
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *


class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SDFSP Démo")
        self.resize(400, 800)

        self.template: dict = DEFAULT_SIDE_PANEL
        self.sketchs: list[dict] = []

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        self.side_panel = SDFSP(debug=True)
        self.side_panel.exchangeContext.connect(self.on_context_changed)

        # Widgets de démo
        default_path = os.getcwd()
        default_list_obj = [
            {
                "name": "Site 1",
                "childs": [
                    {"name": "001"},
                    {"name": "002"},
                    {"name": "003"},
                    {"name": "004"},
                    {"name": "005"},
                    {"name": "006"}
                ]
            },
            {
                "name": "Site 25",
                "childs": [
                    {"name": "251"},
                    {"name": "252"},
                    {"name": "253"}
                ]
            },
        ]

        # Overwriting template with data in sketchs
        for field in self.template['fields']:
            field_form = field.get('form_list')
            if field_form:
                sketch_data = {"field_name": field['title']}

                if field_form == 'tree-file':
                    sketch_data["widget_data"] = default_path
                    field['actions'].append(self.on_file_clicked)
                elif field_form == 'tree':
                    sketch_data["widget_data"] = default_list_obj
                    field['actions'].append(self.on_tree_item_clicked)
                elif field_form == 'list-btn':
                    sketch_data["widget_data"] = ["Tâche 1", "Tâche 2", "Tâche 3"]
                    field['actions'].extend([
                        {
                            'icon': '➕',
                            'callback': self.on_task_added,
                            'tooltip': 'Ajouter une tâche'
                        }
                    ])
                else:
                    logging.warning(
                        f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {field_form} Unknown")
                    continue

                self.sketchs.append(sketch_data)
                field['widget_data'] = sketch_data["widget_data"]

        self.side_panel.load_stack_data(self.template)

        layout.addWidget(self.side_panel)
        layout.addWidget(self.log_text)

    def create_tree_items(self, data_list, parent=None):
        """Crée récursivement les items de l'arbre"""
        items = []
        for data in data_list:
            item = QTreeWidgetItem([data["name"]])
            if "childs" in data:
                child_items = self.create_tree_items(data["childs"])
                for child in child_items:
                    item.addChild(child)
            items.append(item)
        return items

    def on_file_clicked(self, item, column):
        self.log_text.append(f"File clicked: {item.text(column)}")

    def on_tree_item_clicked(self, item, column):
        self.log_text.append(f"Tree item clicked: {item.text(column)}")

    def on_task_added(self):
        self.log_text.append("New task added")

    def on_context_changed(self, context):
        self.log_text.append(f"Context changed: {str(context)}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    sys.exit(app.exec())