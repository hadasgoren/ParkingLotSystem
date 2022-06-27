from enum import Enum


class ParkingSpotType(Enum):
    PRIVATE = 1
    LARGE = 2
    MOTORCYCLE = 3


class ParkingSpot:
    def __init__(self, parking_id, parking_rate, parking_type, electric, handicapped):
        self.__parking_id = parking_id
        self.__parking_rate = parking_rate  # Per Hour
        self.__parking_type = parking_type
        self.__occupied = False
        self.__electric = electric
        self.__handicapped = handicapped

    def getParkingId(self):
        return self.__parking_id

    def getParkingRate(self):
        return self.__parking_rate

    def getParkingType(self):
        return ParkingSpotType(self.__parking_type).name

    def checkIfOccupied(self):
        return self.__occupied

    def getElectric(self):
        return self.__electric

    def getHandicapped(self):
        return self.__handicapped

    def setOccupied(self, occupied):
        self.__occupied = occupied
