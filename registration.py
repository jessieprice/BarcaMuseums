from Tkinter import *

# creates a window
root = Tk()

# header
label_login = Label(root, text="New User Registration")
label_login.grid(row=0, columnspan=2)

# registration labels
label_em = Label(root, text="Email:")
label_pw = Label(root, text="Password:")
label_cnfmPw = Label(root, text="Confirm Password:")
label_ccNum = Label(root, text="Credit Card Number:")
label_ccExpr = Label(root, text="Credit Card Exp. Date:")
label_ccSec = Label(root, text="Credit Card Security Code:")

# login text fields
entry_em = Entry(root)
entry_pw = Entry(root)
entry_cnfmPw = Entry(root)
entry_ccNum = Entry(root)
entry_ccExpr = Entry(root)
entry_ccSec = Entry(root)

# aligning login label and entry fields
label_em.grid(row=1, sticky=E)
label_pw.grid(row=2, sticky=E)
label_cnfmPw.grid(row=3, sticky=E)
label_ccNum.grid(row=4, sticky=E)
label_ccExpr.grid(row=5, sticky=E)
label_ccSec.grid(row=6, sticky=E)

entry_em.grid(row=1, column=1)
entry_pw.grid(row=2, column=1)
entry_cnfmPw.grid(row=3, column=1)
entry_ccNum.grid(row=4, column=1)
entry_ccExpr.grid(row=5, column=1)
entry_ccSec.grid(row=6, column=1)

# create account button
create_acct = Button(root, text="Create Account")
create_acct.grid(row=7, columnspan=2)

# back button
back = Button(root, text="Back")
back.grid(row=8, columnspan=2)


# allows window to be continuously on the screen until exit/minimize
root.mainloop()
