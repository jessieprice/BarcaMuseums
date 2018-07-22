from Tkinter import *
import Tkinter as tk
import mysql as mdb
from PIL import ImageTk, Image
import pymysql
import mysql.connector


# connects python to database
# db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Jp13615!', db='BMTRS')
# cursor = db.cursor()

# print db

# general design things
headerFont = ('helvetica', '48', 'bold')
buttonFont = ('helvetica', '14')
tableFont = ('helvetica', '14', 'bold')

# master class that holds the container to switch between frames
# when you call this class, init method will immediately start it up
class museumApp(tk.Tk):

    # pass arguments into args, dictionaries into kwargs
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("1280x800")
        container = tk.Frame(self)

        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # an empty dictionary
        self.frames = {}

        for F in (mainPage, loginPage, registerPage, accountPage, redirectWindow,
                  wrongLoginWindow, manageAccountPage, allMuseumsPage, myTicketsPage,
                  myReviewsPage, curatorRequestPage):
            frame = F(container, self)
            self.frames[F] = frame

            # sticky = alignment + stretch (north south east west)
            # sticky nsew means to stretch in all directions
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(mainPage)

    def showFrame(self, controller):

        # frame is the dictionary of frames that was initialized in above method
        # looking for the value in the frames with key 'controller'
        frame = self.frames[controller]
        # then run the tkraise method on the selected frame
        frame.tkraise()


# first page that user sees, giving option to either login or register
class mainPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        frontLabel = tk.Label(self,
                              compound = tk.CENTER,
                              text = "BARCELONA MUSEUMS",
                              fg = "black",
                              font = headerFont)
        frontLabel.place(relx = .3, rely = .4, anchor = CENTER)

        # creates the login button which will eventually query database for user
        loginButton = Button(self, text= "Login",
                             command = lambda: controller.showFrame(loginPage))
        loginButton.config(height=0, width=35)
        loginButton.place(relx = 0.5, rely = 0.85, anchor = CENTER)
        loginButton.config(font = buttonFont, fg = "black")

        registerButton = Button(self, text="Register", font = buttonFont,
                                command = lambda: controller.showFrame(registerPage))
        registerButton.config(height = 0, width = 35)
        registerButton.place(relx = 0.8, rely = 0.85, anchor=CENTER)
        registerButton.config(font = buttonFont, fg = "black")


class loginPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        # def loginAction(em, pa):
        #     print em
        #     global entryEmail
        #     cursor.execute("SELECT Email FROM Visitor WHERE Email = 'em'")
        #     if cursor.rowcount == 0:
        #         print "saying can't be found"
        #         controller.showFrame(redirectWindow)
        #     else:
        #         cursor.execute("SELECT Email FROM Visitor WHERE Email = 'em' AND Password = 'pa'")
        #         if cursor.rowcount == 0:
        #             controller.showFrame(wrongLoginWindow)
        #         else:
        #             controller.showFrame(accountPage)

        emailLabel = Label(self, text = "Email: ", font = buttonFont)
        passLabel = Label(self, text = "Password: ", font = buttonFont)
        emailLabel.place(relx = .5, rely = .35, anchor = CENTER)
        passLabel.place(relx = .5, rely = .55, anchor = CENTER)

        entryEmail = Entry(self)
        entryPassword = Entry(self)

        entryEmail.place(relx = .5, rely = .4, anchor = CENTER)
        entryEmail.config(width = 75)
        entryPassword.place(relx = .5, rely = .6, anchor = CENTER)
        entryPassword.config(width=75)

        logButton = Button(self, text= "Login", font = buttonFont,
                           command = lambda: controller.showFrame(accountPage))
        logButton.config(width = 35)
        logButton.place(relx = .5, rely = .85, anchor = CENTER)


        backButton = Button(self, text = "Back to Main Page", font = buttonFont,
                            command = lambda: controller.showFrame(mainPage))
        backButton.config(width = 15)
        backButton.place(relx = .01, rely = .01)

        regButton = Button(self, text = "Whoops! I need to register!", font = buttonFont,
                           command = lambda: controller.showFrame(registerPage))
        regButton.config(width = 35)
        regButton.place(relx = .5, rely = .9, anchor = CENTER)


class registerPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        backButton = Button(self, text = "Back to Main Page", font = buttonFont,
                            command = lambda : controller.showFrame(mainPage))

        regButton = Button(self, text = "Register", font = buttonFont,
                           command = lambda: controller.showFrame(accountPage))

        backButton.config(width = 15)
        backButton.place(relx = .01, rely = .01)
        regButton.config(width = 35)
        regButton.place(relx = .5, rely = .95, anchor = CENTER)

        titleLabel = Label(self, text = "Register for Your Account", font = headerFont)
        emailLabel = Label(self, text = "Email: ", font = buttonFont)
        passLabel = Label(self, text = "Password: ", font = buttonFont)
        confirmLabel = Label(self, text = "Confirm Password: ", font = buttonFont)
        CCNumLabel = Label(self, text = "Credit Card Number: ")
        CCExpLabel = Label(self, text = "Credit Card Expiration Date: ")
        CCSecLabel = Label(self, text = "Credit Card Security Code: ")
        titleLabel.place(relx = .5, rely = .05, anchor = CENTER)
        emailLabel.place(relx=.2, rely=.3, anchor=CENTER)
        passLabel.place(relx=.2, rely=.4, anchor=CENTER)
        confirmLabel.place(relx = .2, rely = .5, anchor = CENTER)
        CCNumLabel.place(relx = .2, rely = .6, anchor = CENTER)
        CCExpLabel.place(relx = .3, rely = .7, anchor = CENTER)
        CCSecLabel.place(relx = .3, rely = .8, anchor = CENTER)

        createEmail = Entry(self)
        createPassword = Entry(self)
        createConfirm = Entry(self)
        createCCNum = Entry(self)
        createCCExp = Entry(self)
        createCCSec = Entry(self)

        createEmail.place(relx=.5, rely = .3, anchor=CENTER)
        createEmail.config(width=60)
        createPassword.place(relx=.5, rely=.4, anchor=CENTER)
        createPassword.config(width=60)
        createConfirm.place(relx=.5, rely = .5, anchor=CENTER)
        createConfirm.config(width=60)
        createCCNum.place(relx=.5, rely = .6, anchor=CENTER)
        createCCNum.config(width=60)
        createCCExp.place(relx=.5, rely = .7, anchor=CENTER)
        createCCExp.config(width=20)
        createCCSec.place(relx=.5, rely=.8, anchor=CENTER)
        createCCSec.config(width=20)


class redirectWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        goBackButton = Button(self, text = "You do not have an account. Click here if you would like to create one.",
                            font = buttonFont,
                            command = lambda: controller.showFrame(registerPage))
        goBackButton.place(relx = .5, rely = .5, anchor = CENTER)


class wrongLoginWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        goBackButton = Button(self, text = "Incorrect password. Click here to try again.",
                            font = buttonFont,
                            command = lambda: controller.showFrame(loginPage))
        goBackButton.place(relx = .5, rely = .5, anchor = CENTER)
        goBackButton.config(width = 80)

        homeButton = Button(self, text = "Back to Main Page", font = buttonFont,
                            command = lambda : controller.showFrame(mainPage))
        homeButton.config(width = 15)
        homeButton.place(relx = .01, rely = .01)


class accountPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        welcomeLabel = Label(self, text = "Welcome, Museum Friend!", font = headerFont)
        welcomeLabel.place(relx = .5, rely = .1, anchor = CENTER)

        # searchMuseumLabel = Label(self, text = "Select a Museum", font = buttonFont)
        # searchMuseumLabel.place(relx = .5, rely = .3, anchor = CENTER)

        allButton = Button(self, text = "View All Museums", font = buttonFont,
                           command = lambda: controller.showFrame(allMuseumsPage))
        allButton.config(width = 20)
        allButton.place(relx = .5, rely = .6, anchor = CENTER)

        myTickets = Button(self, text = "View My Tickets", font = buttonFont,
                           command = lambda: controller.showFrame(myTicketsPage))
        myTickets.config(width = 20)
        myTickets.place(relx = .5, rely = .65, anchor = CENTER)

        myReviews = Button(self, text = "Manage Reviews", font = buttonFont,
                           command = lambda : controller.showFrame(myReviewsPage))
        myReviews.config(width = 20)
        myReviews.place(relx = .5, rely = .7, anchor = CENTER)

        manageAccount = Button(self, text = "Manage Account", font = buttonFont,
                               command = lambda : controller.showFrame(manageAccountPage))
        manageAccount.config(width = 20)
        manageAccount.place(relx = .01, rely = .01)


class manageAccountPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        header = Label(self, text = "Manage Account", font = headerFont)
        header.place(relx = .5, rely = .1, anchor = CENTER)

        logoutButton = Button(self, text = "Logout", font = buttonFont,
                              command = lambda : controller.showFrame(mainPage))
        logoutButton.config(width = 40)
        logoutButton.place(relx = .5, rely = .6, anchor = CENTER)

        curatorButton = Button(self, text = "Make Curator Request", font = buttonFont,
                               command = lambda : controller.showFrame(curatorRequestPage))
        curatorButton.config(width = 40)
        curatorButton.place(relx = .5, rely = .7, anchor = CENTER)

        # this doesn't actually delete the account because need sql to do it
        deleteButton = Button(self, text = "Delete Account", font = buttonFont,
                              command = lambda : controller.showFrame(mainPage))
        deleteButton.config(width = 40)
        deleteButton.place(relx = .5, rely = .8, anchor = CENTER)

        backButton = Button(self, text="Return to Account Home Page", font=buttonFont,
                            command=lambda: controller.showFrame(accountPage))
        backButton.config(width=35)
        backButton.place(relx=.01, rely=.01)


class curatorRequestPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        header = Label(self, text="Curator Request", font=headerFont)
        header.place(relx=.5, rely=.1, anchor=CENTER)

        # need to insert drop down menu with all museum names

        backButton = Button(self, text="Back", font=buttonFont,
                            command=lambda: controller.showFrame(manageAccountPage))
        backButton.config(width=35)
        backButton.place(relx=.01, rely=.01)


class allMuseumsPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        header = Label(self, text = "All Museums", font = headerFont)
        header.place(relx = .5, rely = .1, anchor = CENTER)

        # sql = "SELECT Name FROM Museum"
        # cursor.execute(sql)
        # tableHeight = cursor.rowcount
        # HEIGHT SHOULD BE EQUAL TO NUMBER OF MUSEUMS ONCE THE DB IS CONNECTED
        tableHeight = 5

        name = Label(self, text = "Museum Name", font = tableFont)
        name.place(relx = .3, rely = .3, anchor = CENTER)

        rating = Label(self, text = "Average Rating", font = tableFont)
        rating.place(relx = .7, rely = .3, anchor = CENTER)

        musIncrement = .4

        for i in range(tableHeight):
            museumButton = Button(self, text="museum names should go here; should connect to museum page", font = buttonFont)
            museumButton.config(width = 60)
            museumButton.place(relx = .3, rely = musIncrement, anchor = CENTER)

            ratingLabel = Label(self, text = "ratings from sql function should go here", font = buttonFont)
            ratingLabel.place(relx = .7, rely = musIncrement, anchor = CENTER)
            musIncrement += .05

        backButton = Button(self, text = "Return to Account Page", font = buttonFont,
                            command = lambda : controller.showFrame(accountPage))
        backButton.config(width = 30)
        backButton.place(relx = .01, rely = .01)


class myTicketsPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        header = Label(self, text = "My Tickets", font = headerFont)
        header.place(relx = .5, rely = .1, anchor = CENTER)

        musName = Label(self, text = "Museum Name", font = tableFont)
        musName.place(relx = .2, rely = .3, anchor = CENTER)

        purchaseDate = Label(self, text = "Purchase Date", font = tableFont)
        purchaseDate.place(relx = .5, rely = .3, anchor = CENTER)

        money = Label(self, text = "Cost of Purchase", font = tableFont)
        money.place(relx = .8, rely = .3, anchor = CENTER)

        ticIncrement = .4

        tableHeight = 5

        for i in range(tableHeight):
            nameLabel = Label(self, text = "museum name that will come from db", font = buttonFont)
            nameLabel.place(relx = .2, rely = ticIncrement, anchor = CENTER)

            purLabel = Label(self, text = "purchase date from db will go here", font = buttonFont)
            purLabel.place(relx = .5, rely = ticIncrement, anchor = CENTER)

            moneyLabel = Label(self, text = "moneys paid info will go here", font = buttonFont)
            moneyLabel.place(relx = .8, rely = ticIncrement, anchor = CENTER)
            ticIncrement += .05

        backButton = Button(self, text="Return to Account Page", font=buttonFont,
                            command=lambda: controller.showFrame(accountPage))
        backButton.config(width=30)
        backButton.place(relx=.01, rely=.01)


class myReviewsPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        header = Label(self, text = "My Reviews", font = headerFont)
        header.place(relx = .5, rely = .1, anchor = CENTER)

        musName = Label(self, text = "Museum Name", font = tableFont)
        musName.place(relx = .2, rely = .3, anchor = CENTER)

        reviewLabel = Label(self, text = "Review", font = tableFont)
        reviewLabel.place(relx = .5, rely = .3, anchor = CENTER)

        ratingLabel = Label(self, text = "Rating", font = tableFont)
        ratingLabel.place(relx = .8, rely = .3, anchor = CENTER)

        tableHeight = 5
        tableIncrement = .4

        for i in range(tableHeight):
            nameLabel = Label(self, text = "museum name that will come from db", font = buttonFont,
                              wraplength = 125, justify = CENTER)
            nameLabel.place(relx = .2, rely = tableIncrement, anchor = CENTER)

            reviewLabel = Label(self, text = "i hated that museum i couldn't touch "
                                             "the exhibits and it made me sad how stupid",
                                font = buttonFont,
                                wraplength = 500, justify = CENTER)
            reviewLabel.place(relx=.5, rely=tableIncrement, anchor=CENTER)

            ratingLabel = Label(self, text="rating info will go here", font = buttonFont)
            ratingLabel.place(relx = .8, rely = tableIncrement, anchor = CENTER)
            tableIncrement += .1

        backButton = Button(self, text = "Return to Account Page", font = buttonFont,
                            command=lambda: controller.showFrame(accountPage))
        backButton.config(width = 30)
        backButton.place(relx = .01, rely = .01)

app = museumApp()
app.mainloop()