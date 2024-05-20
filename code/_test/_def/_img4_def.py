import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class EmbeddedTerminal(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        layout = QVBoxLayout(self)

        # Create a QFrame to act as the terminal
        self.terminal = QTextEdit(self)
        self.terminal.setReadOnly(True)
        layout.addWidget(self.terminal)

        # Create a QLineEdit for command input
        self.command_line = QLineEdit(self)
        layout.addWidget(self.command_line)

        # Start the terminal emulator inside the QFrame
        self.process = QProcess(self)
        self.process.start('bash', ['-i', '-l'], QIODevice.ReadWrite)
        self.process.waitForStarted()

        # Set the terminal widget as the process's standard output
        self.process.setProcessChannelMode(QProcess.ForwardedChannels)
        self.process.readyReadStandardOutput.connect(self.read_output)

        # Connect the command line returnPressed signal to execute command
        self.command_line.returnPressed.connect(self.execute_command)

    def read_output(self):
        output = self.process.readAllStandardOutput().data().decode()
        self.terminal.append(output)

    def execute_command(self):
        command = self.command_line.text()
        self.command_line.clear()
        self.process.write(command.encode() + b'\n')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = EmbeddedTerminal()
    main.show()
    sys.exit(app.exec_())
