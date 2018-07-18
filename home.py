from Tkinter import *

# creates a window
root = Tk()

topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

# header
label_login = Label(topFrame, text="Welcome, user@gatech.edu")
label_login.grid(row=0, columnspan=3)

# type or choose a museum label/entry
entry_TypMsm = Entry(topFrame, width=35)
entry_TypMsm.grid(row=1, column=1)
entry_TypMsm.delete(0, END)
entry_TypMsm.insert(0, "Type or Choose a Museum")

# museum drop down menu options
MSM_OPTIONS = [
    "Museum 1",
    "Museum 2",
    "Museum 3"
]  # etc

variable = StringVar(topFrame)
variable.set(MSM_OPTIONS[0])  # default value

# museums drop down menu
msm_dropdown = OptionMenu(topFrame, variable, *MSM_OPTIONS)
msm_dropdown.grid(row=1, column=2)

# view all museums button
allMsms_btn = Button(topFrame, text="View All Museums")
allMsms_btn.grid(row=2, columnspan=3)

# my tickets button
my_tix_btn = Button(topFrame, text="Create Account")
my_tix_btn.grid(row=3, columnspan=3)

# my reviews button
myRvws_btn = Button(topFrame, text="My Reviews")
myRvws_btn.grid(row=4, columnspan=3)

# manage account button
mngAcct_btn = Button(bottomFrame, text="Manage Account")
mngAcct_btn.pack()

# allows window to be continuously on the screen until exit/minimize
root.mainloop()
