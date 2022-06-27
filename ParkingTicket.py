from enum import Enum
from datetime import datetime
from dateutil.relativedelta import relativedelta
import ParkingSpot


class ParkingTicketStatus(Enum):
    ACTIVE = 1
    PAID = 2
    LOST = 3


class ParkingTicket(object):
    def __init__(self, licensePlate, subscribed, parkingId):
        self.__vehicleLicensePlate = licensePlate
        self.__ticketStatus = ParkingTicketStatus.ACTIVE
        self.__issueTime = datetime.now()
        self.__leaveTime = None
        self.__totalCost = 0
        self.__isSubscribed = subscribed
        self.__parkingId = parkingId

    def getTicketStatus(self):
        return self.ticketStatus

    def getLicensePlate(self):
        return self.__vehicleLicensePlate

    def getParkingId(self):
        return self.__parkingId

    def calcTotalCost(self, parkId):
        if self.__isSubscribed:
            return 0
        return parkId.getParkingRate()*(self.calcStayTime(self.__issueTime, self.__leaveTime))

    def calcStayTime(self, start, end):
        end = datetime.now()
        diff_in_hours = (end - start).total_seconds() / 3600
        return diff_in_hours

    def getSubscribed(self):
        return self.__isSubscribed

    def assignParkingSpot(self, licensePlate, parkingId):
        pass

    def checkActiveSubscription(self, start):
        match self.__subscription_period:
            case 'MON3':
                if datetime.today() < self.__subscription_date + relativedelta(months=+3):
                    self.ticketStatus = ParkingTicketStatus.PAID
                else:
                    self.ticketStatus = ParkingTicketStatus.ACTIVE
            case 'MON6':
                if datetime.today() < start + relativedelta(months=+6):
                    self.ticketStatus = ParkingTicketStatus.PAID
                else:
                    self.ticketStatus = ParkingTicketStatus.ACTIVE
            case '1Y':
                if datetime.today() < start + relativedelta(years=+1):
                    self.ticketStatus = ParkingTicketStatus.PAID
                else:
                    self.ticketStatus = ParkingTicketStatus.ACTIVE
            case _:
                pass
