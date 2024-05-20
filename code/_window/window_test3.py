from tkinter import *

def get_selection():
    '''
    Get users selection and print to terminal.
    '''
    selection = lb_of_cities.curselection()  # function takes current selection from listbox
    print(lb_of_cities.get(selection))

root = Tk()
root.title("Place layout Example")
root.geometry("300x300+50+100")  # width x length + x + y

# create label in window
text = Label(root, text="Which of the following cities would you like to travel to?", wraplength=200)
text.place(x=50, y=20)

# create listbox to hold names
lb_of_cities = Listbox(root, selectmode=BROWSE, width = 24)  # width is equal to number of characters
lb_of_cities.place(x=40, y=65)
cities = ["Beijing", "Singapore", "Tokyo", "Dubai", "New York"]

# add items to listbox
for  c  in  cities:
    lb_of_cities.insert(END, c)

# set binding on item select in listbox
# when item of listbox is selected, call the function get_selection
lb_of_cities.bind("&lt;&lt;ListboxSelect&gt;&gt;", lambda event:  get_selection())

# button to close application
end_button = Button(root, text="End", command=quit)
end_button.place(x=125, y=250)

root.mainloop()