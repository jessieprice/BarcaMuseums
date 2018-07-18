from Tkinter import *

# creates a window
root = Tk()

# rectangular frames
topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

# buttons
button1 = Button(topFrame, text="Button 1", fg="red")
button2 = Button(topFrame, text="Button 2", fg="blue")
button3 = Button(topFrame, text="Button 3", fg="green")
button4 = Button(bottomFrame, text="Button 4", fg="purple")

# pack the buttons in order to display them
button1.pack()
button2.pack()
button3.pack()
button4.pack()

# allows window to be continuously on the screen until exit/minimize
root.mainloop()
