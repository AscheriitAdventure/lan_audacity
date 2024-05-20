import tkinter as tk


class Application(tk.Frame):
  def __init__(self, master):
    super().__init__(master)
    self.pack()
    master.geometry("300x300")
    master.title("Fenêtre de base")

    self.window = []
    self.user = []

    self.button = tk.Button(master,text="Création de fenêtres",command=self.buttonClick,width=10)
    self.button.place(x=110, y=150)
    self.button.config(fg="black", bg="skyblue")

  def buttonClick(self):
    self.window.append(tk.Toplevel())
    self.user.append(User(self.window[len(self.window)-1],len(self.window)))

class User(tk.Frame):
  def __init__(self,master,num):
    super().__init__(master)
    self.pack()
    self.num = num
    master.geometry("300x300")
    master.title(str(self.num)+"Deuxième fenêtre créée")

    self.button = tk.Button(master,text="Confirmation sur la console",command=self.buttonClick,width=20)
    self.button.place(x=70, y=150)
    self.button.config(fg="black", bg="pink")

  def buttonClick(self):
    print("C'est"+str(self.num)+"C'est la deuxième fenêtre créée.")

def main():
  win = tk.Tk()
  app = Application(win)
  app.mainloop()

if __name__ == '__main__':
  main()