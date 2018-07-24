from Tkinter import *
import Tkinter as tk
import pymysql
from datetime import datetime

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Jp13615!', db='BMTRS', autocommit = True)
cursor = db.cursor()


headerFont = ('helvetica', '48', 'bold')
buttonFont = ('helvetica', '14')
tableFont = ('helvetica', '14', 'bold')

global user
user = "none"

global museumSelected
museumSelected = "none"

global accountType
accountType = "none"


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

        for F in (loginPage, registerPage, accountPage, redirectWindow, wrongLoginWindow,
                  manageAccountPage, allMuseumsPage, myTicketsPage, myReviewsPage, curatorRequestPage,
                  passDifference, viewMuseumPage, curatorAccountPage, adminAccountPage, allReviewsPage, reviewMuseumPage,
                  curatorMyMuseumsPage, acceptCuratorRequestPage, adminAddMuseumPage, adminDeleteMuseumPage, curatorMyMuseumsPage,
                  addExhibitPage, curatorViewMuseumPage):
            frame = F(container, self)
            self.frames[F] = frame

            # sticky = alignment + stretch (north south east west)
            # sticky nsew means to stretch in all directions
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(loginPage)

    def showFrame(self, controller):
        # frame is the dictionary of frames that was initialized in above method
        # looking for the value in the frames with key 'controller'
        frame = self.frames[controller]
        frame.update()
        # then run the tkraise method on the selected frame
        frame.tkraise()


class loginPage(tk.Frame):

    def __init__(self, parent, controller):

        self.controller = controller

        tk.Frame.__init__(self, parent)

        frontLabel = tk.Label(self,
                              compound = tk.CENTER,
                              text = "BARCELONA MUSEUMS",
                              fg = "black",
                              font = headerFont)
        frontLabel.place(relx = .3, rely = .2, anchor = CENTER)

        self.emailLabel = Label(self, text = "Email: ", font = buttonFont)
        self.passLabel = Label(self, text = "Password: ", font = buttonFont)
        self.emailLabel.place(relx = .5, rely = .45, anchor = CENTER)
        self.passLabel.place(relx = .5, rely = .55, anchor = CENTER)

        self.entryEmail = Entry(self)
        global user
        user = str(self.entryEmail)
        self.entryPassword = Entry(self)

        self.entryEmail.place(relx = .5, rely = .5, anchor = CENTER)
        self.entryEmail.config(width = 50)
        self.entryPassword.place(relx = .5, rely = .6, anchor = CENTER)
        self.entryPassword.config(width = 50)

        self.logButton = Button(self, text= "Login", font = buttonFont,
                           command = self.login)

        self.logButton.config(width = 30)
        self.logButton.place(relx = .5, rely = .7, anchor = CENTER)

        self.regButton = Button(self, text = "Register", font = buttonFont,
                           command = lambda: controller.showFrame(registerPage))
        self.regButton.config(width = 30)
        self.regButton.place(relx = .5, rely = .75, anchor = CENTER)

    def login(self):
        global accountType
        global user
        user = str(self.entryEmail.get())
        pa = self.entryPassword.get()

        cursor.execute("SELECT Email FROM BMTRS.Admin WHERE Email = %s AND Pass = %s", (user, pa))
        if cursor.rowcount == 1:
            accountType = "admin"
            self.controller.showFrame(adminAccountPage)
        else:
            cursor.execute("SELECT Email FROM BMTRS.Admin WHERE Email = %s", user)
            if cursor.rowcount == 1:
                self.controller.showFrame(wrongLoginWindow)
            else:
                cursor.execute("SELECT CuratorEmail FROM Museum WHERE CuratorEmail = %s", user)
                if cursor.rowcount > 0:
                    cursor.execute("SELECT Email FROM Visitor WHERE Email = %s AND Pass = %s", (user, pa))
                    if cursor.rowcount == 1:
                        accountType = "curator"
                        self.controller.showFrame(curatorAccountPage)
                    else:
                            self.controller.showFrame(wrongLoginWindow)
                else:
                    cursor.execute("SELECT Email FROM Visitor WHERE Email = %s AND Pass = %s", (user, pa))
                    if cursor.rowcount == 1:
                        accountType = "visitor"
                        self.controller.showFrame(accountPage)
                    else:
                        cursor.execute("SELECT Email FROM Visitor WHERE Email = %s", user)
                        if cursor.rowcount == 1:
                            self.controller.showFrame(wrongLoginWindow)
                        else:
                            self.controller.showFrame(redirectWindow)
        self.returnEmail()

    def returnEmail(self):
        return str(user)


class registerPage(tk.Frame):

    def __init__(self, parent, controller):

        self.controller = controller

        tk.Frame.__init__(self, parent)

        self.backButton = Button(self, text = "Back", font = buttonFont,
                            command = lambda : controller.showFrame(loginPage))

        self.regButton = Button(self, text = "Register", font = buttonFont,
                           command = self.register)

        self.backButton.config(width = 30)
        self.backButton.place(relx = .5, rely = .85, anchor = CENTER)
        self.regButton.config(width = 30)
        self.regButton.place(relx = .5, rely = .8, anchor = CENTER)

        self.titleLabel = Label(self, text = "Register for Your Account", font = headerFont)
        self.emailLabel = Label(self, text = "Email: ", font = buttonFont)
        self.passLabel = Label(self, text = "Password: ", font = buttonFont)
        self.confirmLabel = Label(self, text = "Confirm Password: ", font = buttonFont)
        self.CCNumLabel = Label(self, text = "Credit Card Number: ")
        self.CCExpLabelMonth = Label(self, text = "Credit Card Exp. Month: ")
        self.CCExpLabelYear = Label(self, text = "Credit Card Exp. Year:")
        self.CCSecLabel = Label(self, text = "Credit Card Security Code: ")

        self.titleLabel.place(relx = .5, rely = .05, anchor = CENTER)
        self.emailLabel.place(relx=.1, rely=.3)
        self.passLabel.place(relx=.1, rely=.4)
        self.confirmLabel.place(relx = .1, rely = .5)
        self.CCNumLabel.place(relx = .1, rely = .6)
        self.CCExpLabelMonth.place(relx = .1, rely = .7)
        self.CCExpLabelYear.place(relx = .35, rely = .7)
        self.CCSecLabel.place(relx = .6, rely = .7)

        self.createEmail = Entry(self)
        self.createPassword = Entry(self)
        self.createConfirm = Entry(self)
        self.createCCNum = Entry(self)
        self.createCCExpMonth = Entry(self)
        self.createCCExpYear = Entry(self)
        self.createCCSec = Entry(self)

        self.createEmail.place(relx=.25, rely = .3)
        self.createEmail.config(width=60)
        self.createPassword.place(relx=.25, rely=.4)
        self.createPassword.config(width=60)
        self.createConfirm.place(relx=.25, rely = .5)
        self.createConfirm.config(width=60)
        self.createCCNum.place(relx=.25, rely = .6)
        self.createCCNum.config(width=60)
        self.createCCExpMonth.place(relx=.25, rely = .7)
        self.createCCExpMonth.config(width = 5)
        self.createCCExpYear.place(relx =  .48, rely = .7)
        self.createCCExpYear.config(width = 5)
        self.createCCSec.place(relx=.75, rely=.7)
        self.createCCSec.config(width=5)

    def register(self):
        em = self.createEmail.get()
        pa = self.createPassword.get()
        co = self.createConfirm.get()
        ccnum = self.createCCNum.get()
        ccexpm = self.createCCExpMonth.get()
        ccexpy = self.createCCExpYear.get()
        ccsec = self.createCCSec.get()
        if (pa == co):
            stuff = "INSERT INTO Visitor(Email, Pass, CCNum, CCExpMonth, CCExpYear, CCSecNum) " \
                    "VALUES(%s, %s, %s, %s, %s, %s)"
            cursor.execute(stuff, (em, pa, ccnum, ccexpm, ccexpy, ccsec))
            db.commit()

            self.controller.showFrame(accountPage)
        else:
            self.controller.showFrame(passDifference)


