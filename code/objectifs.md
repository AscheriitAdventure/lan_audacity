### Rapport du 18/11/2024
Pour les unités centrales je compte ajouter comme stack : Dashboard, System, Monitor (si c'est un outil de niveau 3 et moins et qui permet une intervention extérieure).

J'ajouterai différents stacks en fonction du type s'il délivre un service physique (imprimantes, scanner, voip).

Je prévois pour le journal que quand c'est un fichier il deviendra un lien ouvrable dans un nouvel onglet en lecture seule.

Je compte déplacer les informations actuelles de Dashboard dans un nouveau stack appelé « System » ou « About ».

Je compte après déplacement proposer dans Dashboard d'ajouter les cartes : [OK]
-	Choix de langues
-	Option de Mise à Jour
-	Un Objet qui affichera (si ce n'est pas un fichier) les dernières fonctionnalités ajoutées sinon un lien. 
-	

### Rapport du 19/11/2024

Ajouter une fonction pour éviter les doublons d'onglets.
Avec comme objectif de pouvoir accéder aux fichiers sources en cas d'erreur, je vais faire en sorte de pouvoir éditer les fichiers.

### Rapport du 20/11/2024
### Rapport du 21/11/2024

Recherche de solution pour pouvoir lire/editer un fichier texte.

## 22-11-2024
### MSG ChatGPT:
bon jarvis voici mon code:
```python
from qtpy.QtWidgets import * # PyQt6
from qtpy.QtGui import * # PyQt6
from qtpy.QtCore import * # PyQt6
import logging
import os
import sys
from typing import Optional

class CEVU1(QPlainTextEdit):
    def __init__(
            self, 
            locked: Optional[bool] = False,
            parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        # Font de la police, Taille de la police
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        # Tabulation
        self.setTabStopWidth(40)

        # Verrouillage
        self.setReadOnly(locked)
        logging.debug(f"CodeEditorView: locked={locked}")
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText(" " * 4)
        else:
            super().keyPressEvent(event)
    
    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor("#F5F5F5")
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)
```

L'objectif est d'ajouter et d'afficher le rang de chaque ligne du document ouvert.

### MSG ChatGPT:
bon jarvis, voici mon code:
```python
class MarginObjectTextEdit(QWidget):
    def __init__(
            self, 
            editor, # CodeEditorView
            parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.editor = editor
        self.labels: List[QLabel] = []  # Liste pour stocker les QLabel des numéros de ligne
    
    def updateLineNumbers(self):
        """Met à jour les numéros de ligne en fonction des blocs visibles."""
        # Effacer les anciens QLabel
        for label in self.labels:
            label.deleteLater()
        self.labels.clear()

        # Obtenir le premier bloc visible
        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        # Parcourir les blocs visibles
        while block.isValid() and top <= self.height():
            if block.isVisible() and bottom >= 0:
                # Créer un QLabel pour chaque numéro de ligne
                number = str(block_number + 1)
                label = QLabel(number, self)
                label.move(5, int(top))  # Positionner le QLabel à la bonne hauteur
                label.adjustSize()  # Ajuster la taille du QLabel au contenu
                label.setAlignment(Qt.AlignRight)  # Alignement à droite
                self.labels.append(label)

            # Passer au bloc suivant
            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1
    
    def paintEvent(self, event):
        """Dessiner le fond de la marge."""
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor("Gainsboro"))  # Couleur pour le fond
        self.updateLineNumbers()  # Met à jour les numéros de ligne

```

```python
class CEVU1(QPlainTextEdit):
    def __init__(
            self, 
            locked: Optional[bool] = False,
            parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        # Font de la police, Taille de la police
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        # Tabulation
        self.setTabStopWidth(40)

        # Verrouillage
        self.setReadOnly(locked)
        logging.debug(f"CodeEditorView: locked={locked}")

        # Vue de la marge à gauche
        self.marginArea = MOTE(editor=self, parent=self)
        self.setViewportMargins(40, 0, 0, 0)
        
        # Connecter les signaux nécessaires
        self.blockCountChanged.connect(self.marginArea.update())
        self.updateRequest.connect(self.marginArea.update())
        self.cursorPositionChanged.connect(self.update())
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText(" " * 4)
        else:
            super().keyPressEvent(event)
    
    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor("#F5F5F5")
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def resizeEvent(self, event):
        """Synchroniser la position et la taille du widget marge."""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.marginArea.setGeometry(QRect(cr.left(), cr.top(), 40, cr.height()))

```

voici le msg d'erreur:
```bash
Traceback (most recent call last):
  File "C:\Program Files\JetBrains\PyCharm Community Edition 2024.3\plugins\python-ce\helpers\pydev\pydevd.py", line 1570, in _exec
    pydev_imports.execfile(file, globals, locals)  # execute the script
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\JetBrains\PyCharm Community Edition 2024.3\plugins\python-ce\helpers\pydev\_pydev_imps\_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "C:\Users\g.tronche\Documents\GitHub\lan_audacity\code\src\components\codeEditor\codeEditor_test.py", line 14, in <module>
    editor = CodeEditor()
             ^^^^^^^^^^^^
  File "C:\Users\g.tronche\Documents\GitHub\lan_audacity\code\src\components\codeEditor\cl_codeEditor.py", line 198, in __init__
    self.blockCountChanged.connect(self.marginArea.update())
TypeError: argument 1 has unexpected type 'NoneType'
```

### MSG ChatGPT: