from typing import List, Dict, Any, Optional, ClassVar, Union
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
import logging
import inspect
import os
from .sdfd import SDFD


class SDFSP(SDFD):
    """
        Stacked Dynamic Factory Side Panel
    """
    fileDropped: ClassVar[Signal] = Signal(
        str, str)  # source_path, destination_path
    fileClicked: ClassVar[Signal] = Signal(str)  # path_clicked

    def __init__(self, debug: bool = False, parent: Optional[QWidget] = None):
        super(SDFSP, self).__init__(
            layout_field=SDFD.StackLayout.VERTICAL, debug=debug, parent=parent)

        self.initUI()

    def _createSpecificFieldWidget(self, field: Dict[str, Any]) -> QWidget:
        """Crée le widget spécifique selon le form_list"""
        form_type = field.get('form_list')
        widget_data = field.get('widget_data', os.getcwd())

        if form_type == 'tree-file':
            widget = QTreeView()
            if widget_data and os.path.exists(widget_data):
                model = QFileSystemModel()
                model.setRootPath(widget_data)
                model.setFilter(QDir.Filter.NoDotAndDotDot |
                                QDir.Filter.AllDirs | QDir.Filter.Files)
                widget.setModel(model)
                widget.setRootIndex(model.index(widget_data))

                # Configuration de base
                widget.setColumnHidden(1, True)  # Size
                widget.setColumnHidden(2, True)  # Type
                widget.setColumnHidden(3, True)  # Date Modified
                widget.setSortingEnabled(True)
                widget.sortByColumn(0, Qt.SortOrder.AscendingOrder)
                widget.setAnimated(True)
                widget.setIndentation(20)
                widget.setHeaderHidden(True)

                # Configuration drag & drop
                widget.setDragEnabled(True)
                widget.setAcceptDrops(True)
                widget.setDropIndicatorShown(True)
                widget.setDragDropMode(
                    QAbstractItemView.DragDropMode.InternalMove)
                widget.setSelectionMode(
                    QTreeView.SelectionMode.ExtendedSelection)

                # Connecter les signaux pour double-clic
                widget.doubleClicked.connect(lambda index: self.itemDoubleClicked.emit({
                    'type': 'file',
                    'path': model.filePath(index),
                    'is_dir': model.isDir(index)
                }))

                # Connecter les signaux pour drag & drop
                widget.model().rowsInserted.connect(
                    lambda parent, first, last: self.fileDropped.emit(
                        model.filePath(model.index(first, 0, parent)),
                        model.filePath(parent)
                    )
                )

            return widget

        elif form_type == 'list-btn':
            container = QWidget()
            layout = QVBoxLayout(container)
            list_widget = QListWidget()
            if isinstance(widget_data, list):
                list_widget.addItems(widget_data)
            layout.addWidget(list_widget)
            return container

        elif form_type == 'tree':
            widget = QTreeView()
            model = QStandardItemModel()
            widget.setModel(model)
            widget.setRootIsDecorated(True)
            widget.setHeaderHidden(True)
            model.setColumnCount(2)
            widget.setColumnHidden(1, True)
            widget.setEditTriggers(
                QAbstractItemView.EditTrigger.NoEditTriggers)
            if isinstance(widget_data, list):
                for item_data in widget_data:
                    self.addTreeItems(model.invisibleRootItem(), item_data)

            # Connecter le signal pour double-clic
            widget.doubleClicked.connect(lambda index: self.itemDoubleClicked.emit({
                'type': 'network',
                # filter on 'path'
                'path': index.sibling(index.row(), 1).data(),
                # filter on 'alias'
                'name': index.sibling(index.row(), 0).data(),
                'id': index.row()
            }))

            return widget
        return QWidget()

    def addTreeItems(self, parentItem: QTreeView, data: Dict[str, Any]) -> None:
        """Ajoute récursivement les items à l'arbre"""
        if isinstance(data, dict):
            item = QStandardItem(data.get('name', ''))
            if isinstance(parentItem, QStandardItem):
                parentItem.appendRow(item)
            else:
                parentItem.model().appendRow(item)
            if 'childs' in data and isinstance(data['childs'], list):
                for child in data['childs']:
                    self.addTreeItems(item, child)

