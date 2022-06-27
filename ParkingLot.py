from enum import Enum
import ParkingTicket
import ParkingSpot
import SubscribedVehicle
import datetime


class vehical_type_enum(Enum):
    PRIVATE = 1
    LARGE = 2
    MOTORCYCLE = 3


class ParkingLot(object):
    def __init__(self):
        self.allParkingSpots = []
        # all active subscribers, identified by their vehicle's license Plate
        self.activeSubscriptions = []
        # all active parking tickets, identified by their ticket_number
        self.activeTickets = []

    def isFull(self):
        if len(self.allParkingSpots) == len(self.activeTickets):
            return True
        return False

    def checkActiveSubscriber(self, license_plate):
        for subscriber in self.activeSubscriptions:
            if (subscriber.getLicensePlate() == license_plate) and (subscriber.getSubscripitionEndDate() >= datetime.date.today()):
                return subscriber
        return None

    def checkActiveTicket(self, license_plate):
        for ticket in self.activeTickets:
            if ticket.getLicensePlate() == license_plate:
                return True
        return False

    def addParkingSpot(self, parking_spot):
        self.__allParkingSpots.append(parking_spot)

    def deleteParkingSpot(self, parking_spot_id):
        self.__allParkingSpots.remove(self.__allParkingSpots.index(ParkingSpot.getParkingSpotId() == parking_spot_id))

    def findAvailableSpot(self, vehicle_type, electric, handicapped, licensePlate):
        if self.isFull():
            return 0
        match vehicle_type:
            case 'PRIVATE':
                for p in self.allParkingSpots:
                    if p.getParkingType() == vehicle_type and p.getElectric() == electric and p.getHandicapped() == handicapped and p.checkIfOccupied() is False:
                        print("private spot found")
                        return p.getParkingId()
                return 0
            case 'LARGE':
                for p in self.allParkingSpots:
                    if p.getParkingType() == vehicle_type and p.checkIfOccupied() is False:
                        print("Large spot found")
                        return p.getParkingId()
                return 0
            case 'MOTORCYCLE':
                for p in self.allParkingSpots:
                    if p.getParkingType() == vehicle_type and p.checkIfOccupied() is False:
                        print("Motorcycle spot found")
                        return p.getParkingId()
                return 0

    def registration(self):
        pass

    def entrance(self, vehicle):  # created ticket
        if self.isFull(vehicle.get_type()):
            raise Exception('Parking full!')
        ticket = ParkingTicket()
        vehicle.assign_ticket(ticket)
        ticket.save_in_DB()
        # if the ticket is successfully saved in the database, we can increment the parking spot count
        self.__increment_spot_count(vehicle.get_type())
        self.__active_tickets.put(ticket.get_ticket_number(), ticket)
        self.__lock.release()
        return ticket
