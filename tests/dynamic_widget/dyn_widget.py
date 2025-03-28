from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from typing import Dict, Any, Optional, List, Callable


class DynamicWidgetGenerator:
    """
    Classe qui génère des widgets PyQt6 dynamiquement à partir d'un dictionnaire de configuration.
    """
    
    def __init__(self):
        # Dictionnaire des fonctions de création de widgets par type
        self._widget_creators = {
            'spacer': self._create_spacer,
            'label': self._create_label,
            'lineEdit': self._create_line_edit,
            'textEdit': self._create_text_edit,
            'button': self._create_button,
            'checkBox': self._create_checkbox,
            'comboBox': self._create_combobox,
            'slider': self._create_slider,
            'spinBox': self._create_spinbox,
            'radioButton': self._create_radio_button,
            'groupBox': self._create_group_box,
            'frame': self._create_frame,
            'container': self._create_container,
        }
        
        # Dictionnaire des fonctions de création de layouts
        self._layout_creators = {
            'vertical': QVBoxLayout,
            'horizontal': QHBoxLayout,
            'grid': QGridLayout,
            'form': QFormLayout
        }
        
        # Registre pour stocker les widgets générés
        self._widget_registry = {}
    
    def create_widget(self, config: Dict[str, Any]) -> QWidget:
        """
        Crée un widget à partir d'un dictionnaire de configuration.
        
        Args:
            config: Dictionnaire contenant la configuration du widget
            
        Returns:
            QWidget: Le widget généré
        """
        if not isinstance(config, dict) or 'type' not in config:
            raise ValueError("La configuration doit être un dictionnaire contenant au moins un type")
        
        widget_type = config['type']
        
        if widget_type not in self._widget_creators:
            raise ValueError(f"Type de widget non supporté: {widget_type}")
        
        # Création du widget
        widget = self._widget_creators[widget_type](config)
        
        # Enregistrer le widget si un id est spécifié
        if 'id' in config:
            self._widget_registry[config['id']] = widget
        
        # Configuration du layout si spécifié
        if 'layout' in config and isinstance(config['layout'], dict):
            layout_config = config['layout']
            layout_type = layout_config.get('type', 'vertical')
            
            if layout_type not in self._layout_creators:
                raise ValueError(f"Type de layout non supporté: {layout_type}")
            
            layout = self._layout_creators[layout_type]()
            self._configure_layout(layout, layout_config)
            
            # Ajouter les widgets enfants
            if 'children' in layout_config and isinstance(layout_config['children'], list):
                for child_config in layout_config['children']:
                    # Traitement spécial pour les spacers
                    if isinstance(child_config, dict) and child_config.get('type') == 'spacer':
                        self._add_spacer_to_layout(layout, layout_type, child_config)
                        continue
                    
                    child_widget = self.create_widget(child_config)
                    
                    if layout_type == 'grid' and 'position' in child_config:
                        pos = child_config['position']
                        layout.addWidget(child_widget, pos.get('row', 0), pos.get('column', 0), 
                                         pos.get('rowSpan', 1), pos.get('columnSpan', 1))
                    elif layout_type == 'form' and 'label' in child_config:
                        layout.addRow(child_config['label'], child_widget)
                    else:
                        layout.addWidget(child_widget)
            
            widget.setLayout(layout)
        
        # Appliquer les styles si spécifiés
        if 'style' in config and isinstance(config['style'], dict):
            self._apply_styles(widget, config['style'])
        
        # Connecter les signaux si spécifiés
        if 'signals' in config and isinstance(config['signals'], list):
            self._connect_signals(widget, config['signals'])
        
        return widget
    
    def get_widget_by_id(self, widget_id: str) -> Optional[QWidget]:
        """
        Récupère un widget par son identifiant.
        
        Args:
            widget_id: L'identifiant du widget
            
        Returns:
            QWidget: Le widget correspondant ou None s'il n'existe pas
        """
        return self._widget_registry.get(widget_id)
    
    def register_custom_widget_creator(self, widget_type: str, creator_func: Callable):
        """
        Enregistre une fonction personnalisée pour créer un type de widget spécifique.
        
        Args:
            widget_type: Le type de widget
            creator_func: La fonction qui crée le widget
        """
        self._widget_creators[widget_type] = creator_func
    
    # Fonctions privées pour créer différents types de widgets
    
    def _create_label(self, config: Dict[str, Any]) -> QLabel:
        label = QLabel(config.get('text', ''))
        if 'alignment' in config:
            alignment = self._parse_alignment(config['alignment'])
            label.setAlignment(alignment)
        if 'pixmap' in config:
            pixmap = QPixmap(config['pixmap'])
            if 'pixmapSize' in config:
                size = config['pixmapSize']
                pixmap = pixmap.scaled(size.get('width', 16), size.get('height', 16))
            label.setPixmap(pixmap)
        return label
    
    def _create_line_edit(self, config: Dict[str, Any]) -> QLineEdit:
        line_edit = QLineEdit(config.get('text', ''))
        if 'placeholder' in config:
            line_edit.setPlaceholderText(config['placeholder'])
        if 'readOnly' in config:
            line_edit.setReadOnly(config['readOnly'])
        if 'maxLength' in config:
            line_edit.setMaxLength(config['maxLength'])
        return line_edit
    
    def _create_text_edit(self, config: Dict[str, Any]) -> QTextEdit:
        text_edit = QTextEdit()
        if 'text' in config:
            text_edit.setText(config['text'])
        if 'html' in config:
            text_edit.setHtml(config['html'])
        if 'readOnly' in config:
            text_edit.setReadOnly(config['readOnly'])
        return text_edit
    
    def _create_button(self, config: Dict[str, Any]) -> QPushButton:
        button = QPushButton(config.get('text', ''))
        if 'icon' in config:
            icon = QIcon(config['icon'])
            button.setIcon(icon)
        if 'iconSize' in config:
            size = config['iconSize']
            button.setIconSize(QSize(size.get('width', 16), size.get('height', 16)))
        if 'checkable' in config:
            button.setCheckable(config['checkable'])
        return button
    
    def _create_checkbox(self, config: Dict[str, Any]) -> QCheckBox:
        checkbox = QCheckBox(config.get('text', ''))
        if 'checked' in config:
            checkbox.setChecked(config['checked'])
        return checkbox
    
    def _create_combobox(self, config: Dict[str, Any]) -> QComboBox:
        combo = QComboBox()
        if 'items' in config and isinstance(config['items'], list):
            for item in config['items']:
                if isinstance(item, dict):
                    text = item.get('text', '')
                    data = item.get('data')
                    icon = item.get('icon')
                    
                    if icon:
                        combo.addItem(QIcon(icon), text, data)
                    else:
                        combo.addItem(text, data)
                else:
                    combo.addItem(str(item))
        if 'currentIndex' in config:
            combo.setCurrentIndex(config['currentIndex'])
        if 'editable' in config:
            combo.setEditable(config['editable'])
        return combo
    
    def _create_slider(self, config: Dict[str, Any]) -> QSlider:
        orientation = Qt.Orientation.Horizontal
        if 'orientation' in config:
            if config['orientation'].lower() == 'vertical':
                orientation = Qt.Orientation.Vertical
        
        slider = QSlider(orientation)
        if 'minimum' in config:
            slider.setMinimum(config['minimum'])
        if 'maximum' in config:
            slider.setMaximum(config['maximum'])
        if 'value' in config:
            slider.setValue(config['value'])
        if 'singleStep' in config:
            slider.setSingleStep(config['singleStep'])
        if 'pageStep' in config:
            slider.setPageStep(config['pageStep'])
        if 'tickPosition' in config:
            positions = {
                'none': QSlider.TickPosition.NoTicks,
                'both': QSlider.TickPosition.TicksBothSides,
                'above': QSlider.TickPosition.TicksAbove,
                'below': QSlider.TickPosition.TicksBelow,
                'left': QSlider.TickPosition.TicksLeft,
                'right': QSlider.TickPosition.TicksRight
            }
            slider.setTickPosition(positions.get(config['tickPosition'].lower(), QSlider.TickPosition.NoTicks))
        return slider
    
    def _create_spinbox(self, config: Dict[str, Any]) -> QSpinBox:
        spinbox = QSpinBox()
        if 'minimum' in config:
            spinbox.setMinimum(config['minimum'])
        if 'maximum' in config:
            spinbox.setMaximum(config['maximum'])
        if 'value' in config:
            spinbox.setValue(config['value'])
        if 'prefix' in config:
            spinbox.setPrefix(config['prefix'])
        if 'suffix' in config:
            spinbox.setSuffix(config['suffix'])
        if 'singleStep' in config:
            spinbox.setSingleStep(config['singleStep'])
        return spinbox
    
    def _create_radio_button(self, config: Dict[str, Any]) -> QRadioButton:
        radio = QRadioButton(config.get('text', ''))
        if 'checked' in config:
            radio.setChecked(config['checked'])
        return radio
    
    def _create_group_box(self, config: Dict[str, Any]) -> QGroupBox:
        group_box = QGroupBox(config.get('title', ''))
        if 'checkable' in config:
            group_box.setCheckable(config['checkable'])
        if 'checked' in config and group_box.isCheckable():
            group_box.setChecked(config['checked'])
        return group_box
    
    def _create_frame(self, config: Dict[str, Any]) -> QFrame:
        frame = QFrame()
        
        # Configurer la forme de la frame
        if 'frameShape' in config:
            shapes = {
                'noFrame': QFrame.Shape.NoFrame,
                'box': QFrame.Shape.Box,
                'panel': QFrame.Shape.Panel,
                'winPanel': QFrame.Shape.WinPanel,
                'hLine': QFrame.Shape.HLine,
                'vLine': QFrame.Shape.VLine,
                'stylePanel': QFrame.Shape.StyledPanel
            }
            frame.setFrameShape(shapes.get(config['frameShape'], QFrame.Shape.NoFrame))
        
        # Configurer l'ombre de la frame
        if 'frameShadow' in config:
            shadows = {
                'plain': QFrame.Shadow.Plain,
                'raised': QFrame.Shadow.Raised,
                'sunken': QFrame.Shadow.Sunken
            }
            frame.setFrameShadow(shadows.get(config['frameShadow'], QFrame.Shadow.Plain))
        
        if 'lineWidth' in config:
            frame.setLineWidth(config['lineWidth'])
        
        return frame
    
    def _create_container(self, config: Dict[str, Any]) -> QWidget:
        container = QWidget()
        return container
    
    # Fonctions utilitaires
    def _configure_layout(self, layout: QLayout, config: Dict[str, Any]):
        """Configure un layout avec les propriétés spécifiées dans config"""
        if 'spacing' in config:
            layout.setSpacing(config['spacing'])
        
        if 'margins' in config:
            margins = config['margins']
            if isinstance(margins, int):
                layout.setContentsMargins(margins, margins, margins, margins)
            elif isinstance(margins, dict):
                layout.setContentsMargins(
                    margins.get('left', 0), 
                    margins.get('top', 0), 
                    margins.get('right', 0), 
                    margins.get('bottom', 0)
                )

    def _apply_styles(self, widget: QWidget, style_config: Dict[str, Any]):
        """Applique des styles à un widget"""
        # Appliquer le styleSheet
        if 'styleSheet' in style_config:
            widget.setStyleSheet(style_config['styleSheet'])
        
        # Fixer la taille
        if 'fixedSize' in style_config:
            size = style_config['fixedSize']
            widget.setFixedSize(size.get('width', 0), size.get('height', 0))
        
        # Fixer la largeur
        if 'fixedWidth' in style_config:
            widget.setFixedWidth(style_config['fixedWidth'])
        
        # Fixer la hauteur
        if 'fixedHeight' in style_config:
            widget.setFixedHeight(style_config['fixedHeight'])
        
        # Définir la taille minimale
        if 'minimumSize' in style_config:
            size = style_config['minimumSize']
            widget.setMinimumSize(size.get('width', 0), size.get('height', 0))
        
        # Définir la taille maximale
        if 'maximumSize' in style_config:
            size = style_config['maximumSize']
            widget.setMaximumSize(size.get('width', 0), size.get('height', 0))
        
        # Définir la police
        if 'font' in style_config:
            font = widget.font()
            font_config = style_config['font']
            
            if 'family' in font_config:
                font.setFamily(font_config['family'])
            if 'size' in font_config:
                font.setPointSize(font_config['size'])
            if 'bold' in font_config:
                font.setBold(font_config['bold'])
            if 'italic' in font_config:
                font.setItalic(font_config['italic'])
            
            widget.setFont(font)
        
        # Définir la visibilité
        if 'visible' in style_config:
            widget.setVisible(style_config['visible'])
        
        # Définir l'activation
        if 'enabled' in style_config:
            widget.setEnabled(style_config['enabled'])
    
    def _connect_signals(self, widget: QWidget, signals_config: List[Dict[str, Any]]):
        """Connecte les signaux d'un widget"""
        for signal_config in signals_config:
            if 'signal' not in signal_config or 'slot' not in signal_config:
                continue
            
            signal_name = signal_config['signal']
            slot_id = signal_config['slot']
            
            # Vérifier si le slot est une fonction existante
            if callable(slot_id):
                slot = slot_id
            elif isinstance(slot_id, str) and hasattr(self, slot_id):
                slot = getattr(self, slot_id)
            else:
                continue
            
            # Obtenir l'attribut du signal
            if hasattr(widget, signal_name):
                signal = getattr(widget, signal_name)
                if callable(signal):
                    signal.connect(slot)
    
    def _parse_alignment(self, alignment_str: str) -> Qt.AlignmentFlag:
        """Convertit une chaîne d'alignement en valeur Qt.AlignmentFlag"""
        alignment_map = {
            'left': Qt.AlignmentFlag.AlignLeft,
            'right': Qt.AlignmentFlag.AlignRight,
            'center': Qt.AlignmentFlag.AlignCenter,
            'justify': Qt.AlignmentFlag.AlignJustify,
            'top': Qt.AlignmentFlag.AlignTop,
            'bottom': Qt.AlignmentFlag.AlignBottom,
            'vcenter': Qt.AlignmentFlag.AlignVCenter,
            'hcenter': Qt.AlignmentFlag.AlignHCenter,
        }
        
        if alignment_str in alignment_map:
            return alignment_map[alignment_str]
        
        # Gestion des alignements combinés (par exemple "top left")
        alignment = Qt.AlignmentFlag.AlignLeft  # valeur par défaut
        parts = alignment_str.split()
        
        for part in parts:
            if part in alignment_map:
                alignment |= alignment_map[part]
        
        return alignment

    def _create_spacer(self, config: Dict[str, Any]) -> QWidget:
        """
        Crée un widget vide pour représenter un spacer.
        Note: Les spacers sont gérés différemment car ils sont ajoutés directement au layout
        """
        return QWidget()

    def _add_spacer_to_layout(self, layout, layout_type: str, config: Dict[str, Any]):
        """Ajoute un spacer à un layout"""
        if layout_type in ('vertical', 'horizontal'):
            # Pour les layouts verticaux et horizontaux
            size = config.get('size', 0)
            stretch = config.get('stretch', 1)
        
            if size > 0:
                layout.addSpacing(size)
            else:
                layout.addStretch(stretch)
    
        elif layout_type == 'grid':            
            # Paramètres pour le spacer de grille
            width = config.get('width', 0)
            height = config.get('height', 0)
            h_policy = config.get('horizontalPolicy', 'expanding')
            v_policy = config.get('verticalPolicy', 'expanding')
            
            # Convertir les politiques en valeurs QSizePolicy
            h_policies = {
                'fixed': QSizePolicy.Policy.Fixed,
                'minimum': QSizePolicy.Policy.Minimum,
                'maximum': QSizePolicy.Policy.Maximum,
                'preferred': QSizePolicy.Policy.Preferred,
                'expanding': QSizePolicy.Policy.Expanding,
                'minimumExpanding': QSizePolicy.Policy.MinimumExpanding,
                'ignored': QSizePolicy.Policy.Ignored
            }
            
            h_policy_value = h_policies.get(h_policy, QSizePolicy.Policy.Expanding)
            v_policy_value = h_policies.get(v_policy, QSizePolicy.Policy.Expanding)
            
            # Créer le spacer item
            spacer_item = QSpacerItem(width, height, h_policy_value, v_policy_value)
            
            # Ajouter à la grille à la position spécifiée
            if 'position' in config:
                pos = config['position']
                layout.addItem(
                    spacer_item, 
                    pos.get('row', 0), 
                    pos.get('column', 0), 
                    pos.get('rowSpan', 1), 
                    pos.get('columnSpan', 1)
                )
            else:
                # Par défaut, ajouter à la fin
                row_count = layout.rowCount()
                layout.addItem(spacer_item, row_count, 0)
        
        elif layout_type == 'form':
            # Les spacers dans les form layouts sont plus limités
            # On peut ajouter un spacer entre les lignes
            if 'size' in config:
                layout.addItem(layout.spacing())
