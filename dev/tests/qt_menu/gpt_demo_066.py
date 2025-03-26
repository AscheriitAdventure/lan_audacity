from qtpy.QtWidgets import QApplication, QLabel, QWidget, QGridLayout
from qtpy.QtGui import QPixmap, QDrag, QDragEnterEvent, QDropEvent
from qtpy.QtCore import Qt, QMimeData, QPoint


class DraggableLabel(QLabel):
    def __init__(self, text, width, height, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(width, height)
        self.setStyleSheet("background-color: lightblue; border: 1px solid black;")
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(self.text())  # On peut stocker d'autres infos ici
            drag.setMimeData(mime)
            drag.exec_(Qt.DropAction.MoveAction)


class DropGridWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.mainLayout = QGridLayout(self)
        self.setLayout(self.mainLayout)
        self.items = {}  # Stocke les items avec leurs positions

        # Ajout de quelques éléments de tailles différentes
        self.add_draggable_item("A", 80, 80, 0, 0)
        self.add_draggable_item("B", 100, 50, 0, 1)
        self.add_draggable_item("C", 60, 120, 1, 0)
        self.add_draggable_item("D", 50, 60, 1, 1)

    def add_draggable_item(self, text, width, height, row, col):
        label = DraggableLabel(text, width, height, self)
        self.mainLayout.addWidget(label, row, col)
        self.items[label] = (row, col)

    def dragEnterEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        pos = event.pos()
        widget = event.source()

        if widget and isinstance(widget, DraggableLabel):
            # Trouver la position dans la grille la plus proche
            for lbl, (row, col) in self.items.items():
                cell_widget = self.mainLayout.itemAtPosition(row, col).widget()
                if cell_widget == widget:  # Éviter de repositionner le même widget
                    continue

                rect = cell_widget.geometry()
                if rect.contains(pos):
                    # Récupérer le rowSpan et columnSpan des deux widgets
                    old_row, old_col = self.items[widget]
                
                    # Récupérer les informations de disposition pour les deux widgets
                    widget_index = self.mainLayout.indexOf(widget)
                    target_index = self.mainLayout.indexOf(cell_widget)

                    # Utiliser getItemPosition qui retourne (row, column, rowSpan, columnSpan)
                    _, _, widget_row_span, widget_col_span = self.mainLayout.getItemPosition(widget_index)
                    _, _, target_row_span, target_col_span = self.mainLayout.getItemPosition(target_index)
                
                    # Supprimer les widgets actuels de la grille pour éviter les conflits
                    self.mainLayout.removeWidget(widget)
                    self.mainLayout.removeWidget(cell_widget)
                
                    # Ajouter les widgets aux nouvelles positions avec leurs spans respectifs
                    self.mainLayout.addWidget(widget, row, col, target_row_span, target_col_span)
                    self.mainLayout.addWidget(cell_widget, old_row, old_col, widget_row_span, widget_col_span)

                    # Mettre à jour le dictionnaire des positions
                    self.items[widget] = (row, col)
                    self.items[cell_widget] = (old_row, old_col)
                    break

        event.acceptProposedAction()

if __name__ == "__main__":
    app = QApplication([])
    window = DropGridWidget()
    window.show()
    app.exec_()
