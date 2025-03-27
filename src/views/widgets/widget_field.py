from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from typing import *
import enum
import logging
import inspect

from .card import Card


class WidgetField(QWidget):
    class GridForm(enum.Enum):
        GList = 1      # une colonne, 1 ligne
        CMosaics = 2   # Vue par colonnes
        RMosaics = 3   # Vue par lignes

    def __init__(self, debug: bool = False, parent=None):
        super(WidgetField, self).__init__(parent)

        self._debug = debug
        self._gridObjects: List[QWidget] = []
        self._gridForm: WidgetField.GridForm = WidgetField.GridForm.CMosaics
        self._grid_number: int = 3  # Par défaut : 3 colonnes ou 3 lignes
        self.items: dict = {}

        self.initUI()
    
    def setHeaderArea(self, widget: QWidget) -> None:
        # Supprimer l'ancien widget du layout s'il existe
        if hasattr(self, 'headerArea') and self.headerArea is not None:
            self.mainLayout.removeWidget(self.headerArea)
            self.headerArea.setParent(None)
    
        # Assigner et ajouter le nouveau widget
        self.headerArea = widget
        if widget is not None:
            # Insérer le widget en première position (index 0)
            self.mainLayout.insertWidget(0, widget)
    
        # Forcer une mise à jour visuelle
        self.mainLayout.update()

    def initUI(self):
        self.setAcceptDrops(True)
        # Main layout
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.headerArea = QWidget()
        self.mainLayout.addWidget(self.headerArea)

        # Add Scroll Area
        self._loadScrollArea()
        
    def _loadScrollArea(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.mainLayout.addWidget(self.scrollArea)

        # Create container widget for scroll area
        self.scrollContainer = QWidget()
        self.scrollContainer.setAcceptDrops(True)
        self.scrollArea.setWidget(self.scrollContainer)
        self.scrollLayout = QGridLayout(self.scrollContainer)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        event.acceptProposedAction()
        
    def dropEvent(self, event: QDropEvent):
        pos = event.pos()
        widget = event.source()

        if widget and isinstance(widget, QWidget) and widget in self.items:
            # Trouver la position dans la grille la plus proche
            for lbl, (row, col) in self.items.items():
                cell_widget = self.scrollLayout.itemAtPosition(row, col).widget()
                if cell_widget == widget:  # Éviter de repositionner le même widget
                    continue

                rect = cell_widget.geometry()
                if rect.contains(pos):
                    # Récupérer le rowSpan et columnSpan des deux widgets
                    old_row, old_col = self.items[widget]
                
                    # Récupérer les informations de disposition pour les deux widgets
                    widget_index = self.scrollLayout.indexOf(widget)
                    target_index = self.scrollLayout.indexOf(cell_widget)

                    # Utiliser getItemPosition qui retourne (row, column, rowSpan, columnSpan)
                    _, _, widget_row_span, widget_col_span = self.scrollLayout.getItemPosition(widget_index)
                    _, _, target_row_span, target_col_span = self.scrollLayout.getItemPosition(target_index)
                
                    # Supprimer les widgets actuels de la grille pour éviter les conflits
                    self.scrollLayout.removeWidget(widget)
                    self.scrollLayout.removeWidget(cell_widget)
                
                    # Ajouter les widgets aux nouvelles positions avec leurs spans respectifs
                    self.scrollLayout.addWidget(widget, row, col, target_row_span, target_col_span)
                    self.scrollLayout.addWidget(cell_widget, old_row, old_col, widget_row_span, widget_col_span)

                    # Mettre à jour le dictionnaire des positions
                    self.items[widget] = (row, col)
                    self.items[cell_widget] = (old_row, old_col)
                    break

        event.acceptProposedAction()
    
    def setGridForm(self, form: 'WidgetField.GridForm', grid_number: int = 1):
        """
        Définit la forme de la grille et le nombre de colonnes/lignes.
        
        Args:
            form: Type de grille (GList, CMosaics, RMosaics)
            grid_number: Nombre de colonnes ou de lignes selon le mode
        """
        self._gridForm = form
        if form == self.GridForm.GList:
            self._grid_number = 1  # Pour GList, toujours 1
        else:
            self._grid_number = max(1, grid_number)  # Au moins 1

    def isColumnMode(self) -> bool:
        return self._gridForm in {self.GridForm.GList, self.GridForm.CMosaics}
    
    def isRowMode(self) -> bool:
        return self._gridForm == self.GridForm.RMosaics
    
    def checkLayoutMode(self) -> str:
        if self.isColumnMode():
            return "column"
        
        if self.isRowMode():
            return "row"
    
    def refreshGrid(self):
        """
        Réorganise tous les widgets dans la grille selon la forme actuelle.
        À appeler après un changement de GridForm ou de grid_number.
        """
        if not self.items:
            return  # Rien à faire si la grille est vide
        
        # Sauvegarder l'état actuel
        widgets_info = []
        for widget in self._gridObjects:
            item_index = self.scrollLayout.indexOf(widget)
            if item_index != -1:
                pos = self.scrollLayout.getItemPosition(item_index)
                if pos:
                    r, c, rs, cs = pos
                    widgets_info.append((widget, rs, cs))
        
        # Vider la grille
        for widget, _, _ in widgets_info:
            self.scrollLayout.removeWidget(widget)
        
        # Effacer le dictionnaire des positions
        self.items.clear()
        
        # Replacer les widgets
        for widget, rs, cs in widgets_info:
            next_pos = self.getNextFreePosition(rs, cs)
            self.scrollLayout.addWidget(
                widget, 
                next_pos["row"],
                next_pos["column"],
                next_pos["rowSpan"],
                next_pos["columnSpan"]
            )
            self.items[widget] = (next_pos["row"], next_pos["column"])

    def addCard(self, widget: Optional[QWidget] = None, positions: Optional[dict] = None) -> None:
        """
        Ajoute une carte à la grille à la prochaine position libre.
        
        Args:
            widget: Widget à ajouter (si None, une carte par défaut est créée)
            positions: Dictionnaire de positions (si None, utilise les valeurs par défaut)
        """
        if positions is None:
            tmp_dict: dict = {
                "layout": {
                    "row": 0,
                    "column": 0,
                    "rowSpan": 1,
                    "columnSpan": 1,
                    "alignment": Qt.AlignmentFlag.AlignCenter
                }
            }
        else:
            if self._debug:
                logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {positions}")

            tmp_dict = positions
            
        if widget is None:
            card = Card(debug=True)
        else:
            card = widget

        # Assurez-vous que les clés existent avant d'y accéder
        row_span = tmp_dict["layout"].get("rowSpan", 1)
        col_span = tmp_dict["layout"].get("columnSpan", 1)

        next_free_pos = self.getNextFreePosition(row_span, col_span)

        tmp_dict["layout"]["row"] = next_free_pos["row"]
        tmp_dict["layout"]["column"] = next_free_pos["column"]

        # Ajouter le widget à la liste des objets de la grille
        self._gridObjects.append(card)
        self.scrollLayout.addWidget(
            card,
            tmp_dict["layout"]["row"],
            tmp_dict["layout"]["column"],
            tmp_dict["layout"]["rowSpan"],
            tmp_dict["layout"]["columnSpan"],
            tmp_dict["layout"]["alignment"]
        )
        self.items[card] = (tmp_dict["layout"]["row"], tmp_dict["layout"]["column"])

    def getNextFreePosition(self, rowSpan: int = 1, columnSpan: int = 1) -> Dict[str, int]:
        """
        Détermine la prochaine position libre dans la grille pour une carte de taille spécifiée.
    
        Args:
            rowSpan: Nombre de lignes que la carte occupera
            columnSpan: Nombre de colonnes que la carte occupera
        
        Returns:
            Dict[str, int]: Dictionnaire contenant row, column, rowSpan, columnSpan
        """
        # Initialisation des valeurs par défaut
        max_row, max_col = 0, 0

        resultDict: dict = {
            "row": 0,
            "column": 0,
            "rowSpan": rowSpan,
            "columnSpan": columnSpan
        }

        if not self.items:
            return resultDict
        
        # Parcourir tous les widgets existants pour trouver les positions occupées
        occupied_cells = set()
        for widget, (row, col) in self.items.items():
            item_index = self.scrollLayout.indexOf(widget)
            if item_index != -1:  # Vérifier que le widget est bien dans la grille
                pos = self.scrollLayout.getItemPosition(item_index)
                if pos:
                    r, c, rs, cs = pos
                    # Ajouter toutes les cellules occupées par ce widget
                    for i in range(r, r + rs):
                        for j in range(c, c + cs):
                            occupied_cells.add((i, j))
                    # Mettre à jour les valeurs maximales
                    max_row = max(max_row, r + rs - 1)
                    max_col = max(max_col, c + cs - 1)
        
        # Stratégie de placement basée sur le mode de grille
        if self.isColumnMode():
            # En mode colonne, on remplit d'abord les colonnes
            max_columns = self._grid_number
        
            # Parcourir la grille pour trouver une position libre assez grande
            for row in range(max_row + 2):  # +2 pour vérifier au-delà de la dernière ligne
                for col in range(max_columns):
                    # Vérifier si l'espace est suffisant
                    can_place = True
                    # Vérifier que le placement ne dépasse pas la limite de colonnes
                    if col + columnSpan > max_columns:
                        can_place = False
                        continue
                    
                    for r in range(row, row + rowSpan):
                        for c in range(col, col + columnSpan):
                            if (r, c) in occupied_cells:
                                can_place = False
                                break
                        if not can_place:
                            break
                
                    if can_place:
                        resultDict["row"] = row
                        resultDict["column"] = col
                        return resultDict
            
            # Si pas de place trouvée, ajouter à la ligne suivante
            resultDict["row"] = max_row + 1
            resultDict["column"] = 0
            return resultDict

        elif self.isRowMode():
            # En mode ligne, on remplit d'abord les lignes
            max_rows = self._grid_number

            # Parcourir la grille pour trouver une position libre assez grande
            for col in range(max_col + 2):  # +2 pour vérifier au-delà de la dernière colonne
                for row in range(max_rows):
                    # Vérifier si l'espace est suffisant
                    can_place = True
                    # Vérifier que le placement ne dépasse pas la limite de lignes
                    if row + rowSpan > max_rows:
                        can_place = False
                        continue
                    
                    for r in range(row, row + rowSpan):
                        for c in range(col, col + columnSpan):
                            if (r, c) in occupied_cells:
                                can_place = False
                                break
                        if not can_place:
                            break
                
                    if can_place:
                        resultDict["row"] = row
                        resultDict["column"] = col
                        return resultDict
            
            # Si pas de place trouvée, ajouter à la colonne suivante
            resultDict["row"] = 0
            resultDict["column"] = max_col + 1
            return resultDict

        # Par défaut, simplement ajouter à la fin
        resultDict["row"] = max_row + 1
        resultDict["column"] = 0
        return resultDict
