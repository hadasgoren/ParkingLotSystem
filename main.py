import tkinter
from tkinter import *
from tkinter.ttk import *
from ParkingScreen import *
from PIL import Image, ImageTk
from random import *
import random
import ParkingLot
import ParkingTicket
from ParkingTicket import *
import SubscribedVehicle
from SubscribedVehicle import *
from ParkingSpot import *
from ParkingSpot import ParkingSpotType
from SubscribedVehicle import SubscriptionPeriod
from enum import Enum
from datetime import datetime, date, timedelta


def main():
    print("start")


if __name__ == "__main__":
    main()
    # Creating window
    window = Tk()
    parkingScreen = ParkingScreen(window)
    createRandomParkingSpots(parkingScreen.pl)
    createRandomSubscribers(parkingScreen.pl)
    createRandomTickets(parkingScreen.pl)
    window.title("Modern Parking")
    window.geometry('630x500')
    window.configure(bg='white')
    window.resizable(False, False)
    window.mainloop()


def createRandomParkingSpots(pl):
    # create 100 random Parking Spots
    for i in range(1, 100):
        newParkingSpot = ParkingSpot(('P'+str(i)), randrange(1, 10), choice(list(ParkingSpotType)), random.randint(0, 1), random.randint(0, 1))
        pl.allParkingSpots.append(newParkingSpot)


def createRandomSubscribers(pl):
    for i in range(1, 50):
        newSubscriber = SubscribedVehicle(generateRandLicensePlate(pl), random.choice(list(VehicleType)),
                                          random.randint(0, 1), random.randint(0, 1), createRandomDate(), choice(list(SubscriptionPeriod)))
        pl.activeSubscriptions.append(newSubscriber)
    pl.activeSubscriptions.append(SubscribedVehicle('1234567', 1, 0, 0, createRandomDate(), choice(list(SubscriptionPeriod))))


def generateRandLicensePlate(pl):
    nums = '0123456789'
    tempLicensePlate = ''
    flag = True
    while flag:
        for n in range(8):
            tempLicensePlate += str(random.choice(nums))
        # check uniqueness
        for s in pl.activeSubscriptions:
            if tempLicensePlate == s.getLicensePlate():
                flag = True
        else:
            flag = False
    return str(tempLicensePlate)


def createRandomTickets(pl):
    randLicensePlate = generateRandLicensePlate(pl)
    spot = findSub(randLicensePlate, pl)
    for i in range(1, 20):
        if spot != None:
            newTicket = ParkingTicket(randLicensePlate, bool(random.getrandbits(1)), pl.findAvailableSpot(sub.getVehicalType(), sub.getElectric(), sub.getHandicapped(), randLicensePlate))
        else:
            newTicket = ParkingTicket(randLicensePlate, bool(random.getrandbits(1)), pl.findAvailableSpot(random.choice(list(VehicleType)), 0, 0, randLicensePlate))
        pl.activeTickets.append(newTicket)


def findSub(randLicensePlate, pl):
    for sub in pl.activeSubscriptions:
        if sub.getLicensePlate() == randLicensePlate:
            ps = pl.ParkingLot.findAvailableSpot(sub.getVehicalType(), sub.getElectric(), sub.getHandicapped(), randLicensePlate)
            return ps
    return None


def createRandomDate():
    start_date = date(2022, 2, 10)
    end_date = date.today()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date
