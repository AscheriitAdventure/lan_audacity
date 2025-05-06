from qtpy.QtWidgets import *
from qtpy.QtCore import *


class WDialogs(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading...")
        self.setLayout(QVBoxLayout())
        self.progress_bar = QProgressBar(self)
        self.progress_label = QLabel("Synchronisation en cours...", self)

        self.layout().addWidget(self.progress_label)
        self.layout().addWidget(self.progress_bar)
        self.progress_bar.setValue(0)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def set_message(self, message: str):
        self.progress_label.setText(message)

    def set_maximum(self, max_value: int):
        self.progress_bar.setMaximum(max_value)

class WorkerTemplateDialog(QDialog):
    def __init__(self, parent=None, debug: bool = False):
        super().__init__(parent)

        self.active_fields: list = list()
        self.fields = {}
        self.title_window: str = "Worker Dialog"
        self.debug = debug

        ## Options du field
        self._opt_progress_bar: bool = False
        self._opt_value: bool = False
        self._opt_message: bool = False
        self._opt_time: bool = False
        self._opt_operations: bool = False
        self.loadUI()
    
    def loadUI(self):
        self.setWindowTitle(self.title_window)

        # Layout principal en vertical
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
    
    def setProgressBar(self):
        # Affiche la barre de progression
        if not self._opt_progress_bar:
            self._opt_progress_bar = True
            self.progress_bar = QProgressBar()
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)
            self.main_layout.addWidget(self.progress_bar)
            self.active_fields.append("progress_bar")
            self.fields["progress_bar"] = self.progress_bar

    def setValue(self, min_value: int = 0, max_value: int = 100):
        # Affiche la valeur de progression de la tâche
        if not self._opt_value:
            self._opt_value = True
            self.value_layout = QHBoxLayout()
            self.value_label = QLabel("Progress:")
            self.value_lcd = QLCDNumber()
            self.value_lcd.setDigitCount(3)
            self.value_lcd.display(0)
            
            self.value_layout.addWidget(self.value_label)
            self.value_layout.addWidget(self.value_lcd)
            
            self.main_layout.addLayout(self.value_layout)
            self.active_fields.append("value")
            self.fields["value"] = self.value_lcd
            
        if hasattr(self, 'progress_bar'):
            self.progress_bar.setRange(min_value, max_value)

    def setMessage(self, message: str = ""):
        # Affiche un message préparamétré/personnalisé
        if not self._opt_message:
            self._opt_message = True
            self.message_label = QLabel(message)
            self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.message_label.setWordWrap(True)
            
            self.main_layout.addWidget(self.message_label)
            self.active_fields.append("message")
            self.fields["message"] = self.message_label
        else:
            self.fields["message"].setText(message)

    def setTime(self):
        # Affiche le temps d'exécution de la tâche
        # Affiche le temps restant avant la fin de la tâche
        if not self._opt_time:
            self._opt_time = True
            self.time_layout = QHBoxLayout()
            
            self.elapsed_layout = QVBoxLayout()
            self.elapsed_label = QLabel("Temps écoulé:")
            self.elapsed_time = QLabel("00:00:00")
            self.elapsed_layout.addWidget(self.elapsed_label)
            self.elapsed_layout.addWidget(self.elapsed_time)
            
            self.remaining_layout = QVBoxLayout()
            self.remaining_label = QLabel("Temps restant:")
            self.remaining_time = QLabel("--:--:--")
            self.remaining_layout.addWidget(self.remaining_label)
            self.remaining_layout.addWidget(self.remaining_time)
            
            self.time_layout.addLayout(self.elapsed_layout)
            self.time_layout.addLayout(self.remaining_layout)
            
            self.main_layout.addLayout(self.time_layout)
            self.active_fields.append("time")
            self.fields["elapsed_time"] = self.elapsed_time
            self.fields["remaining_time"] = self.remaining_time
            
            # Créer un timer pour mettre à jour le temps écoulé
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateElapsedTime)
            self.start_time = QTime.currentTime()
            self.timer.start(1000)  # Update every second

    def updateElapsedTime(self):
        elapsed = self.start_time.secsTo(QTime.currentTime())
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        self.fields["elapsed_time"].setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def updateRemainingTime(self, total_seconds):
        if hasattr(self, 'progress_bar'):
            progress = self.progress_bar.value()
            max_val = self.progress_bar.maximum()
            if progress > 0:
                elapsed = self.start_time.secsTo(QTime.currentTime())
                estimated_total = elapsed * max_val / progress
                remaining = estimated_total - elapsed
                
                hours = int(remaining // 3600)
                minutes = int((remaining % 3600) // 60)
                seconds = int(remaining % 60)
                
                self.fields["remaining_time"].setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def setOperations(self):
        # Affiche les opérations en cours et terminées
        if not self._opt_operations:
            self._opt_operations = True
            self.operations_group = QGroupBox("Opérations")
            self.operations_layout = QVBoxLayout()
            
            self.current_op_layout = QHBoxLayout()
            self.current_op_label = QLabel("Opération en cours:")
            self.current_op_value = QLabel("--")
            self.current_op_layout.addWidget(self.current_op_label)
            self.current_op_layout.addWidget(self.current_op_value)
            
            self.completed_op_layout = QHBoxLayout()
            self.completed_op_label = QLabel("Opérations terminées:")
            self.completed_op_value = QLabel("0")
            self.completed_op_layout.addWidget(self.completed_op_label)
            self.completed_op_layout.addWidget(self.completed_op_value)
            
            self.operations_layout.addLayout(self.current_op_layout)
            self.operations_layout.addLayout(self.completed_op_layout)
            
            self.operations_log = QTextEdit()
            self.operations_log.setReadOnly(True)
            self.operations_log.setMaximumHeight(100)
            self.operations_layout.addWidget(self.operations_log)
            
            self.operations_group.setLayout(self.operations_layout)
            self.main_layout.addWidget(self.operations_group)
            
            self.active_fields.append("operations")
            self.fields["current_operation"] = self.current_op_value
            self.fields["completed_operations"] = self.completed_op_value
            self.fields["operations_log"] = self.operations_log
            
            self.completed_count = 0
    
    def updateProgress(self, value):
        if "progress_bar" in self.active_fields:
            self.progress_bar.setValue(value)
        if "value" in self.active_fields:
            self.value_lcd.display(value)
        if "time" in self.active_fields:
            self.updateRemainingTime(value)
    
    def logOperation(self, operation_name):
        if "operations" in self.active_fields:
            self.fields["current_operation"].setText(operation_name)
            timestamp = QTime.currentTime().toString("hh:mm:ss")
            self.fields["operations_log"].append(f"[{timestamp}] {operation_name}")
    
    def completeOperation(self, operation_name=""):
        if "operations" in self.active_fields:
            self.completed_count += 1
            self.fields["completed_operations"].setText(str(self.completed_count))
            timestamp = QTime.currentTime().toString("hh:mm:ss")
            if operation_name:
                self.fields["operations_log"].append(f"[{timestamp}] ✓ {operation_name} terminé")
            self.fields["current_operation"].setText("--")

