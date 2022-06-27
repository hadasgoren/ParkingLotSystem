from enum import Enum

from dateutil.relativedelta import relativedelta


class VehicleType(Enum):
    PRIVATE = 1
    LARGE = 2
    MOTORCYCLE = 3


class SubscriptionPeriod(Enum):
    MON3 = 1
    MON6 = 2
    Y1 = 3


class SubscribedVehicle(object):

    def __init__(self, license_plate, vehicle_type, electric, handicapped, subDate, sub_period):
        self.__license_plate = license_plate
        self.__vehicle_type = vehicle_type
        self.__electric = electric
        self.__handicapped = handicapped
        self.__subscription_date = subDate
        self.__subscription_period = sub_period

    def getLicensePlate(self):
        return self.__license_plate

    def getSubscriptionPeriod(self):
        return SubscriptionPeriod(self.__subscription_period).name

    def getVehicaleType(self):
        return VehicleType(self.__vehicle_type).name

    def getElectric(self):
        return self.__electric

    def getHandicapped(self):
        return self.__handicapped

    def getSubscripitionEndDate(self):
        return self.__subscription_date + relativedelta(months=self.__subscription_period.value)
