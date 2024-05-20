import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import subprocess
import os

class ConsoleFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Création d'un widget ScrolledText pour afficher la console
        self.console_output = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.console_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Création d'un widget Entry pour saisir des commandes
        self.command_entry = tk.Entry(self)
        self.command_entry.pack(side=tk.BOTTOM, fill=tk.X)
        self.command_entry.bind("<Return>", self.execute_command)

    def execute_command(self, event):
        # Récupération de la commande saisie par l'utilisateur
        command = self.command_entry.get()
        # Exécution de la commande via un processus externe
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        # Lecture de la sortie et de l'erreur standard
        output, error = process.communicate()
        # Affichage du résultat dans la console
        self.console_output.insert(tk.END, output.decode())
        self.console_output.insert(tk.END, error.decode())
        # Effacer le champ de saisie après l'exécution de la commande
        self.command_entry.delete(0, tk.END)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Terminal intégré")

# Création de la frame pour la console
console_frame = ConsoleFrame(root)
console_frame.pack(fill=tk.BOTH, expand=True)

# Lancement de la boucle principale
root.mainloop()

'''
class PyApp(tk.Tk()):
    def __init__(self):
        super()
        self.title = "Network Audacity"

    def topbar(self):
        print("Hello Tkinker App!")

    def gest_mul_window(self):
        print("Multi Windows integration")

    def footbar(self):
        print("Goodbye Tkinter App🫡")
'''