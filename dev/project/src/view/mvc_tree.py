from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from typing import ClassVar, Signal, Any
from dev.project.src.classes.welcome_tab import EditorTab, TabType

import logging
import inspect
import os

class TreeViewController:
    def __init__(self, widget, debug=False):
        self.main_window = widget
        self.last_file_path = None
        self.last_object_path = None
        self.debug = debug
        
    def handle_single_click(self, index: QModelIndex) -> None:
        """
        Gère le simple clic sur un TreeView
        Args:
            index (QModelIndex): Index du modèle cliqué
        """
        model = index.model()
        
        if isinstance(model, QFileSystemModel):
            self.last_file_path = model.filePath(index)
            if self.debug:
                logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: File path stored: {self.last_file_path}")
            
        elif isinstance(model, QStandardItemModel):
            # Capture la hiérarchie de l'objet
            item_path = []
            current = index
            while current.isValid():
                item_path.insert(0, current.data())
                current = current.parent()
            self.last_object_path = '/'.join(item_path)
            if self.debug:
                logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Object path stored: {self.last_object_path}")
            
        else:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Unsupported tree model type: {type(model)}")
            
    def handle_double_click(self, index: QModelIndex) -> None:
        """
        Gère le double clic sur un TreeView
        Args:
            index (QModelIndex): Index du modèle double-cliqué
        """
        model = index.model()
        
        if isinstance(model, QFileSystemModel):
            file_path = model.filePath(index)
            
            if model.isDir(index):
                # Trouve le TreeView parent
                tree_view = self.main_window.findChild(QTreeView)
                if tree_view:
                    if tree_view.isExpanded(index):
                        tree_view.collapse(index)
                    else:
                        tree_view.expand(index)
            else:
                # Vérifie si le fichier est déjà ouvert dans un onglet
                for tab in self.main_window.primary_center.get_tabs_by_type(TabType.EDITOR):
                    if isinstance(tab, EditorTab) and tab.file_path == file_path:
                        self.main_window.primary_center.setCurrentWidget(tab)
                        return
                        
                # Si non ouvert, crée un nouvel onglet
                self.main_window.open_file_in_editor(file_path)
                
            self.last_file_path = file_path
            
        elif isinstance(model, QStandardItemModel):
            item_path = []
            current = index
            while current.isValid():
                item_path.insert(0, current.data())
                current = current.parent()
            self.last_object_path = '/'.join(item_path)
            
            # TODO: Implémenter la logique d'ouverture des objets réseau
            
        else:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Unsupported tree model type: {type(model)}")

class CustomTreeFile(QTreeView):
    """Widget TreeView personnalisé pour la gestion des fichiers avec drag & drop"""
    fileDropped = Signal(str, str)  # source_path, destination_path
    fileClicked = Signal(str)  # path_clicked
    
    def __init__(self, root_path):
        super().__init__()
        self.setup_model(root_path)
        self.setup_drag_drop()
        
    def setup_model(self, root_path):
        """Configure le modèle de système de fichiers"""
        self.model = QFileSystemModel()
        self.model.setRootPath(root_path)
        self.model.setFilter(QDir.Filter.NoDotAndDotDot | QDir.Filter.AllDirs | QDir.Filter.Files)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(root_path))
        self.model.setReadOnly(False)
        
        # Configuration de base
        self.setColumnHidden(1, True)  # Size
        self.setColumnHidden(2, True)  # Type
        self.setColumnHidden(3, True)  # Date Modified
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.setAnimated(True)
        self.setIndentation(20)
        self.setHeaderHidden(True)
        
        # Connecter le signal clicked
        self.clicked.connect(self._handle_click)
        
    def _handle_click(self, index):
        """Gère les clics sur les éléments"""
        path = self.model.filePath(index)
        self.fileClicked.emit(path)
        
    def setup_drag_drop(self):
        """Configure les paramètres de drag & drop"""
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Gère l'entrée d'un drag"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
            
    def dragMoveEvent(self, event: QDragMoveEvent):
        """Gère le mouvement pendant un drag"""
        if event.mimeData().hasUrls():
            drop_index = self.indexAt(event.pos())
            if drop_index.isValid():
                if self.model.isDir(drop_index):
                    event.acceptProposedAction()
                    return
            event.ignore()
        else:
            event.ignore()
            
    def dropEvent(self, event: QDropEvent):
        """Gère le drop des fichiers"""
        if event.mimeData().hasUrls():
            drop_index = self.indexAt(event.pos())
            if not drop_index.isValid():
                return
                
            destination_path = self.model.filePath(drop_index)
            if not self.model.isDir(drop_index):
                destination_path = QFileInfo(destination_path).dir().absolutePath()
                
            for url in event.mimeData().urls():
                source_path = url.toLocalFile()
                if not source_path:
                    continue
                    
                try:
                    source_file = QFile(source_path)
                    file_name = QFileInfo(source_path).fileName()
                    destination_file = QDir(destination_path).filePath(file_name)
                    
                    if QFile.exists(destination_file):
                        # Gestion des doublons
                        base_name = QFileInfo(file_name).baseName()
                        extension = QFileInfo(file_name).completeSuffix()
                        counter = 1
                        while QFile.exists(destination_file):
                            new_name = f"{base_name}_{counter}.{extension}"
                            destination_file = QDir(destination_path).filePath(new_name)
                            counter += 1
                    
                    if source_file.rename(destination_file):
                        self.fileDropped.emit(source_path, destination_file)
                    else:
                        logging.error(f"Erreur lors du déplacement: {source_path}")
                        
                except Exception as e:
                    logging.error(f"Erreur: {str(e)}")
                    
            event.acceptProposedAction()
        else:
            event.ignore()

