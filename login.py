from Tkinter import *

# creates a window
root = Tk()

# creates a label with text
theLabel = Label(root, text="This is text")

# "packs" the label somewhere on the screen (no formatting)
theLabel.pack()

# allows window to be continuously on the screen until exit/minimize is pressed
root.mainloop()
