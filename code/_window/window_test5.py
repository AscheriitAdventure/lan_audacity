import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess


class TerminalApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.terminal_process = None
        self.title("Terminal Interactif")

        # Création d'une zone de texte pour afficher la sortie
        self.output_text = ScrolledText(self, wrap=tk.WORD)
        self.output_text.pack(expand=True, fill=tk.BOTH)

        # Création d'un champ d'entrée pour saisir les commandes
        self.input_entry = tk.Entry(self)
        self.input_entry.pack(expand=False, fill=tk.X)
        self.input_entry.bind("<Return>", self.execute_command)

        # Démarrage du terminal
        self.start_terminal()

    def start_terminal(self):
        # Démarrage du processus de terminal
        self.terminal_process = subprocess.Popen(
            ["bash"],  # ou "cmd" pour Windows
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
            shell=True,
            cwd="/",  # Changer le répertoire de travail si nécessaire
        )

        # Fonction de mise à jour de la sortie
        self.update_output()

    def execute_command(self, event):
        # Récupération de la commande saisie
        command = self.input_entry.get().strip()
        # Envoi de la commande au terminal
        self.terminal_process.stdin.write(command + "\n")
        self.terminal_process.stdin.flush()
        # Effacement du champ de saisie
        self.input_entry.delete(0, tk.END)

    def update_output(self):
        # Lecture de la sortie du terminal
        output = self.terminal_process.stdout.readline()
        # Affichage de la sortie
        if output:
            self.output_text.insert(tk.END, output)
            self.output_text.see(tk.END)
        # Réexécution de la fonction après un court délai
        self.after(10, self.update_output)

if __name__ == "__main__":
    app = TerminalApp()
    app.mainloop()
