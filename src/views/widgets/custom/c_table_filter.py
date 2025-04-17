from typing import *
import logging
import inspect
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *


class CustomTableFilter(QWidget):
    """
    Widget de filtrage pour un QTableWidget.
    Fournit des fonctionnalités de recherche, tri, visibilité des colonnes et filtrage par mots-clés.
    """
    filterChanged: ClassVar[Signal] = Signal()

    def __init__(self, table_widget: QTableWidget, debug: Optional[bool] = False, parent=None) -> None:
        """
        Initialise le widget de filtrage.
        
        Args:
            table_widget: QTableWidget à filtrer
            debug: Active le mode debug
            parent: Widget parent
        """
        super(CustomTableFilter, self).__init__(parent)
        
        self.debug = debug
        self.table = table_widget
        
        # Initialiser l'interface utilisateur
        self.initUI()
        
        # Mettre à jour les widgets avec les colonnes actuelles
        self.updateFilterWidgets()
    
    def initUI(self) -> None:
        """Initialise l'interface utilisateur du filtre."""
        # Main layout
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.headerArea = QLabel("Filtres de tableau")
        self.headerArea.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.mainLayout.addWidget(self.headerArea)

        # Add Scroll Area
        self._loadScrollArea()

        # Section de recherche
        search_group = QGroupBox("Recherche")
        search_layout = QVBoxLayout()
        search_group.setLayout(search_layout)
        
        # Widget de recherche par colonne
        search_layout_col = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher...")
        self.search_input.textChanged.connect(self.applyFilters)
        
        self.column_combo = QComboBox()
        self.column_combo.addItem("Toutes les colonnes")
        # Les colonnes spécifiques seront ajoutées dynamiquement

        search_layout_col.addWidget(self.search_input)
        search_layout_col.addWidget(self.column_combo)
        search_layout.addLayout(search_layout_col)
        
        # Bouton de réinitialisation de la recherche
        self.reset_search_btn = QPushButton("Réinitialiser la recherche")
        self.reset_search_btn.clicked.connect(self.resetSearch)
        search_layout.addWidget(self.reset_search_btn)

        self.scrollLayout.addWidget(search_group)
        
        # Section de tri
        sort_group = QGroupBox("Tri")
        sort_layout = QVBoxLayout()
        sort_group.setLayout(sort_layout)
        
        # Widget de sélection de colonne pour le tri
        sort_layout_col = QHBoxLayout()
        sort_col_label = QLabel("Colonne:")
        self.sort_column_combo = QComboBox()
        # Les colonnes seront ajoutées dynamiquement
        
        sort_layout_col.addWidget(sort_col_label)
        sort_layout_col.addWidget(self.sort_column_combo)
        sort_layout.addLayout(sort_layout_col)
        
        # Boutons radio pour l'ordre de tri
        sort_order_layout = QHBoxLayout()
        self.sort_asc_radio = QRadioButton("Croissant")
        self.sort_desc_radio = QRadioButton("Décroissant")
        self.sort_asc_radio.setChecked(True)
        
        sort_order_layout.addWidget(self.sort_asc_radio)
        sort_order_layout.addWidget(self.sort_desc_radio)
        sort_layout.addLayout(sort_order_layout)
        
        # Bouton d'application du tri
        self.apply_sort_btn = QPushButton("Appliquer le tri")
        self.apply_sort_btn.clicked.connect(self.applySorting)
        sort_layout.addWidget(self.apply_sort_btn)
        
        self.scrollLayout.addWidget(sort_group)
        
        # Section de visibilité des colonnes
        columns_group = QGroupBox("Visibilité des colonnes")
        columns_layout = QVBoxLayout()
        columns_group.setLayout(columns_layout)
        
        # Liste des colonnes avec cases à cocher
        self.column_list_widget = QListWidget()
        self.column_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        # Les colonnes seront ajoutées dynamiquement
        
        columns_layout.addWidget(self.column_list_widget)
        
        # Boutons pour afficher/masquer toutes les colonnes
        col_buttons_layout = QHBoxLayout()
        self.show_all_cols_btn = QPushButton("Afficher tout")
        self.show_all_cols_btn.clicked.connect(self.showAllColumns)
        self.hide_all_cols_btn = QPushButton("Masquer tout")
        self.hide_all_cols_btn.clicked.connect(self.hideAllColumns)
        
        col_buttons_layout.addWidget(self.show_all_cols_btn)
        col_buttons_layout.addWidget(self.hide_all_cols_btn)
        columns_layout.addLayout(col_buttons_layout)
        
        self.scrollLayout.addWidget(columns_group)
        
        # Section pour les filtres par mots-clés
        keyword_group = QGroupBox("Filtres par mots-clés")
        keyword_layout = QVBoxLayout()
        keyword_group.setLayout(keyword_layout)
        
        # Liste des filtres actifs
        self.keyword_list = QListWidget()
        keyword_layout.addWidget(self.keyword_list)
        
        # Ajout d'un nouveau filtre
        keyword_add_layout = QHBoxLayout()
        self.keyword_col_combo = QComboBox()
        self.keyword_col_combo.addItem("Toutes les colonnes")
        # Les colonnes spécifiques seront ajoutées dynamiquement
        
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Mot-clé...")
        
        self.add_keyword_btn = QPushButton("+")
        self.add_keyword_btn.clicked.connect(self.addKeywordFilter)
        
        keyword_add_layout.addWidget(self.keyword_col_combo)
        keyword_add_layout.addWidget(self.keyword_input)
        keyword_add_layout.addWidget(self.add_keyword_btn)
        keyword_layout.addLayout(keyword_add_layout)
        
        self.scrollLayout.addWidget(keyword_group)
        
        # Ajouter un espace extensible en bas
        self.scrollLayout.addStretch()
        
        # Définir la taille initiale
        self.setMinimumWidth(250)
        self.scrollContainer.updateGeometry()
        self.scrollArea.updateGeometry()
        self.updateGeometry()
    
    def updateFilterWidgets(self) -> None:
        """Met à jour les widgets de filtrage avec les colonnes actuelles du tableau."""
        if self.debug:
            logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Updating filter widgets")
        
        # Vider les combobox existants
        self.column_combo.clear()
        self.sort_column_combo.clear()
        self.keyword_col_combo.clear()
        
        # Ajouter l'option "Toutes les colonnes"
        self.column_combo.addItem("Toutes les colonnes")
        self.keyword_col_combo.addItem("Toutes les colonnes")
        
        # Effacer la liste des colonnes
        self.column_list_widget.clear()
        
        # Récupérer les en-têtes de colonnes du tableau
        column_count = self.table.columnCount()
        column_headers = []
        
        for col in range(column_count):
            header_item = self.table.horizontalHeaderItem(col)
            if header_item:
                header = header_item.text()
                column_headers.append(header)
                
                # Ajouter aux combos
                self.column_combo.addItem(header)
                self.sort_column_combo.addItem(header)
                self.keyword_col_combo.addItem(header)
                
                # Ajouter à la liste des colonnes avec checkbox
                item = QListWidgetItem(header)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Checked if not self.table.isColumnHidden(col) else Qt.CheckState.Unchecked)
                self.column_list_widget.addItem(item)
            
        # Connecter le changement des checkboxes
        try:
            self.column_list_widget.itemChanged.disconnect()
        except:
            pass
        self.column_list_widget.itemChanged.connect(self.toggleColumnVisibility)
    
    def resetSearch(self) -> None:
        """Réinitialise la recherche."""
        if self.debug:
            logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Resetting search")
        
        self.search_input.clear()
        self.column_combo.setCurrentIndex(0)
        self.applyFilters()
    
    def applySorting(self) -> None:
        """Applique le tri sélectionné."""
        if self.debug:
            logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Applying sorting")
        
        if self.sort_column_combo.count() == 0:
            return
            
        column_index = self.sort_column_combo.currentIndex()
        
        # Définir l'ordre de tri
        if self.sort_asc_radio.isChecked():
            order = Qt.SortOrder.AscendingOrder
        else:
            order = Qt.SortOrder.DescendingOrder
        
        # Appliquer le tri
        self.table.sortByColumn(column_index, order)
    
    def toggleColumnVisibility(self, item) -> None:
        """Affiche ou masque une colonne en fonction de l'état de la case à cocher."""
        if self.debug:
            logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Toggling column visibility for {item.text()}")
        
        for col in range(self.table.columnCount()):
            header_item = self.table.horizontalHeaderItem(col)
            if header_item and header_item.text() == item.text():
                self.table.setColumnHidden(col, item.checkState() != Qt.CheckState.Checked)
                # Émettre le signal de changement
                self.filterChanged.emit()
                break
    
    def showAllColumns(self) -> None:
        """Affiche toutes les colonnes."""
        if self.debug:
            logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Showing all columns")
        
        for col in range(self.table.columnCount()):
            self.table.setColumnHidden(col, False)
            
        # Met à jour les cases à cocher
        try:
            self.column_list_widget.itemChanged.disconnect()
        except:
            pass
            
        for i in range(self.column_list_widget.count()):
            item = self.column_list_widget.item(i)
            item.setCheckState(Qt.CheckState.Checked)
            
        self.column_list_widget.itemChanged.connect(self.toggleColumnVisibility)
        
        # Émettre le signal de changement
        self.filterChanged.emit()
    
    def hideAllColumns(self) -> None:
        """Masque toutes les colonnes."""
        if self.debug:
            logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Hiding all columns")
        
        for col in range(self.table.columnCount()):
            self.table.setColumnHidden(col, True)
            
        # Met à jour les cases à cocher
        try:
            self.column_list_widget.itemChanged.disconnect()
        except:
            pass
            
        for i in range(self.column_list_widget.count()):
            item = self.column_list_widget.item(i)
            item.setCheckState(Qt.CheckState.Unchecked)
            
        self.column_list_widget.itemChanged.connect(self.toggleColumnVisibility)
        
        # Émettre le signal de changement
        self.filterChanged.emit()
    
    def addKeywordFilter(self) -> None:
        """Ajoute un nouveau filtre par mot-clé."""
        keyword = self.keyword_input.text().strip()
        if not keyword:
            return
            
        column = self.keyword_col_combo.currentText()
        filter_text = f"{column}: {keyword}"
        
        if self.debug:
            logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Adding keyword filter: {filter_text}")
        
        # Créer un widget pour l'élément de la liste
        list_item_widget = QWidget()
        item_layout = QHBoxLayout(list_item_widget)
        item_layout.setContentsMargins(2, 2, 2, 2)
        
        # Label pour le texte du filtre
        filter_label = QLabel(filter_text)
        filter_label.setStyleSheet("padding-left: 5px;")
        
        # Bouton de suppression
        delete_btn = QPushButton("X")
        delete_btn.setMaximumWidth(30)
        delete_btn.setStyleSheet("padding: 2px;")
        
        item_layout.addWidget(filter_label, 1)
        item_layout.addWidget(delete_btn, 0)
        
        # Ajouter à la liste
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, filter_text)  # Stocker le texte du filtre
        self.keyword_list.addItem(item)
        self.keyword_list.setItemWidget(item, list_item_widget)
        
        # Connecter le bouton de suppression
        delete_btn.clicked.connect(lambda: self.removeKeywordFilter(item))
        
        # Effacer le champ d'entrée
        self.keyword_input.clear()
        
        # Appliquer le filtre
        self.applyFilters()
    
    def removeKeywordFilter(self, item) -> None:
        """Supprime un filtre par mot-clé."""
        if self.debug:
            filter_text = item.data(Qt.ItemDataRole.UserRole)
            logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Removing keyword filter: {filter_text}")
        
        row = self.keyword_list.row(item)
        self.keyword_list.takeItem(row)
        self.applyFilters()
    
    def getKeywordFilters(self) -> List[Tuple[str, str]]:
        """Récupère la liste des filtres par mots-clés actifs."""
        filters = []
        for i in range(self.keyword_list.count()):
            item = self.keyword_list.item(i)
            filter_text = item.data(Qt.ItemDataRole.UserRole)
            
            # Extraire la colonne et le mot-clé
            parts = filter_text.split(": ", 1)
            if len(parts) == 2:
                col, keyword = parts
                filters.append((col, keyword.lower()))
        
        return filters
    
    def applyFilters(self) -> None:
        """Applique tous les filtres actifs au tableau."""
        if self.debug:
            logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Applying filters")
        
        search_text = self.search_input.text().lower()
        search_column = self.column_combo.currentText()
        
        # Collecter les filtres par mots-clés
        keyword_filters = self.getKeywordFilters()
        
        # Appliquer les filtres à chaque ligne
        for row in range(self.table.rowCount()):
            show_row = True
            
            # Vérifier le filtre de recherche
            if search_text:
                row_matches_search = False
                
                # Rechercher dans la colonne spécifiée ou dans toutes les colonnes
                if search_column == "Toutes les colonnes":
                    # Rechercher dans toutes les colonnes
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        if item and search_text in item.text().lower():
                            row_matches_search = True
                            break
                else:
                    # Rechercher dans la colonne spécifiée
                    for col in range(self.table.columnCount()):
                        header_item = self.table.horizontalHeaderItem(col)
                        if header_item and header_item.text() == search_column:
                            item = self.table.item(row, col)
                            if item and search_text in item.text().lower():
                                row_matches_search = True
                            break
                
                if not row_matches_search:
                    show_row = False
            
            # Vérifier les filtres par mots-clés
            if show_row and keyword_filters:
                for col_name, keyword in keyword_filters:
                    if col_name == "Toutes les colonnes":
                        # Rechercher dans toutes les colonnes
                        matches_keyword = False
                        for col in range(self.table.columnCount()):
                            item = self.table.item(row, col)
                            if item and keyword in item.text().lower():
                                matches_keyword = True
                                break
                        
                        if not matches_keyword:
                            show_row = False
                            break
                    else:
                        # Rechercher dans la colonne spécifiée
                        matches_keyword = False
                        for col in range(self.table.columnCount()):
                            header_item = self.table.horizontalHeaderItem(col)
                            if header_item and header_item.text() == col_name:
                                item = self.table.item(row, col)
                                if item and keyword in item.text().lower():
                                    matches_keyword = True
                                break
                        
                        if not matches_keyword:
                            show_row = False
                            break
            
            # Appliquer la visibilité de la ligne
            self.table.setRowHidden(row, not show_row)
        
        # Émettre le signal de changement
        self.filterChanged.emit()

    def _loadScrollArea(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mainLayout.addWidget(self.scrollArea, 1)

        # Create container widget for scroll area
        self.scrollContainer = QWidget()
        self.scrollArea.setWidget(self.scrollContainer)
        self.scrollLayout = QVBoxLayout(self.scrollContainer)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setSpacing(3)
        

