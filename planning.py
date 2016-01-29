#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos

from constants import *
from timeTT import *
from calculations import *
from copy import deepcopy
from serviceListManipulation import *


def addNoServiceDriver(new_services, waiting4Services):
    """Adds the drivers/vehicles that had no service in the current period to the list
    of new services.

    Requires:
    new_services is a list of lists with the structure of the output of
    consultStatus.readServicesFile although not necessarilly ordered;
    waiting4Services is a list of lists with the structure of
    consultStatus.waiting4ServicesList
    Ensures:
    a list of lists similar to new_services but with list(s), corresponding
    to drivers/vehicles which had no service in the current, appended to it.
    """
    # list of names of drivers with services
    drivers_with_services = [service[INDEXDriverName] for service in new_services]

    # services of the previous period of the drivers which got no services in this period
    drivers_with_no_services = [driver[:INDEXDriverStatus + 1] for driver in waiting4Services if driver[INDEXDriverName] not in drivers_with_services]

    for driver in drivers_with_no_services:
        driver = noService(driver)
        new_services.append(driver)

    return new_services


def nextDriver(reservation, waiting4Services):
    """Returns the index of the driver/vehicle to work on the reservation.

    Requires:
    reservation is a sublist of a list with the structure as in the output of
    consultStatus.readReservationsFile; waiting4ServicesList_prevp is a list
    with the structure as in the output of consultStatus.waiting4Services.
    Ensures:
    An int corresponding to the index of waiting4Services of the driver/vehicle
    to work on the reservation. If the int returned is equal to the length
    of waiting4Services then neither of the drivers got the reservation.
    """
    i = 0
    # checks if reservation would pass km limit of vehicle or time limit of driver and chooses another driver if that's the case
    # while cycle stops also when all the drivers were checked
    while i < len(waiting4Services) and \
            (int(reservation[INDEXCircuitKmsInReservation]) >= kmsLeftVehicle(waiting4Services[i]) or
             durationReservation(reservation) >= diff(TIMELimit, waiting4Services[i][INDEXAccumulatedTime])):
        i += 1

    return i


def updateOneService(reservation, old_service):
    """Assign a driver with her vehicle to a service that was reserved.

    Requires:
    reservation is a sublist of a list with the structure as in the output of
    consultStatus.readReservationsFile; service is a sublist of a list with
    the structure as in the output of consultStatus.waiting4ServicesList.
    Ensures:
    a list with the structure of the sublists of consultStatus.waiting4ServicesList
    where the driver and her vehicle are assigned to a reservation
    (unless the first condition of the ifelse block is true. In that case the
    structure of the list is the same as the sublists of the output of
    consultStatus.readServicesFile). See specifications of UpdateServices for more
    information.
    """
    # Adds information to the new service
    new_service = []
    new_service.append(old_service[INDEXDriverName])
    new_service.append(old_service[INDEXVehiclePlate])
    new_service.append(reservation[INDEXClientNameInReservation])

    # checks if it's going to be a delay, that is, if the driver/vehicle is not available at the requested time
    startHour, endHour = calculateDelay(old_service, reservation)

    new_service.append(startHour)
    new_service.append(endHour)

    new_service.append(reservation[INDEXCircuitInReservation])
    new_service.append(reservation[INDEXCircuitKmsInReservation])

    # Calculates how much work time is left for the driver after this service
    duration = durationReservation(reservation)
    new_accumulated_hours = add(old_service[INDEXAccumulatedTime], duration)
    allowed_time_left = diff(TIMELimit, new_accumulated_hours)

    # Calculates how much kms are left fot the vehivle after this service
    new_accumulated_kms = int(old_service[INDEXAccumulatedKms]) + int(new_service[INDEXCircuitKms])
    allowed_kms_left = int(old_service[INDEXINDEXVehicAutonomy]) - new_accumulated_kms

    # Adds the rest of the information, depending on the allowed time and kms left
    if allowed_time_left < TIMEThreshold:
        new_service.append(STATUSTerminated)
    elif allowed_kms_left < AUTONThreshold:
        new_service.append(STATUSCharging)
        new_service.append(new_accumulated_hours)
        new_service.append(old_service[INDEXINDEXVehicAutonomy])
        new_service.append('0')
    else:
        new_service.append(STATUSStandBy)
        new_service.append(new_accumulated_hours)
        new_service.append(old_service[INDEXINDEXVehicAutonomy])
        new_service.append(str(new_accumulated_kms))

    return new_service


def updateServices(reservations_p, waiting4ServicesList_prevp):

    """Assigns drivers with their vehicles to services that were reserved.

    Requires:
    reservations_p is a list with a structure as in the output of
    consultStatus.readReservationsFile; waiting4ServicesList_prevp is a list
    with the structure as in the output of consultStatus.waiting4ServicesList;
    objects in reservations_p concern a period p, and objects in
    waiting4ServicesList_prevp concern a period immediately preceding p.
    Ensures:
    list L of lists, where each list has the structure of
    consultStatus.readServicesFile, representing the services to be provided
    in a period starting in the beginning of the period p upon they having
    been reserved as they are represented in reservations_p;
    Reservations with earlier booking times are served first (lexicographic
    order of clients' names is used to resolve eventual ties);
    Drivers available earlier are assigned services first (lexicographic
    order of their names is used to resolve eventual ties) under
    the following conditions:
    If a driver has less than 30 minutes left to reach their 5 hour
    daily limit of accumulated activity, he is given no further service
    in that day (this is represented with a service entry marhed with
    "terminates");
    Else if a vehicle has less than 15 kms autonomy, it is recharged
    (this is represented with a service entry marked with "charges") and
    is available 1 hour later, after recharging (this is represented with
    another service entry, marked with "standby").
    in this list L:
    drivers terminating their services earlier have priority over the ones
    terminating later;
    in case of eventual ties, drivers with less accumulated time have
    priority over the ones with more accumulated time;
    lexicographic order of drivers's names decides eventual ties
    in each case above.
    """

    waiting4Services = deepcopy(waiting4ServicesList_prevp)

    new_services = []

    for reservation in reservations_p:

        # checks if reservation would pass km limit of vehicle or time limit of driver and chooses another driver if that's the case
        i = nextDriver(reservation, waiting4Services)

        # if there is no driver available to a reservation, try get some to work on the next reservation
        if i == len(waiting4Services):
            next
        else:

            old_service = waiting4Services.pop(i)
            new_service = updateOneService(reservation, old_service)
            new_services.append(new_service[:INDEXDriverStatus + 1])

            # makes driver and vehicle available again, after charging
            if new_service[INDEXDriverStatus] == STATUSCharging:
                charged = afterCharge(new_service)
                new_services.append(charged[:INDEXDriverStatus + 1])
                waiting4Services.append(charged)

            elif new_service[INDEXDriverStatus] == STATUSStandBy:
                waiting4Services.append(new_service)

            # sorts waiting4Services so that drivers available earlier are assigned services first
            waiting4Services = sortWaitingServices(waiting4Services)

    # adds to new_services the drivers that had no service in this period
    new_services = addNoServiceDriver(new_services, waiting4Services)

    return sortServices(new_services)
