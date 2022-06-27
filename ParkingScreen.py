import time
import tkinter
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from tkinter import messagebox
import ParkingLot as pl
from main import *


# Class to create and handle all GUI elements in project
class ParkingScreen:

    def __init__(self, win):
        # Window
        self.win = win
        self.subWin = None
        self.visitorWin = None
        self.btn_subscribe = None
        self.btn_visitor = None
        self.pl = pl.ParkingLot()
        self.ps = None
        self.curLicensePlate = None
        self.btn_proceed_payment = None
        self.subscribed = False
        self.paymentWin = None
        self.subscribing = False

        self.var1 = None
        self.var2 = None
        self.var3 = None
        self.var4 = None
        self.var5 = None
        self.cbtn1 = None
        self.cbtn2 = None

        # Labels
        self.lbl_welcome = tkinter.Label(win, text="Welcome to our Modern Parking Lot", font=("Terminal", 22), bg='white', fg='blue')
        self.lbl_welcome.place(x=50, y=50)
        self.lbl_enterInfo = tkinter.Label(win, text="Please enter your vehicle's license plate:", font=("Terminal", 17), bg='white', fg='blue')
        self.lbl_enterInfo.place(x=100, y=100)
        # image
        self.image = Image.open('icon.jpg')
        self.image.thumbnail((240, 240), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.label_image = Label(image=self.photo)
        self.label_image.place(x=173, y=240)

        # Entry Field
        self.licensePlateInput = Entry(win, width=40)
        self.licensePlateInput.focus_set()
        self.licensePlateInput.pack()
        self.licensePlateInput.place(x=173, y=150)

        # After entering license plate - user should click Next
        self.btn_next = tkinter.Button(win, text="Next", font=("Terminal", 15), bg='white', fg='blue', command=self.validateInput)
        self.btn_next.place(x=265, y=200)

    def welcome_window(self):
        self.lbl_welcome = tkinter.Label(self.win, text="Welcome to our Modern Parking Lot", font=("Terminal", 22),
                                         bg='white', fg='blue')
        self.lbl_welcome.place(x=50, y=50)
        self.lbl_enterInfo = tkinter.Label(self.win, text="Please enter your vehicle's license plate:",
                                           font=("Terminal", 17), bg='white', fg='blue')
        self.lbl_enterInfo.place(x=100, y=100)
        # image
        self.image = Image.open('icon.jpg')
        self.image.thumbnail((240, 240), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.label_image = Label(image=self.photo)
        self.label_image.place(x=173, y=240)

        # Entry Field
        self.licensePlateInput = Entry(self.win, width=40)
        self.licensePlateInput.focus_set()
        self.licensePlateInput.pack()
        self.licensePlateInput.place(x=173, y=150)

        # After entering license plate - user should click Next
        self.btn_next = tkinter.Button(self.win, text="Next", font=("Terminal", 15), bg='white', fg='blue',
                                       command= lambda: self.validateInput())
        self.btn_next.place(x=265, y=200)

    # Function for checking user input (of his vehicles license plate)
    def validateInput(self):
        if len(self.getLicensePlate()) != 7 and len(self.getLicensePlate()) != 8:
            # show the error message
            messagebox.showerror("Invalid Input", "Uh-Oh looks like that cannot be your license plate!")
            self.clearField(self.licensePlateInput)
        else:
            self.clearFrame(self.win)
            self.win.title("Modern Parking")
            tkinter.Label(self.win, text="Car License Number: " + self.curLicensePlate, font=("Terminal", 17), bg='white', fg='blue').pack(pady=20)
            tkinter.Label(self.win, text="Are you entering the Parking or Leaving?", font=("Terminal", 17), bg='white', fg='blue').pack(pady=20)
            btn_enter = tkinter.Button(self.win, text="Enter Parking", font=("Terminal", 17), bg='white', fg='blue', command=self.enterParking).pack(pady=20)
            btn_leave = tkinter.Button(self.win, text="Exit Parking", font=("Terminal", 17), bg='white', fg='blue', command=self.checkTicket).pack(pady=20)

    def checkIfParked(self):
        for lp in self.pl.activeTickets:
            if lp.getLicensePlate() == self.curLicensePlate:
                tkinter.messagebox.showinfo("Plate already Parked", "Please exit the parking lot first")
                return True
        return False

    # Get license Plate entered by user as string
    def getLicensePlate(self):
        licensePlate = Entry.get(self.licensePlateInput)
        self.curLicensePlate = str(licensePlate)
        return self.curLicensePlate

    def enterParking(self):
        if not self.checkIfParked():
            activeSub = self.pl.checkActiveSubscriber(self.curLicensePlate)
            if activeSub:
                self.subscribed = True
                self.subscribing = False
                self.createSubscribedWindow(activeSub)
            else:
                self.subscribed = False
                self.subscribing = False
                self.createVisitorWindow()

    def checkTicket(self):
        if self.pl.checkActiveTicket(self.curLicensePlate):
            ticket = self.getTicketDetails()
            for p in self.pl.allParkingSpots:
                if p.getParkingId() == ticket.getParkingId():
                    if not ticket.getSubscribed():
                        self.createPaymentWindow(ticket.calcTotalCost(p), p, ticket)
                    else:
                        self.leaveParkingLot(p, ticket)
                    break
        else:
            # show the error message
            messagebox.showerror("Invalid Input", "Uh-Oh! no ticket found for this vehicle, please contact technical team for assistance")

    def leaveParkingLot(self, p, ticket):
        p.setOccupied(False)
        self.pl.activeTickets.remove(ticket)
        tkinter.messagebox.showinfo("Bye bye", "Drive Safely")
        self.homeBtn()

    def getTicketDetails(self):
        for t in self.pl.activeTickets:
            if self.curLicensePlate == t.getLicensePlate():
                return t

    # Create a new GUI window for subscribed customers
    def createSubscribedWindow(self, activeSub):
        self.ps = self.pl.findAvailableSpot(activeSub.getVehicaleType(), activeSub.getElectric(),
                                            activeSub.getHandicapped(), self.curLicensePlate)
        self.subWin = Toplevel(self.win)
        self.subWin.resizable(False, False)
        self.subWin.geometry("630x500")
        self.subWin.title("Subscribed Modern Parking Member")
        self.recognizeSubscribe()

    def recognizeSubscribe(self):
        if self.ps != 0:
            self.subscribed = True
            self.createTicket()
            if self.subscribing:
                Label(self.paymentWin, text="Great! You are subscribed", font=("Terminal", 22)).pack(pady=30)
                Label(self.paymentWin, text="Please proceed to parking spot: " + str(self.ps), font=("Terminal", 17)).pack(
                    pady=30)
                tkinter.Button(self.paymentWin, text="Home", font=("Terminal", 17), command=self.homeBtn).pack()
            else:
                Label(self.subWin, text="Great! You are subscribed", font=("Terminal", 22)).pack(pady=30)
                Label(self.subWin, text="Please proceed to parking spot: " + str(self.ps), font=("Terminal", 17)).pack(pady=30)
                tkinter.Button(self.subWin, text="Home", font=("Terminal", 17), command=self.homeBtn).pack()
        else:
            Label(self.subWin, text="We are sorry, there are no available spots.", font=("Terminal", 17)).pack(
                pady=30)

    def createTicket(self):
        newTicket = ParkingTicket(self.curLicensePlate, self.subscribed, self.ps)
        self.pl.activeTickets.append(newTicket)

    # Create a new GUI window for visitors or new subscribers
    def createVisitorWindow(self):
        self.visitorWin = Toplevel(self.win)
        self.visitorWin.resizable(False, False)
        self.visitorWin.geometry("630x500")
        self.visitorWin.title("Visitor at Modern Parking")
        self.btn_subscribe = tkinter.Button(self.visitorWin, text="I want to Subscribe!", font=("Terminal", 19),
                                            command=self.createSignUpWindow).pack(pady=30)
        self.btn_visitor = tkinter.Button(self.visitorWin, text="This is a one time thing...",
                                          font=("Terminal", 19), command=self.createOneTimeWindow).pack(pady=30)

    def createVehicleTypeRB(self):
        Label(self.visitorWin, text="Select vehicle type:", font=("Terminal", 17)).pack(pady=30)
        self.var2 = StringVar()
        rbtn_V1 = Radiobutton(self.visitorWin, text="Private Car", variable=self.var2, value='PRIVATE', command= lambda:[self.chooseSpecialParking(), self.checkAvailablity(special)])
        rbtn_V1.pack(anchor=CENTER)
        rbtn_V2 = Radiobutton(self.visitorWin, text="Large(Bus, Truck)", variable=self.var2, value='LARGE', command= lambda: [self.clearSpecialParking(), self.checkAvailablity(special)])
        rbtn_V2.pack(anchor=CENTER)
        rbtn_V3 = Radiobutton(self.visitorWin, text="Motorcycle", variable=self.var2, value='MOTORCYCLE', command= lambda: [self.clearSpecialParking(), self.checkAvailablity(special)])
        rbtn_V3.pack(anchor=CENTER)
        if self.var2 == 1:
                special = self.chooseSpecialParking()
        else:
            special = [0, 0]

    def checkAvailablity(self, special):
        self.ps = self.pl.findAvailableSpot(self.var2.get(), special[0], special[1], self.curLicensePlate)
        if self.ps != 0:
            if self.subscribing:
                self.createPaymentBtn()
            else:
                self.btn_proceed_payment = Button(self.visitorWin, text="Get Ticket", command=self.getVisitorTicket)
                self.btn_proceed_payment.place(x=280, y=420)
        else:
            messagebox.showwarning("No parking Available", "No available spot!")
            self.visitorWin.destroy()

    def getVisitorTicket(self):
        if self.btn_proceed_payment is not None:
            self.btn_proceed_payment.destroy()
            self.btn_proceed_payment = None
        lbl = Label(self.visitorWin, text="Please proceed to parking spot: " + str(self.ps), font=("Terminal", 17))
        lbl.pack(pady=30)
        self.createTicket()
        tkinter.Button(self.visitorWin, text="Home", font=("Terminal", 17), command=self.homeBtn).pack()

    def homeBtn(self):
        self.clearFrame(self.win)
        self.welcome_window()

    def chooseSpecialParking(self):
        if self.cbtn1 is None:
            self.var3 = IntVar()
            self.cbtn1 = Checkbutton(self.visitorWin, text="Electric", variable=self.var3)
            self.cbtn1.pack(anchor=CENTER)
            self.var4 = IntVar()
            self.cbtn2 = Checkbutton(self.visitorWin, text="Handicapped", variable=self.var4)
            self.cbtn2.pack(anchor=CENTER)

    def clearSpecialParking(self):
        if self.cbtn1 is not None:
            self.cbtn1.destroy()
            self.cbtn1 = None
            self.cbtn2.destroy()
            self.cbtn2 = None

    def createSignUpWindow(self):
        self.subscribing = True
        self.clearFrame(self.visitorWin)
        self.visitorWin.title("Subscribe as a Modern Parking member")
        Label(self.visitorWin, text="Car License Number: " + self.curLicensePlate, font=("Terminal", 17)).pack(pady=20)
        Label(self.visitorWin, text="Select wanted period of subscription", font=("Terminal", 17)).pack(pady=20)
        self.var1 = IntVar()
        rbtn_P1 = Radiobutton(self.visitorWin, text="3 Months - 1000 NIS", variable=self.var1, value=1000)
        self.var1.set(1000)
        rbtn_P1.pack(anchor=CENTER)
        rbtn_P2 = Radiobutton(self.visitorWin, text="6 Months - 1500 NIS", variable=self.var1, value=1500)
        rbtn_P2.pack(anchor=CENTER)
        rbtn_P3 = Radiobutton(self.visitorWin, text="1 Year - 1800 NIS", variable=self.var1, value=1800)
        rbtn_P3.pack(anchor=CENTER)
        self.createVehicleTypeRB()
        if self.ps == 0:
            # show the error message
            messagebox.showerror("No availabale Parking Spot found", "We're so sorry, there is no available parking spot that matches your Vehicle")
        else:
            #payment
            self.createPaymentBtn()

    def createPaymentBtn(self):
        self.btn_proceed_payment = Button(self.visitorWin, text="Proceed to Payment",
                                          command=lambda: self.createPaymentWindow(self.var1, None, None))
        self.btn_proceed_payment.place(x=280, y=420)

    def createPaymentWindow(self, var1, p, ticket):
        self.paymentWin = Toplevel(self.win)
        self.paymentWin.resizable(False, False)
        self.paymentWin.geometry("630x500")
        self.paymentWin.title("Subscribed Modern Parking Payment")
        if p is None:
            tkinter.Button(self.paymentWin, text="Pay Cash", command=lambda: self.recognizeSubscribe()).pack(
                anchor=CENTER)
            tkinter.Button(self.paymentWin, text="Pay Credit", command=lambda: self.recognizeSubscribe()).pack(
                anchor=CENTER)
            Label(self.paymentWin, text="Total Cost: " + str(self.var1.get()), font=("Terminal", 17)).pack(pady=20)
        else:
            tkinter.Button(self.paymentWin, text="Pay Cash", command= lambda: self.leaveParkingLot(p, ticket)).pack(anchor=CENTER)
            tkinter.Button(self.paymentWin, text="Pay Credit", command=lambda: self.leaveParkingLot(p, ticket)).pack(anchor=CENTER)
            Label(self.paymentWin, text="Total Cost: " + str(var1), font=("Terminal", 17)).pack(pady=20)

    def createOneTimeWindow(self):
        self.clearFrame(self.visitorWin)
        self.visitorWin.title("Visitor at Modern Parking")
        Label(self.visitorWin, text="Car License Number: " + self.curLicensePlate, font=("Terminal", 17)).pack(pady=20)
        self.createVehicleTypeRB()

    # Function to clear the text entry box
    def clearField(self, field):
        field.delete(0, END)

    def clearFrame(self, window):
        # destroy all widgets from frame
        for widget in window.winfo_children():
            widget.destroy()