class CTV(QTreeView):
    """Custom Tree View"""
    objCliked: ClassVar[Signal] = Signal(any)
    objDropped: ClassVar[Signal] = Signal(any, any)

    def __init__(self, debug=False, parent=None):
        super().__init__(parent)
        self.debug = debug
        self.setup_model()
    
    def setup_model(self, model = QAbstractItemModel) -> None:
        self.setModel(model)
        self.setHeaderHidden(True)
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.setAnimated(True)
        self.setIndentation(20)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        
        # Connecter le signal clicked
        self.clicked.connect(self._handle_click)
        self.doubleClicked.connect(self._handle_double_click)
    
    def _handle_click(self, index: QModelIndex):
        """Gère les clics sur les éléments"""
        if isinstance(index.model(), QFileSystemModel):
            item = index.model().filePath(index)
        elif isinstance(index.model(), QStandardItemModel):
            item_path = []
            current = index
            while current.isValid():
                item_path.insert(0, current.data())
                current = current.parent()
            item = '/'.join(item_path)
        elif isinstance(index.model(), QAbstractItemModel):
            item = index.model().data(index)
        else:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Unsupported tree model type: {type(index.model())}")
            return
        
        self.objCliked.emit(item)
    
    def _handle_double_click(self, index: QModelIndex) -> None:
        """Gère les double-clics sur les éléments"""
        if isinstance(index.model(), QFileSystemModel):
            item = index.model().filePath(index)

            if index.model().isDir(index):
                # Trouve le TreeView parent
                tree_view = self.main_window.findChild(QTreeView)
                if tree_view:
                    if tree_view.isExpanded(index):
                        tree_view.collapse(index)
                    else:
                        tree_view.expand(index)
            else:
                # Vérifie si le fichier est déjà ouvert dans un onglet
                for tab in self.main_window.primary_center.get_tabs_by_type(TabType.EDITOR):
                    if isinstance(tab, EditorTab) and tab.file_path == item:
                        self.main_window.primary_center.setCurrentWidget(tab)
                        return
                        
                # Si non ouvert, crée un nouvel onglet
                self.main_window.open_file_in_editor(item)
            
            self.objCliked.emit(item)

        elif isinstance(index.model(), QStandardItemModel):
            pass

        else:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Unsupported tree model type: {type(index.model())}")

    def setup_drag_drop(self):
        """Configure les paramètres de drag & drop"""
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Gère l'entrée d'un drag"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
            
    def dragMoveEvent(self, event: QDragMoveEvent):
        """Gère le mouvement pendant un drag"""
        if event.mimeData().hasUrls():
            drop_index = self.indexAt(event.pos())
            if drop_index.isValid():
                if self.model.isDir(drop_index):
                    event.acceptProposedAction()
                    return
            event.ignore()
        else:
            event.ignore()
            
    def dropEvent(self, event: QDropEvent):
        """Gère le drop des fichiers"""
        if event.mimeData().hasUrls():
            drop_index = self.indexAt(event.pos())
            if not drop_index.isValid():
                return
                
            destination_path = self.model.filePath(drop_index)
            if not self.model.isDir(drop_index):
                destination_path = QFileInfo(destination_path).dir().absolutePath()
                
            for url in event.mimeData().urls():
                source_path = url.toLocalFile()
                if not source_path:
                    continue
                    
                try:
                    source_file = QFile(source_path)
                    file_name = QFileInfo(source_path).fileName()
                    destination_file = QDir(destination_path).filePath(file_name)
                    
                    if QFile.exists(destination_file):
                        # Gestion des doublons
                        base_name = QFileInfo(file_name).baseName()
                        extension = QFileInfo(file_name).completeSuffix()
                        counter = 1
                        while QFile.exists(destination_file):
                            new_name = f"{base_name}_{counter}.{extension}"
                            destination_file = QDir(destination_path).filePath(new_name)
                            counter += 1
                    
                    if source_file.rename(destination_file):
                        self.fileDropped.emit(source_path, destination_file)
                    else:
                        logging.error(f"Erreur lors du déplacement: {source_path}")
                        
                except Exception as e:
                    logging.error(f"Erreur: {str(e)}")
                    
            event.acceptProposedAction()
        else:
            event.ignore()