class passDifference(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        badButton = Button(self, text = "Passwords did not match. Click here to try again.", font = buttonFont,
                           command = lambda: controller.showFrame(registerPage))
        badButton.config(width = 80)
        badButton.place(relx = .5, rely = .5, anchor = CENTER)

        self.backButton = Button(self, text="Back", font=buttonFont,
                            command=lambda: controller.showFrame(loginPage))
        self.backButton.config(width=30)
        self.backButton.place(relx=.01, rely=.85)


class redirectWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.backButton = Button(self, text = "You do not have an account. Click here if you would like to create one.",
                            font = buttonFont,
                            command = lambda: controller.showFrame(registerPage))
        self.backButton.place(relx = .5, rely = .5, anchor = CENTER)


class wrongLoginWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.backButton = Button(self, text = "Incorrect password. Click here to try again.",
                            font = buttonFont,
                            command = lambda: controller.showFrame(loginPage))
        self.backButton.place(relx = .5, rely = .5, anchor = CENTER)
        self.backButton.config(width = 50)



class accountPage(tk.Frame):

    def __init__(self, parent, controller):

        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)

        welcomeLabel = Label(self, text = "Welcome, Museum Friend!", font = headerFont)
        welcomeLabel.place(relx = .5, rely = .1, anchor = CENTER)


        self.museumLabel = Label(self, text = "Search for Museum: ", font = buttonFont)
        self.museumLabel.place(relx = .2, rely = .5, anchor = CENTER)
        self.v = StringVar()
        self.entryMuseum = Entry(self, textvariable=self.v)
        self.entryMuseum.pack()
        global museumSelected
        museumSelected = self.v.get()

        self.entryMuseum.place(relx=.45, rely=.5, anchor=CENTER)
        self.entryMuseum.config(width=50)

        self.museumButton = Button(self, text="View Museum", font=buttonFont,
                                   command=lambda: self.onButton())
        self.museumButton.config(width=15)

        self.museumButton.place(relx=.7, rely=.5, anchor=CENTER)


        allMuseums = Button(self, text = "View All Museums", font = buttonFont,
                           command = lambda: controller.showFrame(allMuseumsPage))
        allMuseums.config(width = 30)
        allMuseums.place(relx = .5, rely = .6, anchor = CENTER)

        myTickets = Button(self, text = "My Tickets", font = buttonFont,
                           command = lambda: controller.showFrame(myTicketsPage))
        myTickets.config(width = 30)
        myTickets.place(relx = .5, rely = .65, anchor = CENTER)

        myReviews = Button(self, text = "My Reviews", font = buttonFont,
                           command = lambda : controller.showFrame(myReviewsPage))
        myReviews.config(width = 30)
        myReviews.place(relx = .5, rely = .7, anchor = CENTER)

        manageAccount = Button(self, text = "Manage Account", font = buttonFont,
                               command = lambda : controller.showFrame(manageAccountPage))
        manageAccount.config(width = 30)
        manageAccount.place(relx = .7, rely = .85)

    def onButton(self):
        global museumSelected
        museumSelected = self.v.get()
        query = "SELECT Name FROM Museum WHERE Name = %s"
        cursor.execute(query, (museumSelected))
        if cursor.rowcount == 1:
            self.controller.showFrame(viewMuseumPage)
        else:
            self.controller.showFrame(accountPage)


class curatorAccountPage(tk.Frame):

    def __init__(self, parent, controller):

        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)

        welcomeLabel = Label(self, text = "Welcome, Museum Friend!", font = headerFont)
        welcomeLabel.place(relx = .5, rely = .1, anchor = CENTER)


        self.museumLabel = Label(self, text = "Search for Museum: ", font = buttonFont)
        self.museumLabel.place(relx = .2, rely = .5, anchor = CENTER)
        self.v = StringVar()
        self.entryMuseum = Entry(self, textvariable=self.v)
        self.entryMuseum.pack()
        global museumSelected
        museumSelected = self.v.get()

        self.entryMuseum.place(relx=.45, rely=.5, anchor=CENTER)
        self.entryMuseum.config(width=50)

        self.museumButton = Button(self, text="View Museum", font=buttonFont,
                                   command=lambda: self.onButton())
        self.museumButton.config(width=15)

        self.museumButton.place(relx=.7, rely=.5, anchor=CENTER)


        allMuseums = Button(self, text = "View All Museums", font = buttonFont,
                           command = lambda: controller.showFrame(allMuseumsPage))
        allMuseums.config(width = 30)
        allMuseums.place(relx = .5, rely = .6, anchor = CENTER)

        myTickets = Button(self, text = "My Tickets", font = buttonFont,
                           command = lambda: controller.showFrame(myTicketsPage))
        myTickets.config(width = 30)
        myTickets.place(relx = .5, rely = .65, anchor = CENTER)

        myReviews = Button(self, text = "My Reviews", font = buttonFont,
                           command = lambda : controller.showFrame(myReviewsPage))
        myReviews.config(width = 30)
        myReviews.place(relx = .5, rely = .7, anchor = CENTER)

        myMuseums = Button(self, text = "My Museums", font = buttonFont,
                           command = lambda : controller.showFrame(curatorMyMuseumsPage))
        myMuseums.config(width = 30)
        myMuseums.place(relx = .5, rely = .75, anchor = CENTER)

        manageAccount = Button(self, text = "Manage Account", font = buttonFont,
                               command = lambda : controller.showFrame(manageAccountPage))
        manageAccount.config(width = 30)
        manageAccount.place(relx = .7, rely = .85)

    def onButton(self):
        global museumSelected
        museumSelected = self.v.get()
        query = "SELECT Name FROM Museum WHERE Name = %s"
        cursor.execute(query, (museumSelected))
        if cursor.rowcount == 1:
            self.controller.showFrame(viewMuseumPage)
        else:
            global accountType
            if accountType == "curator":
                self.controller.showFrame(curatorAccountPage)
            elif accountType == "admin":
                self.controller.showFrame(adminAccountPage)
            else:
                self.controller.showFrame(accountPage)


class curatorMyMuseumsPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        welcomeLabel = Label(self, text = "My Museums", font = headerFont)
        welcomeLabel.place(relx = .5, rely = .1, anchor = CENTER)
        global museumSelected
        museumLabel = Label(self, text = "Museum Name", font = buttonFont)
        museumLabel.place(relx = .3, rely = .3, anchor = CENTER)

        exhibitCountLabel = Label(self, text = "Exhibit Counts", font = buttonFont)
        exhibitCountLabel.place(relx = .6, rely = .3, anchor =  CENTER)

        ratingLabel = Label(self, text = "Rating", font = buttonFont)
        ratingLabel.place(relx = .8, rely = .3, anchor = CENTER)

        self.backButton = Button(self, text="Back", font=buttonFont,
                            command=lambda: controller.showFrame(curatorAccountPage))
        self.backButton.config(width=30)
        self.backButton.place(relx=.01, rely=.85)


        self.musIncrement = .4
        self.parent = parent
        self.controller = controller

        self.curMusList = self.viewCuratorMuseums()
        self.musName = []
        self.exhibitCountList = []
        self.ratingList = []
        for self.mus in self.curMusList:
            self.musNameButton = Button(self, text = self.mus[0], font = buttonFont, command = lambda text=self.mus[0]: self.OnClick(text))
            self.musNameButton.config(width = 60)
            self.musNameButton.place(relx = .3, rely = self.musIncrement, anchor = CENTER)
            self.musName.append(self.musNameButton)

            self.exhibitsInMuseum = self.countExhibits(self.mus[0])
            self.exhibitCountLab = Label(self, text = self.exhibitsInMuseum, font = buttonFont)
            self.exhibitCountLab.place(relx = .6, rely = self.musIncrement, anchor = CENTER)
            self.exhibitCountList.append(self.exhibitCountLab)

            self.ratingAvg = Label(self, text = self.mus[1], font = buttonFont)
            self.ratingAvg.place(relx = .8, rely = self.musIncrement, anchor = CENTER)
            self.ratingList.append(self.ratingAvg)

            self.musIncrement += .1

    def viewCuratorMuseums(self):
        self.museums = []
        query = "SELECT Name, AvgRating FROM Museum WHERE curatorEmail = %s"
        cursor.execute(query, user)
        for row in cursor.fetchall():
            name = row[0]
            rate = "SELECT AVG(Rating) FROM Review WHERE MuseumName = %s"
            cursor.execute(rate, (name))
            list = []
            list.append(row[0])
            for rate in cursor.fetchone():
                list.append(rate)
            self.museums.append(list)
        return self.museums

    def countExhibits(self, mName):
        self.exhibs = []
        query = "SELECT ExhibitName FROM Exhibit WHERE MuseumName = %s"
        cursor.execute(query, mName)
        result = cursor.rowcount
        return result

    def OnClick(self, text):
        global user
        global museumSelected
        museumSelected = text
        self.controller.showFrame(curatorViewMuseumPage)

    def update(self):
        global user
        self.curMusList = self.viewCuratorMuseums()
        self.musName = []
        self.exhibitCountList = []
        self.ratingList = []
        self.musIncrement = .4
        for self.museum in self.musName:
            self.museum.destroy()
        for self.count in self.exhibitCountList:
            self.count.destroy()
        for self.rating in self.ratingList:
            self.rating.destroy()

        for self.mus in self.curMusList:
            self.musNameButton = Button(self, text=self.mus[0], font=buttonFont, command = lambda text=self.mus[0]: self.OnClick(text))
            self.musNameButton.config(width=60)
            self.musNameButton.place(relx=.3, rely=self.musIncrement, anchor=CENTER)
            self.musName.append(self.musNameButton)

            self.exhibitsInMuseum = self.countExhibits(self.mus[0])
            self.exhibitCountLab = Label(self, text = self.exhibitsInMuseum, font = buttonFont)
            self.exhibitCountLab.place(relx = .6, rely = self.musIncrement, anchor = CENTER)
            self.exhibitCountList.append(self.exhibitCountLab)

            self.ratingAvg = Label(self, text = self.mus[1], font = buttonFont)
            self.ratingAvg.place(relx = .8, rely = self.musIncrement, anchor = CENTER)
            self.ratingList.append(self.ratingAvg)

            self.musIncrement += .05





class adminAccountPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        welcomeLabel = Label(self, text = "Welcome, Museum Friend!", font = headerFont)
        welcomeLabel.place(relx = .5, rely = .1, anchor = CENTER)

        acceptCuratorRequest = Button(self, text = "Accept Curator Requests", font = buttonFont,
                           command = lambda: controller.showFrame(acceptCuratorRequestPage))
        acceptCuratorRequest.config(width = 30)
        acceptCuratorRequest.place(relx = .5, rely = .4, anchor = CENTER)

        addMuseum = Button(self, text = "Add Museum", font = buttonFont,
                           command = lambda: controller.showFrame(adminAddMuseumPage))
        addMuseum.config(width = 30)
        addMuseum.place(relx = .5, rely = .45, anchor = CENTER)

        deleteMuseum = Button(self, text = "Delete Museum", font = buttonFont,
                           command = lambda : controller.showFrame(adminDeleteMuseumPage))
        deleteMuseum.config(width = 30)
        deleteMuseum.place(relx = .5, rely = .5, anchor = CENTER)

        logoutButton = Button(self, text = "Logout", font = buttonFont,
                              command = lambda : controller.showFrame(loginPage))
        logoutButton.config(width = 30)
        logoutButton.place(relx = .5, rely = .55, anchor = CENTER)

class adminAddMuseumPage(tk.Frame):

    def __init__(self, parent, controller):

        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)


        self.titleLabel = Label(self, text = "Add Museum", font = headerFont)
        self.titleLabel.place(relx = .5, rely = .05, anchor = CENTER)

        self.submitLabel = Label(self, text = "Submit Museum: ", font = buttonFont)
        self.submitLabel.place(relx = .2, rely = .5, anchor = CENTER)
        self.v = StringVar()
        self.entryMuseumName = Entry(self, textvariable=self.v)
        museumName = self.v.get()

        self.entryMuseumName.place(relx=.45, rely=.5, anchor=CENTER)
        self.entryMuseumName.config(width=50)

        self.submitMuseumButton = Button(self, text="Submit Museum", font=buttonFont,
                                   command=lambda: self.submitMuseum())
        self.submitMuseumButton.config(width=15)
        self.submitMuseumButton.place(relx=.7, rely=.5, anchor=CENTER)

        self.backButton = Button(self, text = "Back", font = buttonFont,
                            command = lambda : controller.showFrame(adminAccountPage))
        self.backButton.config(width=30)
        self.backButton.place(relx=.01, rely=.85)


    def submitMuseum(self):
        museumName = self.v.get()
        cursor.execute("INSERT INTO Museum(Name) VALUES(%s)", (museumName))
        self.controller.showFrame(allMuseumsPage)

class adminDeleteMuseumPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        header = Label(self, text = "Delete Museum Form", font = headerFont)
        header.place(relx = .5, rely = .1, anchor = CENTER)

        self.controller = controller
        self.parent = parent
        name = Label(self, text = "Which museum would you like to delete?", font = tableFont)
        name.place(relx = .5, rely = .3, anchor = CENTER)

        self.musIncrement = .4
        self.listmus = self.viewAllMuseums()
        self.buttonList = []

        for museum in self.listmus:
            self.museumButton = Button(self, text=museum, font=buttonFont, command = lambda text=museum: self.OnClick(text))
            self.museumButton.config(width=60)
            self.museumButton.place(relx=.5, rely=self.musIncrement, anchor=CENTER)
            self.buttonList.append(self.museumButton)

            self.musIncrement += .05

        self.backButton = Button(self, text="Back", font=buttonFont,
                            command=lambda: controller.showFrame(adminAccountPage))
        self.backButton.config(width=30)
        self.backButton.place(relx=.01, rely=.85)


    def viewAllMuseums(self):
        self.museums = []
        query = "SELECT Name FROM Museum"
        cursor.execute(query)
        for row in cursor.fetchall():
            self.museums.append(row[0])
        return self.museums

    def OnClick(self, text):
        global museumSelected
        museumSelected = text
        cursor.execute("DELETE FROM Museum WHERE Name = %s", museumSelected)
        self.controller.showFrame(adminDeleteMuseumPage)

    def update(self):
        self.musIncrement = .4
        for self.button in self.buttonList:
            self.button.destroy()

        self.listmus = self.viewAllMuseums()
        self.buttonList = []
        for museum in self.listmus:
            self.museumButton = Button(self, text=museum, font=buttonFont, command = lambda text=museum: self.OnClick(text))
            self.museumButton.config(width=60)
            self.museumButton.place(relx=.5, rely=self.musIncrement, anchor=CENTER)
            self.buttonList.append(self.museumButton)

            self.musIncrement += .05

class manageAccountPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.parent = parent

        header = Label(self, text = "Manage Account", font = headerFont)
        header.place(relx = .5, rely = .1, anchor = CENTER)

        self.logoutButton = Button(self, text = "Logout", font = buttonFont,
                              command = lambda : controller.showFrame(loginPage))
        self.logoutButton.config(width = 30)
        self.logoutButton.place(relx = .5, rely = .4, anchor = CENTER)

        self.curatorButton = Button(self, text = "Curator Request", font = buttonFont,
                               command = lambda : controller.showFrame(curatorRequestPage))
        self.curatorButton.config(width = 30)
        self.curatorButton.place(relx = .5, rely = .45, anchor = CENTER)

        # this doesn't actually delete the account because need sql to do it
        self.deleteButton = Button(self, text = "Delete Account", font = buttonFont,
                              command = self.deleteButton)
        self.deleteButton.config(width = 30)
        self.deleteButton.place(relx = .5, rely = .5, anchor = CENTER)

        self.backButton = Button(self, text="Back", font=buttonFont,
                            command=self.OnClick)
        self.backButton.config(width=30)
        self.backButton.place(relx=.01, rely=.8)


    def OnClick(self):
        global accountType
        if accountType == "curator":
            self.controller.showFrame(curatorAccountPage)
        elif accountType == "admin":
            self.controller.showFrame(adminAccountPage)
        else:
            self.controller.showFrame(accountPage)

    def deleteButton(self):

        global user
        toplevel = self.toplevel = tk.Toplevel(self)
        toplevel.geometry("%dx%d%+d%+d" % (500, 200, 0, 0))

        label1 = Label(toplevel, text="Are you sure?", height=0, width=50)
        label1.pack()
        label2 = Label(toplevel, text="Deleting your account will get rid of all your reviews,\nticket history, "
                                      "and credit card information.\nDo you still wish to continue?")
        label2.pack()

        B1 = Button(toplevel, text="Yes, delete account.", anchor=CENTER,
                    command= self.deleteAccount)
        B1.pack()
        B1.place(relx=.3, rely=.5, anchor=CENTER)

        B2 = Button(toplevel, text="No, do not delete account", anchor=CENTER,
                    command=toplevel.destroy)
        B2.pack()
        B2.place(relx=.7, rely=.5, anchor=CENTER)

    def deleteAccount(self):
        global user
        cursor.execute("DELETE FROM Visitor WHERE Email = %s", user)
        self.toplevel.destroy()
        self.controller.showFrame(loginPage)


class acceptCuratorRequestPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.parent = parent
        tk.Frame.__init__(self, parent)
        header = Label(self, text="Curator Requests", font=headerFont)
        header.place(relx=.5, rely=.1, anchor=CENTER)

        visitor = Label(self, text="Visitor", font=tableFont)
        visitor.place(relx=.2, rely=.3, anchor=CENTER)

        museum = Label(self, text="Museum", font=tableFont)
        museum.place(relx=.4, rely = .3, anchor = CENTER)

        approve = Label(self, text="Approve", font=tableFont)
        approve.place(relx=.6, rely=.3, anchor=CENTER)

        reject = Label(self, text="Reject", font=tableFont)
        reject.place(relx=.8, rely=.3, anchor=CENTER)

        self.backButton = Button(self, text="Back", font=buttonFont,
                                 command=lambda: controller.showFrame(adminAccountPage))
        self.backButton.config(width=30)
        self.backButton.place(relx=.01, rely=.85)

        self.requests = self.viewAllRequests()
        self.visitorNameList = []
        self.museumNameList = []
        self.approveButtonList = []
        self.rejectButtonList = []

        self.musIncrement = .4
        for self.requests in self.viewAllRequests():
            self.visitor = Label(self, text=self.requests[0], font=buttonFont)
            self.visitor.place(relx=.2, rely=self.musIncrement, anchor=CENTER)
            self.visitorNameList.append(self.visitor)

            self.museum = Label(self, text=self.requests[1], font=buttonFont)
            self.museum.place(relx=.4, rely=self.musIncrement, anchor=CENTER)
            self.museumNameList.append(self.museum)

            self.approveButton = Button(self, text="Approve", font=buttonFont,
                                        command=lambda ex=self.requests[0], mus=self.requests[1]: self.approveRequest(
                                            ex, mus))
            self.approveButton.config(width=25)
            self.approveButton.place(relx=.6, rely=self.musIncrement, anchor=CENTER)
            self.approveButtonList.append(self.approveButton)

            self.rejectButton = Button(self, text="Reject", font=buttonFont,
                                       command=lambda ex=self.requests[0], mus=self.requests[1]: self.rejectRequest(ex,
                                                                                                                    mus))
            self.rejectButton.config(width=25)
            self.rejectButton.place(relx=.8, rely=self.musIncrement, anchor=CENTER)
            self.rejectButtonList.append(self.rejectButton)
            self.musIncrement += .05


    def viewAllRequests(self):
        global user
        self.requests = []
        query = "SELECT VisitorEmail, MuseumName FROM CuratorRequest"
        cursor.execute(query)
        for request in cursor.fetchall():
            list = [request[0], request[1]]
            self.requests.append(list)
        return self.requests

    def update(self):
        for self.visitor in self.visitorNameList:
            self.visitor.destroy()
        for self.museum in self.museumNameList:
            self.museum.destroy()
        for self.approve in self.approveButtonList:
            self.approve.destroy()
        for self.reject in self.rejectButtonList:
            self.reject.destroy()

        self.requests = self.viewAllRequests()
        self.visitorNameList = []
        self.museumNameList = []
        self.approveButtonList = []
        self.rejectButtonList = []

        self.musIncrement = .4
        for self.requests in self.viewAllRequests():
            self.visitor = Label(self, text=self.requests[0], font=buttonFont)
            self.visitor.place(relx=.2, rely=self.musIncrement, anchor=CENTER)
            self.visitorNameList.append(self.visitor)

            self.museum = Label(self, text=self.requests[1], font=buttonFont)
            self.museum.place(relx=.4, rely=self.musIncrement, anchor=CENTER)
            self.museumNameList.append(self.museum)

            self.approveButton = Button(self, text="Approve", font=buttonFont,
                                       command=lambda ex=self.requests[0], mus =self.requests[1]: self.approveRequest(ex, mus))
            self.approveButton.config(width=25)
            self.approveButton.place(relx=.6, rely=self.musIncrement, anchor=CENTER)
            self.approveButtonList.append(self.approveButton)

            self.rejectButton = Button(self, text="Reject", font=buttonFont,
                                       command=lambda ex=self.requests[0], mus = self.requests[1]: self.rejectRequest(ex, mus))
            self.rejectButton.config(width=25)
            self.rejectButton.place(relx=.8, rely=self.musIncrement, anchor=CENTER)
            self.rejectButtonList.append(self.rejectButton)
            self.musIncrement += .05

    def approveRequest(self, email, museum):
        global user
        toplevel = Toplevel()
        query = "DELETE FROM CuratorRequest WHERE VisitorEmail <> %s AND MuseumName = %s"
        cursor.execute(query, (email, museum))
        query = "UPDATE Museum SET CuratorEmail = %s WHERE Name = %s"
        cursor.execute(query, (email, museum))
        query = "DELETE FROM CuratorRequest WHERE VisitorEmail = %s AND MuseumName = %s"
        cursor.execute(query, (email, museum))
        label1 = Label(toplevel, text="Success", height=0, width=50)
        label1.pack()
        self.controller.showFrame(acceptCuratorRequestPage)

    def rejectRequest(self, email, museum):
        toplevel = Toplevel()
        query = "DELETE FROM CuratorRequest WHERE VisitorEmail = %s"
        cursor.execute(query, (email))
        label1 = Label(toplevel, text = "Rejected", height = 0, width = 50)
        label1.pack()
        self.controller.showFrame(acceptCuratorRequestPage)


class curatorViewMuseumPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        # change header to name of museum
        self.header = Label(self, text= museumSelected, font=headerFont)
        self.header.place(relx=.5, rely=.1, anchor=CENTER)

        name = Label(self, text="Exhibit Name", font=tableFont)
        name.place(relx=.2, rely=.3, anchor=CENTER)

        year = Label(self, text="Year", font=tableFont)
        year.place(relx=.4, rely=.3, anchor=CENTER)

        url = Label(self, text="Link to Image/Information", font=tableFont)
        url.place(relx=.6, rely=.3, anchor=CENTER)

        musIncrement = .4
        self.parent = parent
        self.controller = controller

        self.listExhibits = self.viewAllExhibits()
        self.exhibitNameList = []
        self.yearList = []
        self.urlList = []
        self.removeButtonList = []

        self.purchaseTicketButton = Button(self, text="Purchase Ticket", font=buttonFont, command=self.purchaseTicket)
        self.purchaseTicketButton.config(width=35)
        self.purchaseTicketButton.place(relx=.5, rely=.75, anchor=CENTER)

        reviewMuseumButton = Button(self, text="Review Museum", font=buttonFont,
                                    command=lambda: controller.showFrame(reviewMuseumPage))
        reviewMuseumButton.config(width=35)
        reviewMuseumButton.place(relx=.5, rely=.8, anchor=CENTER)

        viewReviewsButton = Button(self, text="View All Reviews", font=buttonFont,
                                   command=lambda: controller.showFrame(allReviewsPage))
        viewReviewsButton.config(width=35)
        viewReviewsButton.place(relx=.5, rely=.85, anchor=CENTER)

        allMuseumsButton = Button(self, text="View all Museums", font=buttonFont,
                            command=lambda: controller.showFrame(allMuseumsPage))
        allMuseumsButton.config(width=30)
        allMuseumsButton.place(relx=.01, rely=.8)

        myAccountButton = Button(self, text="Return to Account Page", font=buttonFont,
                            command=self.OnClick)
        myAccountButton.config(width=30)
        myAccountButton.place(relx=.01, rely=.85)

        self.addExhibitButton = Button(self, text="Add Exhibit", font=buttonFont,
                                       command=lambda: controller.showFrame(addExhibitPage))
        self.addExhibitButton.place(relx = .5, rely = .9, anchor = CENTER)
        self.addExhibitButton.config(width=35)

    def removeExhibit(self, exhibitName):
        toplevel = Toplevel()
        query = "DELETE FROM Exhibit WHERE ExhibitName = %s"
        cursor.execute(query, (exhibitName))
        label1 = Label(toplevel, text="You have successfully removed the exhibit.", height=0, width=50)
        label1.pack()
        self.controller.showFrame(curatorViewMuseumPage)

    def OnClick(self):
        global accountType
        if accountType == "curator":
            self.controller.showFrame(curatorAccountPage)
        elif accountType == "admin":
            self.controller.showFrame(adminAccountPage)
        else:
            self.controller.showFrame(accountPage)

    def purchaseTicket(self):
        toplevel = Toplevel()
        query = "SELECT * FROM Ticket WHERE MuseumName = %s AND VisitorEmail = %s"
        cursor.execute(query, (museumSelected, user))
        if(cursor.rowcount == 0):
            query = "INSERT INTO Ticket(VisitorEmail, MuseumName, Price, PurchaseTimeStamp) VALUES(%s, %s, %s, %s)"
            cursor.execute(query, (user, museumSelected, 50, datetime.now()))
            label1 = Label(toplevel, text="Thank you for purchasing a ticket to Museum!", height=0, width=50)
            label1.pack()
            label2 = Label(toplevel, text="Check your email for your ticket!", height=0, width=50)
            label2.pack()
        else:
            label3 = Label(toplevel, text = "You have already purchased a ticket.", height = 0, width = 50)
            label3.pack()

    def viewAllExhibits(self):
        self.exhibits = []
        global museumSelected
        museumName = museumSelected
        cursor.execute("SELECT * FROM Exhibit WHERE MuseumName = %s", museumName)
        for row in cursor.fetchall():
            list = []
            list.append(row[1])
            list.append(row[2])
            list.append(row[3])
            self.exhibits.append(list)
        return self.exhibits


    def update(self):
        self.musIncrement = .4

        self.header.destroy()
        self.header = Label(self, text=museumSelected, font=headerFont)
        self.header.place(relx=.5, rely=.1, anchor=CENTER)

        for self.exhibit in self.exhibitNameList:
            self.exhibit.destroy()
        for self.year in self.yearList:
            self.year.destroy()
        for self.url in self.urlList:
            self.url.destroy()
        for self.button in self.removeButtonList:
            self.button.destroy()

        self.listExhibits = self.viewAllExhibits()
        self.exhibitNameList = []
        self.yearList = []
        self.urlList = []
        for self.exhibit in self.listExhibits:
            self.exhibitLabel = Label(self, text=self.exhibit[0], font=buttonFont)
            self.exhibitLabel.place(relx=.2, rely=self.musIncrement, anchor=CENTER)
            self.exhibitNameList.append(self.exhibitLabel)

            self.yearLabel = Label(self, text=self.exhibit[1], font=buttonFont)
            self.yearLabel.place(relx=.4, rely=self.musIncrement, anchor=CENTER)
            self.yearList.append(self.yearLabel)

            self.urlLabel = Label(self, text=self.exhibit[2], font=buttonFont)
            self.urlLabel.place(relx=.6, rely=self.musIncrement, anchor=CENTER)
            self.urlList.append(self.urlLabel)

            self.removeButton = Button(self, text="Remove Exhibit", font=buttonFont, command= lambda ex=self.exhibit[0]: self.removeExhibit(ex))
            self.removeButton.config(width = 30)
            self.removeButton.place(relx = .85, rely= self.musIncrement, anchor = CENTER)
            self.removeButtonList.append(self.removeButton)
            self.musIncrement += .05


        #have to check if they have already purchsed
        #check what museum too




class addExhibitPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        global museumSelected
        self.parent = parent
        self.controller = controller

        # header
        self.header = Label(self, text = "Add Exhibit", font = headerFont)
        self.header.place(relx = .5, rely = .1, anchor = CENTER)

        # label for exhibit name
        self.nameLabel = Label(self, text = "Exhibit Name: ", font = buttonFont)
        self.nameLabel.place(relx = .25, rely = .4, anchor = CENTER)

        # label for exhibit year
        self.yearLabel = Label(self, text = "Year: ", font = buttonFont)
        self.yearLabel.place(relx = .25, rely = .5)

        # label for exhibit url
        self.urlLabel = Label(self, text = "URL: ", font = buttonFont)
        self.urlLabel.place(relx = .25, rely = .6, anchor = CENTER)

        # entry fields
        self.nameEntry = Entry(self)
        self.yearEntry = Entry(self)
        self.URLEntry = Entry(self)

        # exhibit name entry box
        self.nameEntry.config(width = 10)
        self.nameEntry.place(relx = .3, rely = .4)

        # exhibit year entry box
        self.yearEntry.config(width = 10)
        self.yearEntry.place(relx = .3, rely = .5)

        # exhibit url input box
        self.URLEntry.config(width = 10)
        self.URLEntry.place(relx = .3, rely = .6)

        # submit button that should call method to add exhibit to db
        self.submitButton = Button(self, text = "Submit Exhibit", font = buttonFont,
            command = self.addThatExhibit)
        self.submitButton.config(width = 50)
        self.submitButton.place(relx = .5, rely = .8, anchor = CENTER)

        # back button to cancel adding
        self.backButton = Button(self, text = "Back", font = buttonFont,
            command = lambda: controller.showFrame(curatorViewMuseumPage))
        self.backButton.config(width = 50)
        self.backButton.place(relx = .5, rely = .9, anchor = CENTER)

    def addThatExhibit(self):
        toplevel = Toplevel()
        eName = self.nameEntry.get()
        eYear = self.yearEntry.get()
        eURL = self.URLEntry.get()

        query = "SELECT * FROM Exhibit WHERE ExhibitName = %s"
        cursor.execute(query, eName)
        if cursor.rowcount == 1:
            label1 = Label(toplevel, text = "An exhibit with this name already exists.",
                height = 0, width = 60)
            label1.pack()
        else:
            query = "INSERT INTO Exhibit(MuseumName, ExhibitName, Year, URL) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (museumSelected, eName, eYear, eURL))
            label2 = Label(toplevel, text = "Exhibit Added.", height = 0, width = 50)
            label2.pack()
            self.controller.showFrame(curatorViewMuseumPage)

class curatorRequestPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        header = Label(self, text="Curator Request", font=headerFont)
        header.place(relx=.5, rely=.1, anchor=CENTER)

        self.controller = controller
        self.parent = parent

        name = Label(self, text="Which museum would you like to curate?", font=tableFont)
        name.place(relx=.3, rely=.3, anchor=CENTER)

        curator = Label(self, text="Curator Name", font=tableFont)
        curator.place(relx=.7, rely=.3, anchor=CENTER)

        self.musIncrement = .4
        self.listmus = self.viewAllMuseums()
        self.buttonList = []
        self.labelList = []

        for museum in self.listmus:
            self.museumButton = Button(self, text=museum[0], font=buttonFont,
                                       command=lambda text=museum[0]: self.OnClick(text))
            self.museumButton.config(width=60)
            self.museumButton.place(relx=.3, rely=self.musIncrement, anchor=CENTER)
            self.buttonList.append(self.museumButton)

            self.curatorLabel = Label(self, text=museum[1], font=buttonFont)
            self.curatorLabel.place(relx=.7, rely=self.musIncrement, anchor=CENTER)
            self.labelList.append(self.curatorLabel)

            self.musIncrement += .05

        self.backButton = Button(self, text="Back", font=buttonFont,
                            command=lambda: controller.showFrame(manageAccountPage))
        self.backButton.config(width=30)
        self.backButton.place(relx=.01, rely=.85)

    def viewAllMuseums(self):
        self.museums = []
        query = "SELECT Name, CuratorEmail FROM Museum"
        cursor.execute(query)
        for row in cursor.fetchall():
            list = []
            list.append(row[0])
            list.append(row[1])
            self.museums.append(list)
        return self.museums

    def OnClick(self, text):
        global user
        global museumSelected
        museumSelected = text
        print(user)
        print(museumSelected)
        toplevel = Toplevel()
        query = "SELECT CuratorEmail FROM Museum WHERE Name = %s"
        cursor.execute(query, (museumSelected))
        for row in cursor.fetchall():
            if row[0] is None:
                cursor.execute("SELECT * FROM CuratorRequest WHERE VisitorEmail = %s AND MuseumName = %s",
                               (user, museumSelected))
                if (cursor.rowcount == 0):
                    cursor.execute("INSERT INTO CuratorRequest(VisitorEmail, MuseumName) VALUES(%s, %s)",
                                   (user, museumSelected))
                    label2 = Label(toplevel, text="Your request has been submitted!", height=0, width=50)
                    label2.pack()
                else:
                    label3 = Label(toplevel, text="You have already submitted a curator request for this museum.",
                                   height=0, width=50)
                    label3.pack()
            else:
                label1 = Label(toplevel, text="Sorry, this museum already has a curator.", height=0, width=50)
                label1.pack()

    def update(self):
        self.musIncrement = .4

        for self.label in self.labelList:
            self.label.destroy()
        for self.button in self.buttonList:
            self.button.destroy()

        self.listmus = self.viewAllMuseums()
        self.buttonList = []
        self.labelList = []
        for museum in self.listmus:
            self.museumButton = Button(self, text=museum[0], font=buttonFont,
                                       command=lambda text=museum[0]: self.OnClick(text))
            self.museumButton.config(width=60)
            self.museumButton.place(relx=.3, rely=self.musIncrement, anchor=CENTER)
            self.buttonList.append(self.museumButton)

            self.curatorLabel = Label(self, text=museum[1], font=buttonFont)
            self.curatorLabel.place(relx=.7, rely=self.musIncrement, anchor=CENTER)
            self.labelList.append(self.curatorLabel)

            self.musIncrement += .05


class allMuseumsPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        header = Label(self, text = "All Museums", font = headerFont)
        header.place(relx = .5, rely = .1, anchor = CENTER)

        self.controller = controller
        self.parent = parent
        name = Label(self, text = "Museum Name", font = tableFont)
        name.place(relx = .3, rely = .3, anchor = CENTER)

        rating = Label(self, text = "Average Rating", font = tableFont)
        rating.place(relx = .7, rely = .3, anchor = CENTER)

        self.musIncrement = .4
        self.listmus = self.viewAllMuseums()
        self.labelList = []
        self.buttonList = []

        for museum in self.listmus:
            self.museumButton = Button(self, text=museum[0], font=buttonFont, command = lambda text=museum[0]: self.OnClick(text))
            self.museumButton.config(width=60)
            self.museumButton.place(relx=.3, rely=self.musIncrement, anchor=CENTER)
            self.buttonList.append(self.museumButton)

            self.ratingLabel = Label(self, text=museum[1], font=buttonFont)
            self.ratingLabel.place(relx=.7, rely=self.musIncrement, anchor=CENTER)
            self.musIncrement += .05
            self.labelList.append(self.ratingLabel)

        self.backButton = Button(self, text="Back", font=buttonFont,
                            command=self.backToAccount)
        self.backButton.config(width=30)
        self.backButton.place(relx=.01, rely=.85)

    def viewAllMuseums(self):
        self.museums = []
        query = "SELECT Name, AvgRating FROM Museum"
        cursor.execute(query)
        for row in cursor.fetchall():
            name = row[0]
            rate = "SELECT AVG(Rating) FROM Review WHERE MuseumName = %s"
            cursor.execute(rate, (name))
            list = []
            list.append(row[0])
            for rate in cursor.fetchone():
                list.append(rate)
            self.museums.append(list)
        return self.museums

    def OnClick(self, text):
        global museumSelected
        museumSelected = text
        self.controller.showFrame(viewMuseumPage)

    def backToAccount(self):
        global accountType
        if accountType == "curator":
            self.controller.showFrame(curatorAccountPage)
        elif accountType == "admin":
            self.controller.showFrame(adminAccountPage)
        else:
            self.controller.showFrame(accountPage)


    def update(self):
        self.musIncrement = .4
        for self.label in self.labelList:
            self.label.destroy()
        for self.button in self.buttonList:
            self.button.destroy()

        self.listmus = self.viewAllMuseums()
        self.labelList = []
        self.buttonList = []
        for museum in self.listmus:
            self.museumButton = Button(self, text=museum[0], font=buttonFont, command = lambda text=museum[0]: self.OnClick(text))
            self.museumButton.config(width=60)
            self.museumButton.place(relx=.3, rely=self.musIncrement, anchor=CENTER)
            self.buttonList.append(self.museumButton)

            self.ratingLabel = Label(self, text=museum[1], font=buttonFont)
            self.ratingLabel.place(relx=.7, rely=self.musIncrement, anchor=CENTER)
            self.musIncrement += .05
            self.labelList.append(self.ratingLabel)


class viewMuseumPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        # change header to name of museum
        self.header = Label(self, text= museumSelected, font=headerFont)
        self.header.place(relx=.5, rely=.1, anchor=CENTER)

        name = Label(self, text="Exhibit Name", font=tableFont)
        name.place(relx=.3, rely=.3, anchor=CENTER)

        year = Label(self, text="Year", font=tableFont)
        year.place(relx=.5, rely=.3, anchor=CENTER)

        url = Label(self, text="Link to Image/Information", font=tableFont)
        url.place(relx=.7, rely=.3, anchor=CENTER)

        musIncrement = .4
        self.parent = parent
        self.controller = controller

        self.listExhibits = self.viewAllExhibits()
        self.exhibitNameList = []
        self.yearList = []
        self.urlList = []
        for self.exhibit in self.listExhibits:
            self.exhibitLabel = Label(self, text=self.exhibit[0], font=buttonFont)
            self.exhibitLabel.place(relx=.3, rely=musIncrement, anchor=CENTER)
            self.exhibitNameList.append(self.exhibitLabel)

            self.yearLabel = Label(self, text=self.exhibit[1], font=buttonFont)
            self.yearLabel.place(relx=.5, rely=musIncrement, anchor=CENTER)
            self.yearList.append(self.yearLabel)

            self.urlLabel = Label(self, text=self.exhibit[0], font=buttonFont)
            self.urlLabel.place(relx=.7, rely=musIncrement, anchor=CENTER)
            self.urlList.append(self.urlLabel)

            musIncrement += .05


        self.purchaseTicketButton = Button(self, text="Purchase Ticket", font=buttonFont, command=self.purchaseTicket)
        self.purchaseTicketButton.config(width=35)
        self.purchaseTicketButton.place(relx=.5, rely=.75, anchor=CENTER)

        reviewMuseumButton = Button(self, text="Review Museum", font=buttonFont,
                                    command=lambda: controller.showFrame(reviewMuseumPage))
        reviewMuseumButton.config(width=35)
        reviewMuseumButton.place(relx=.5, rely=.8, anchor=CENTER)

        viewReviewsButton = Button(self, text="View All Reviews", font=buttonFont,
                                   command=lambda: controller.showFrame(allReviewsPage))
        viewReviewsButton.config(width=35)
        viewReviewsButton.place(relx=.5, rely=.85, anchor=CENTER)

        allMuseumsButton = Button(self, text="View all Museums", font=buttonFont,
                            command=lambda: controller.showFrame(allMuseumsPage))
        allMuseumsButton.config(width=30)
        allMuseumsButton.place(relx=.01, rely=.8)

        myAccountButton = Button(self, text="Return to Account Page", font=buttonFont,
                            command=self.OnClick)
        myAccountButton.config(width=30)
        myAccountButton.place(relx=.01, rely=.85)

    def OnClick(self):
        global accountType
        if accountType == "curator":
            self.controller.showFrame(curatorAccountPage)
        elif accountType == "admin":
            self.controller.showFrame(adminAccountPage)
        else:
            self.controller.showFrame(accountPage)

    def purchaseTicket(self):
        toplevel = Toplevel()
        query = "SELECT * FROM Ticket WHERE MuseumName = %s AND VisitorEmail = %s"
        cursor.execute(query, (museumSelected, user))
        if(cursor.rowcount == 0):
            query = "INSERT INTO Ticket(VisitorEmail, MuseumName, Price, PurchaseTimeStamp) VALUES(%s, %s, %s, %s)"
            cursor.execute(query, (user, museumSelected, 50, datetime.now()))
            label1 = Label(toplevel, text="Thank you for purchasing a ticket to Museum!", height=0, width=50)
            label1.pack()
            label2 = Label(toplevel, text="Check your email for your ticket!", height=0, width=50)
            label2.pack()
        else:
            label3 = Label(toplevel, text = "You have already purchased a ticket.", height = 0, width = 50)
            label3.pack()

    def viewAllExhibits(self):
        self.exhibits = []
        global museumSelected
        museumName = museumSelected
        cursor.execute("SELECT * FROM Exhibit WHERE MuseumName = %s", museumName)
        for row in cursor.fetchall():
            list = []
            list.append(row[1])
            list.append(row[2])
            list.append(row[3])
            self.exhibits.append(list)
        return self.exhibits


    def update(self):
        self.musIncrement = .4

        self.header.destroy()
        self.header = Label(self, text=museumSelected, font=headerFont)
        self.header.place(relx=.5, rely=.1, anchor=CENTER)

        for self.exhibit in self.exhibitNameList:
            self.exhibit.destroy()
        for self.year in self.yearList:
            self.year.destroy()
        for self.url in self.urlList:
            self.url.destroy()

        self.listExhibits = self.viewAllExhibits()
        self.exhibitNameList = []
        self.yearList = []
        self.urlList = []
        for self.exhibit in self.listExhibits:
            self.exhibitLabel = Label(self, text=self.exhibit[0], font=buttonFont)
            self.exhibitLabel.place(relx=.3, rely=self.musIncrement, anchor=CENTER)
            self.exhibitNameList.append(self.exhibitLabel)

            self.yearLabel = Label(self, text=self.exhibit[1], font=buttonFont)
            self.yearLabel.place(relx=.5, rely=self.musIncrement, anchor=CENTER)
            self.yearList.append(self.yearLabel)

            self.urlLabel = Label(self, text=self.exhibit[2], font=buttonFont)
            self.urlLabel.place(relx=.7, rely=self.musIncrement, anchor=CENTER)
            self.urlList.append(self.urlLabel)

            self.musIncrement += .05


        #have to check if they have already purchsed
        #check what museum too

class reviewMuseumPage(tk.Frame):

    def __init__(self, parent, controller):
        global museumSelected
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self,parent)
        self.header = Label(self, text=museumSelected, font=headerFont)
        self.header.place(relx=.5, rely=.1, anchor=CENTER)

        self.ratingLabel = Label(self, text="Rating: ", font=buttonFont)
        self.ratingLabel.place(relx=.2, rely=.5, anchor=CENTER)
        self.rate = StringVar()
        self.entryRating = Entry(self, textvariable=self.rate)
        self.entryRating.place()

        self.entryRating.place(relx=.45, rely=.5, anchor=CENTER)
        self.entryRating.config(width=50)

        self.commentLabel = Label(self, text="Comment: ", font=buttonFont)
        self.commentLabel.place(relx=.2, rely=.7, anchor=CENTER)
        self.comment = StringVar()
        self.entryComment = Entry(self, textvariable=self.comment)
        self.entryComment.place()

        self.entryComment.place(relx=.45, rely=.7, anchor=CENTER)
        self.entryComment.config(width=50)

        submitButton = Button(self, text = "Submit", font = buttonFont, command = lambda: self.makeReview())
        submitButton.config(width = 30)
        submitButton.place(relx = .7, rely = .8)

        self.backButton = Button(self, text="Back", font=buttonFont,
                            command=lambda: controller.showFrame(viewMuseumPage))
        self.backButton.config(width=30)
        self.backButton.place(relx=.01, rely=.85)

    def makeReview(self):
        toplevel = Toplevel()
        global museumSelected
        global user
        if self.entryRating.get() <= 5 and self.entryRating.get() > 0:
            query = "SELECT * FROM Ticket WHERE VisitorEmail = %s AND MuseumName = %s"
            cursor.execute(query, (user, museumSelected))
            if (cursor.rowcount == 1):
                query = "SELECT * FROM Review WHERE VisitorEmail = %s and MuseumName = %s"
                cursor.execute(query, (user, museumSelected))
                if cursor.rowcount == 1:
                    update = "UPDATE Review SET Comment = %s, Rating = %s WHERE MuseumName = %s AND VisitorEmail = %s"
                    cursor.execute(update, (self.entryComment.get(), self.entryRating.get(), museumSelected, user))
                    label1 = Label(toplevel, text = "Thank you for updating your comment.", height = 0, width = 50)
                    label1.pack()
                else:
                    insert = "INSERT INTO Review(VisitorEmail, MuseumName, Comment, Rating) VALUES (%s, %s, %s, %s)"
                    cursor.execute(insert, (user, museumSelected, self.comment.get(), self.entryRating.get()))
                    label3 = Label(toplevel, text = "Thank you for your review.", height = 0, width = 50)
                    label3.pack()
            else:
                label4 = Label(toplevel, text = "You can't write a review for a museum you haven't been to.", height = 0, width= 50)
                label4.pack()
                self.controller.showFrame(reviewMuseumPage)
        else:
            label1 = Label(toplevel, text="Ratings must be between 0 and 5.", height=0, width=50)
            label1.pack()


    def update(self):
        global museumSelected
        self.header.destroy()
        self.header = Label(self, text=museumSelected, font=headerFont)
        self.header.place(relx=.5, rely=.1, anchor=CENTER)
        self.entryRating.destroy()
        self.rate = StringVar()
        self.entryRating = Entry(self, textvariable=self.rate)
        self.entryRating.place()

        self.entryRating.place(relx=.45, rely=.5, anchor=CENTER)
        self.entryRating.config(width=50)

        self.entryComment.destroy()
        self.comment = StringVar()
        self.entryComment = Entry(self, textvariable=self.comment)
        self.entryComment.place()

        self.entryComment.place(relx=.45, rely=.7, anchor=CENTER)
        self.entryComment.config(width=50)


class allReviewsPage(tk.Frame):

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, parent)
        header = Label(self, text = "All Reviews", font = headerFont)
        header.place(relx = .5, rely = .1, anchor = CENTER)

        reviewCol = Label(self, text = "Review", font = tableFont)
        reviewCol.place(relx = .3, rely = .3, anchor = CENTER)

        ratingCol = Label(self, text = "Rating", font = tableFont)
        ratingCol.place(relx = .7, rely = .3, anchor = CENTER)

        self.reviews = self.getReviews()
        self.reviewList = []
        self.ratingList = []
        self.ticIncrement = .4
        for r in self.reviews:
            self.reviewLabel = Label(self, text= r[0], font=buttonFont)
            self.reviewLabel.place(relx=.3, rely=self.ticIncrement, anchor=CENTER)
            self.reviewList.append(self.reviewList)

            self.ratingLabel = Label(self, text=r[1], font=buttonFont)
            self.ratingLabel.place(relx=.7, rely=self.ticIncrement, anchor=CENTER)
            self.ratingList.append(self.ratingLabel)
            self.ticIncrement += .05

        self.backButton = Button(self, text="Back", font=buttonFont,
                            command=lambda: controller.showFrame(viewMuseumPage))
        self.backButton.config(width=30)
        self.backButton.place(relx=.01, rely=.85)

    def getReviews(self):
        self.reviewList = []
        query = "SELECT Comment, Rating FROM Review WHERE MuseumName = %s"
        cursor.execute(query, museumSelected)
        for mus in cursor.fetchall():
            list = [mus[0], mus[1]]
            self.reviewList.append(list)
        return self.reviewList

    def update(self):
        for self.review in self.reviewList:
            self.review.destroy()
        for self.rate in self.ratingList:
            self.rate.destroy()

        self.reviews = self.getReviews()
        ticIncrement = .4

        self.reviewList = []
        self.ratingList = []

        for t in self.reviews:
            self.reviewLabel = Label(self, text=t[0], font=buttonFont)
            self.reviewLabel.place(relx=.2, rely=ticIncrement, anchor=CENTER)
            self.reviewList.append(self.reviewLabel)

            self.ratingLabel = Label(self, text=t[1], font=buttonFont)
            self.ratingLabel.place(relx=.5, rely=ticIncrement, anchor=CENTER)
            self.ratingList.append(self.ratingLabel)
            ticIncrement += .05


