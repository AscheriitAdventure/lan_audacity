import tkinter as tk


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
