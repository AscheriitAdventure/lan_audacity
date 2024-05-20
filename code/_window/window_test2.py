from tkinter import *

fenetre = Tk()
fenetre.title("Mon application")

cadre1 = Frame(fenetre)
cadre1.pack()

bouton1 = Button(cadre1, text="bouton1")
bouton2 = Button(cadre1, text="bouton2")
bouton3 = Button(cadre1, text="bouton3")

bouton1.pack()
bouton2.pack()
bouton3.pack()

fenetre.mainloop()