class myTicketsPage(tk.Frame):

    def __init__(self, parent, controller):

        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, parent)
        header = Label(self, text = "My Tickets", font = headerFont)
        header.place(relx = .5, rely = .1, anchor = CENTER)

        musName = Label(self, text = "Museum Name", font = tableFont)
        musName.place(relx = .2, rely = .3, anchor = CENTER)

        purchaseDate = Label(self, text = "Cost of Purchase", font = tableFont)
        purchaseDate.place(relx = .5, rely = .3, anchor = CENTER)

        money = Label(self, text = "Purchase Date", font = tableFont)
        money.place(relx = .8, rely = .3, anchor = CENTER)

        self.backButton = Button(self, text="Back", font=buttonFont,
                            command=self.OnClick)
        self.backButton.config(width=30)
        self.backButton.place(relx=.01, rely=.85)
        self.tickets = self.myTix()
        ticIncrement = .4

        self.ticketsList = []
        self.labelList = []
        self.moneyList = []

        for t in self.tickets:
            self.nameLabel = Label(self, text=t[0], font=buttonFont)
            self.nameLabel.place(relx=.2, rely=ticIncrement, anchor=CENTER)
            self.ticketsList.append(self.nameLabel)

            self.purLabel = Label(self, text=t[1], font=buttonFont)
            self.purLabel.place(relx=.5, rely=ticIncrement, anchor=CENTER)
            self.labelList.append(self.purLabel)

            self.moneyLabel = Label(self, text=t[2], font=buttonFont)
            self.moneyLabel.place(relx=.8, rely=ticIncrement, anchor=CENTER)
            ticIncrement += .05
            self.moneyList.append(self.moneyLabel)

    def OnClick(self):
        if accountType == "curator":
            self.controller.showFrame(curatorAccountPage)
        elif accountType == "admin":
            self.controller.showFrame(adminAccountPage)
        else:
            self.controller.showFrame(accountPage)

    def myTix(self):
        self.tickets = []
        email = str(user)
        query = "SELECT MuseumName, Price, PurchaseTimeStamp FROM Ticket WHERE VisitorEmail = '" + email + "'"
        cursor.execute(query)
        for row in cursor.fetchall():
            list = []
            list.append(row[0])
            list.append(row[1])
            list.append(row[2])
            self.tickets.append(list)
        return self.tickets

    def update(self):
        for self.ticket in self.ticketsList:
            self.ticket.destroy()
        for self.label in self.labelList:
            self.label.destroy()
        for self.money in self.moneyList:
            self.money.destroy()

        self.tickets = self.myTix()
        ticIncrement = .4

        self.ticketsList = []
        self.labelList = []
        self.moneyList = []

        for t in self.tickets:
            self.nameLabel = Label(self, text=t[0], font=buttonFont)
            self.nameLabel.place(relx=.2, rely=ticIncrement, anchor=CENTER)
            self.ticketsList.append(self.nameLabel)

            self.purLabel = Label(self, text=t[1], font=buttonFont)
            self.purLabel.place(relx=.5, rely=ticIncrement, anchor=CENTER)
            self.labelList.append(self.purLabel)

            self.moneyLabel = Label(self, text=t[2], font=buttonFont)
            self.moneyLabel.place(relx=.8, rely=ticIncrement, anchor=CENTER)
            self.moneyList.append(self.moneyLabel)
            ticIncrement += .05


class myReviewsPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.parent = parent

        header = Label(self, text = "My Reviews", font = headerFont)
        header.place(relx = .5, rely = .1, anchor = CENTER)

        musName = Label(self, text = "Museum Name", font = tableFont)
        musName.place(relx = .2, rely = .3, anchor = CENTER)

        reviewLabel = Label(self, text = "Review", font = tableFont)
        reviewLabel.place(relx = .5, rely = .3, anchor = CENTER)

        ratingLabel = Label(self, text = "Rating", font = tableFont)
        ratingLabel.place(relx = .8, rely = .3, anchor = CENTER)

        tableHeight = 5
        self.tableIncrement = .4

        self.reviews = self.reviewHistory()
        self.namesList = []
        self.commentList = []
        self.ratingList = []

        for i in self.reviews:
            self.nameLabel = Label(self, text = i[0], font = buttonFont,
                              wraplength = 125, justify = CENTER)
            self.nameLabel.place(relx = .2, rely = self.tableIncrement, anchor = CENTER)
            self.namesList.append(self.nameLabel)

            self.reviewLabel = Label(self, text = i[1],
                                font = buttonFont,
                                wraplength = 500, justify = CENTER)
            self.reviewLabel.place(relx=.5, rely= self.tableIncrement, anchor=CENTER)
            self.commentList.append(self.reviewLabel)

            self.ratingLabel = Label(self, text=i[2], font = buttonFont)
            self.ratingLabel.place(relx = .8, rely = self.tableIncrement, anchor = CENTER)
            self.tableIncrement += .1
            self.ratingList.append(self.ratingLabel)

        self.backButton = Button(self, text = "Back", font = buttonFont,
                            command=self.OnClick)
        self.backButton.config(width=30)
        self.backButton.place(relx=.01, rely=.85)

    def OnClick(self):
        if accountType == "curator":
            self.controller.showFrame(curatorAccountPage)
        elif accountType == "admin":
            self.controller.showFrame(adminAccountPage)
        else:
            self.controller.showFrame(accountPage)

    def reviewHistory(self):
        email = str(user)
        query = "SELECT MuseumName, Comment, Rating FROM Review WHERE VisitorEmail = '" + email + "'"
        cursor.execute(query)
        self.reviews = []
        for row in cursor.fetchall():
            each = []
            each.append(row[0])
            each.append(row[1])
            each.append(row[2])
            self.reviews.append(each)
        return self.reviews

    def update(self):
        self.tableIncrement = .4
        for self.name in self.namesList:
            self.name.destroy()
        for self.comment in self.commentList:
            self.comment.destroy()
        for self.rating in self.ratingList:
            self.rating.destroy()

        self.reviews = self.reviewHistory()
        self.namesList = []
        self.commentList = []
        self.ratingList = []

        self.tableIncrement = .4

        for i in self.reviews:
            self.nameLabel = Label(self, text=i[0], font=buttonFont,
                                   wraplength=125, justify=CENTER)
            self.nameLabel.place(relx=.2, rely= self.tableIncrement, anchor=CENTER)
            self.namesList.append(self.nameLabel)

            self.reviewLabel = Label(self, text=i[1],
                                     font=buttonFont,
                                     wraplength=500, justify=CENTER)
            self.reviewLabel.place(relx=.5, rely= self.tableIncrement, anchor=CENTER)
            self.commentList.append(self.reviewLabel)

            self.ratingLabel = Label(self, text=i[2], font=buttonFont)
            self.ratingLabel.place(relx=.8, rely= self.tableIncrement, anchor=CENTER)
            self.tableIncrement += .1
            self.ratingList.append(self.ratingLabel)

app = museumApp()
app.mainloop()