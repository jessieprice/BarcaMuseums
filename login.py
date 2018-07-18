from Tkinter import *

# creates a window
root = Tk()

# header
label_login = Label(root, text="Barcelona Museum Ticketing")
label_login.grid(row=0, columnspan=2)

# login labels
label_un = Label(root, text="Username:")
label_pw = Label(root, text="Password:")

# login text fields
entry_un = Entry(root)
entry_pw = Entry(root)

# aligning login label and entry fields
label_un.grid(row=1, sticky=E)
label_pw.grid(row=2, sticky=E)
entry_un.grid(row=1, column=1)
entry_pw.grid(row=2, column=1)

# keep me logged in checkbox
c = Checkbutton(root, text="Keep me logged in")
c.grid(columnspan=2)

# login button
login_btn = Button(root, text="Login")
login_btn.grid(row=4, columnspan=2)

# new user link
label_nwUsr = Label(root, text="New user? Create account here")
label_nwUsr.grid(row=5, columnspan=2)

# allows window to be continuously on the screen until exit/minimize
root.mainloop()
