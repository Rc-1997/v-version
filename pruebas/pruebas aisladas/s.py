from tkinter import *

def func1():
    print("in func1")

def func2():
    print("in func2")

def selection():
    try:
        dictionary[listbox.selection_get()]()
    except:
        pass

root = Tk()

frame = Frame(root)
frame.pack()

dictionary = {"1":func1, "2":func2}

items = StringVar(value=tuple(sorted(dictionary.keys())))

listbox = Listbox(frame, listvariable=items, width=15, height=5)
listbox.grid(column=0, row=2, rowspan=6, sticky=("n", "w", "e", "s"))
listbox.focus()

selectButton = Button(frame, text='Select', underline = 0, command=selection)
selectButton.grid(column=2, row=4, sticky="e", padx=50, pady=50)

root.bind('<Double-1>', lambda x: selectButton.invoke())

root.mainloop()