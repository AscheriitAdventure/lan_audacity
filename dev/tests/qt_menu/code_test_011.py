from dev.project.src.classes.cl_stacked_objects import SDFSP
from dev.project.src.lib.template_tools_bar import *
import sys
import logging
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *



class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SDFSP Demo")
        self.resize(400, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        self.side_panel = SDFSP(debug=True)
        self.side_panel.exchangeContext.connect(self.on_context_changed)
        
        # Widgets de démo
        file_tree = QTreeWidget()
        file_tree.setHeaderLabels(["Files"])
        project = QTreeWidgetItem(file_tree, ["Project"])
        QTreeWidgetItem(project, ["main.py"])
        QTreeWidgetItem(project, ["utils.py"])
        
        properties_tree = QTreeWidget()
        properties_tree.setHeaderLabels(["Property", "Value"])
        QTreeWidgetItem(properties_tree, ["Name", "main.py"])
        QTreeWidgetItem(properties_tree, ["Size", "1.2 KB"])
        
        task_list = QListWidget()
        task_list.addItems(["Task 1", "Task 2", "Task 3"])
        add_task_btn = QPushButton("Add Task")
        task_container = QWidget()
        task_layout = QVBoxLayout(task_container)
        task_layout.addWidget(task_list)
        task_layout.addWidget(add_task_btn)
        
        # Un seul stack avec trois fields
        demo_stack = {
            'stacked_title': 'Explorer',
            'separator': True,
            'shortcut': 'Ctrl+E',
            'fields': [
                {
                    'title': 'Files',
                    'form_list': 'tree-file',
                    'widget': file_tree,
                    'widget_layout': QVBoxLayout(),
                    'visible': True,
                    'actions': [self.on_file_clicked],
                    'description': 'File explorer'
                },
                {
                    'title': 'Tasks',
                    'form_list': 'list-btn',
                    'separator': True,
                    'widget': task_container,
                    'widget_layout': QVBoxLayout(),
                    'visible': True,
                    'actions': [self.on_task_added],
                    'tooltip': 'Manage tasks',
                    'description': 'Task manager'
                },
                {
                    'title': 'Properties',
                    'form_list': 'tree',
                    'widget': properties_tree,
                    'widget_layout': QVBoxLayout(),
                    'visible': True,
                    'description': 'File properties'
                }
            ]
        }
        
        self.side_panel.load_stack_data(DEFAULT_SIDE_PANEL)
        
        layout.addWidget(self.side_panel)
        layout.addWidget(self.log_text)
        
    def on_file_clicked(self, item, column):
        self.log_text.append(f"File clicked: {item.text(column)}")
        
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