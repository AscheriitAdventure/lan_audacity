import tkinter as tk
from tkinter import ttk
import nmap


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network Audacity")
        self.center_window()
        # Frame d'action
        act_frame = tk.Frame(self, height=50, bg="grey")
        act_frame.pack(side=tk.TOP, fill=tk.X)
        # Conteneur pour les objets alignés horizontalement
        container = tk.Frame(self)
        container.pack(pady=20)  # Espacement entre les objets
        self.list_device(container) 
        # Crée deux objets alignés horizontalement
        for _ in range(2):
            self.middle_object(container)
        # Frame de version
        version_frame = tk.Frame(self, height=10, bg="blue")
        version_frame.pack(side=tk.BOTTOM, fill=tk.X)

    def middle_object(self, parent):
        # LabelFrame pour la liste des appareils
        display_lf = ttk.LabelFrame(parent, text="Device List")
        display_lf.pack(side=tk.LEFT, padx=20)  # Utilisation de side=tk.LEFT pour aligner horizontalement

        # Création des boutons radio
        alignment_var = tk.StringVar()
        alignments = ('Left', 'Center', 'Right')
        for alignment in alignments:
            radio = ttk.Radiobutton(display_lf, text=alignment, value=alignment, variable=alignment_var)
            radio.pack(side=tk.LEFT, padx=10, pady=10)

    def list_device(self, parent):
        # LabelFrame pour la liste des appareils
        display_lf = ttk.LabelFrame(parent, text="Device List")
        display_lf.pack(side=tk.LEFT, padx=20)  # Utilisation de side=tk.LEFT pour aligner horizontalement

        # Création des boutons radio
        alignment_var = tk.StringVar()
        alignments = ('Left', 'Center', 'Right')
        for alignment in alignments:
            radio = ttk.Radiobutton(display_lf, text=alignment, value=alignment, variable=alignment_var)
            radio.pack(side=tk.TOP, padx=10, pady=10)  # Utilisation de side=tk.TOP pour aligner verticalement

    def center_window(self):
        # Récupère les dimensions de l'écran
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Récupère les dimensions de la fenêtre
        window_width = 1000
        window_height = 600

        # Calcule les coordonnées x et y pour centrer la fenêtre
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Place la fenêtre au centre de l'écran
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Exemple d'utilisation :
if __name__ == "__main__":
    app = Window()
    app.mainloop()
