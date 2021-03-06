#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos

from constants import *
from copy import deepcopy
from operator import itemgetter
from serviceListManipulation import resetVehic
from headerRelated import removeHeader


def readDriversFile(file_name):
    """Reads a file with a list of drivers into a collection.

    Requires:
    file_name is str with the name of a .txt file containing
    a list of drivers organized as in the examples provided in
    the general specification (omitted here for the sake of readability).
    Ensures:
    dict where each item corresponds to a driver listed in
    file with name file_name, a key is the string with the name of a driver,
    and a value is the list with the other elements belonging to that
    driver, in the order provided in the lines of the file.
    """

    inFile = removeHeader(open(file_name, "r"))
    driversDict = {}
    for line in inFile:
        driverData = line.rstrip().split(', ')
        driverName = driverData.pop(INDEXDriverName)
        driversDict[driverName] = driverData

    return driversDict


def readVehiclesFile(file_name):
    """Reads a file with a list of vehicles into a collection.

    Requires:
    file_name is str with the name of a .txt file containing
    a list of vehicles organized as in the examples provided in
    the general specification (omitted here for the sake of readability).
    Ensures:
    dict where each item corresponds to a vehicle listed in
    file with name file_name, a key is the string with the plate of a vehicle,
    and a value is the list with the other elements belonging to that
    vehicle, in the order provided in the lines of the file.
    """

    inFile = removeHeader(open(file_name, "r"))

    vehiclesDict = {}
    for line in inFile:
        vehicleData = line.rstrip().split(", ")
        vehiclePlate = vehicleData.pop(INDEXVehiclePlateInDict)
        vehiclesDict[vehiclePlate] = vehicleData

    return vehiclesDict


def readServicesFile(file_name):
    """Reads a file with a list of services into a collection.

    Requires:
    file_name is str with the name of a .txt file containing
    a list of services organized as in the examples provided in
    the general specification (omitted here for the sake of readability).
    Ensures:
    list L of lists, where each list corresponds to a service listed
    in file with name file_name and its elements are the elements
    belonging to that service in the order provided in the lines of
    the file.
    in this list L:
    drivers terminating their services earlier have priority over the ones
    terminating later;
    lexicographic order of drivers's names decides eventual ties
    in each case above.
    """

    inFile = removeHeader(open(file_name, "r"))

    servicesList = []
    for line in inFile:
        servicesList.append(line.rstrip().split(", "))

    return servicesList


def readReservationsFile(file_name):
    """Reads a file with a list of reservations into a collection.

    Requires:
    file_name is a string with the name of a .txt file containing
    a list of reservations organized as in the examples provided in
    the general specification (omitted here for the sake of readability).
    Ensures:
    list L of lists, where each list corresponds to a reservation
    listed in file name with file_name and its elements are
    the elements belonging to that reservation in the order provided in
    the lines of the file.
    in this list L:
    clients reserving a service with an earlier starting time have
    priority over the ones with later starting times;
    lexicographic order of clients's names decides eventual ties.
    """

    inFile = removeHeader(open(file_name, "r"))

    reservationsList = []
    for line in inFile:
        reservationsList.append(line.rstrip().split(", "))

    return reservationsList


def waiting4ServicesList(drivers_p, vehicles_p, services_p):
    """Organizes a list of active drivers with their assigned
    vehicles that can take further services.

    Requires:
    drivers_p is a dict with a structure as in the output
    of readDriversFile; vehicles_p is a dict with the structure as in
    the output of readVehiclesFile; services_p is a list with the structure
    as in the output of readServicesFile; the objects in drivers_p,
    vehicles_p and services_p concern the same period p.
    Ensures:
    a list L of lists with a structure similar to the output of
    readServicesFile and obtained by:
    extracting the sublist SL of services_p where each list in
    that sublist SL corresponds to the last representation of an active
    driver, converted to a “standby” status (older representations of active
    drivers and representations of terminated drivers are excluded),
    and by appending to each list of that subset SL 3 further elements:
    one with the accumulated time of the driver, another with the autonomy
    of his vehicle in kilometers for a fully charged batery, and yet
    another with the accumulated kilometers of that vehicle;
    in this list L:
    drivers terminating their services earlier have priority over the ones
    terminating later;
    in case of eventual ties, drivers with less accumulated time have
    priority over the ones with more accumulated time;
    lexicographic order of drivers's names decides eventual ties
    in each case above.
    """

    serviceList = deepcopy(services_p)
    serviceList.reverse()

    driversInWaitingList = []
    detailedWaitingList = []

    # Obtains sublist SL
    for service in serviceList:
        driver = service[INDEXDriverName]
        driverTerminated = service[INDEXDriverStatus] == STATUSTerminated
        if (driver not in driversInWaitingList) and (not driverTerminated):
            if service[INDEXDriverStatus] == STATUSCharging:
                service = resetVehic(service)
            driversInWaitingList.append(driver)
            detailedWaitingList.append(service)

    # Enriches SL with 3 further data items
    for service in detailedWaitingList:
        driverName = service[INDEXDriverName]
        driverAccumulatedTime = drivers_p[driverName][INDEXAccumulatedTimeInDict]
        service.append(driverAccumulatedTime)
        vehiclePlate = service[INDEXVehiclePlate]
        vehicleKms = vehicles_p[vehiclePlate][INDEXVehicleAutonomyInDict:]
        service.extend(vehicleKms)

    # Puts it back to the original order
    detailedWaitingList.reverse()

    # Sorting according to increasing availability time,
    # untying with drivers's names
    detailedWaitingList = sorted(detailedWaitingList, \
                                 key=itemgetter(INDEXArrivalHour, \
                                                INDEXAccumulatedTime, \
                                                INDEXDriverName))

    return detailedWaitingList


