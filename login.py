from Tkinter import *

# creates a window
root = Tk()

# login labels
label_1 = Label(root, text="Username:")
label_2 = Label(root, text="Password:")

# login text fields
entry_1 = Entry(root)
entry_2 = Entry(root)

# aligning login label and entry fields
label_1.grid(row=0, sticky=E)
label_2.grid(row=1, sticky=E)
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)

# keep me logged in checkbox
c = Checkbutton(root, text="Keep me logged in")
c.grid(columnspan=2)




# allows window to be continuously on the screen until exit/minimize
root.mainloop()
