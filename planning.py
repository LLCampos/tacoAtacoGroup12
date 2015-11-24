#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos

from constants import *
from timeTT import *
from copy import deepcopy


def updateOneService(reservation, service):
    """Assign a driver with her vehicle to a service that was reserved.

    Requires:
    reservation is a sublist of a list with the structure as in the output of
    consultStatus.readReservationsFile; service is a sublist of a list with
    the structure as in the output of consultStatus.waiting4ServicesList
    Ensures:
    a list with the structure of the sublists of consultStatus.waiting4ServicesList
    where the driver and her vehicle are assigned to a reservation
    (unless the first condition of the ifelse block is true. In that case the
    structure of the list is the same as the sublists of the output of
    consultStatus.readServicesFile)
    """
    new_service = []
    new_service[INDEXDriverName] = service[INDEXDriverName]
    new_service[INDEXVehiclePlate] = service[INDEXVehiclePlate]
    new_service[INDEXClientName] = reservation[INDEXClientNameInReservation]
    new_service[INDEXDepartureHour] = reservation[INDEXRequestedStartHour]
    new_service[INDEXArrivalHour] = reservation[INDEXRequestedEndHour]
    new_service[INDEXCircuitId] = reservation[INDEXCircuitInReservation]
    new_service[INDEXCircuitKms] = reservation[INDEXCircuitKmsInReservation]

    duration = diff(new_service[INDEXArrivalHour], new_service[INDEXDepartureHour])
    new_accumulated_hours = add(service[INDEXAccumulatedTime], duration)
    allowed_time_left = diff(TIMELimit, new_accumulated_hours)

    new_accumulated_kms = add(service[INDEXAccumulatedKms], new_service[INDEXCircuitKms])
    allowed_kms_left = diff(service[INDEXINDEXVehicAutonomy], new_accumulated_kms)

    if allowed_time_left < TIMEThreshold:
        new_service[INDEXDriverStatus] = STATUSTerminated
    elif allowed_kms_left < AUTONThreshold:
        new_service[INDEXDriverStatus] = STATUSCharging
        new_service[INDEXAccumulatedTime] = new_accumulated_hours
        new_service[INDEXINDEXVehicAutonomy] = service[INDEXINDEXVehicAutonomy]
        new_service[INDEXAccumulatedKms] = 0
    else:
        new_service[INDEXDriverStatus] = STATUSStandBy
        new_service[INDEXAccumulatedTime] = new_accumulated_hours
        new_service[INDEXINDEXVehicAutonomy] = service[INDEXINDEXVehicAutonomy]
        new_service[INDEXAccumulatedKms] = new_accumulated_kms

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
        old_service = waiting4Services.pop(0)
        new_service = updateOneService(reservation, old_service)
        new_services.append(new_service[:INDEXDriverStatus + 1])

        if new_service[INDEXDriverStatus] == STATUSCharging:
            charged = afterCharge(new_service)
            new_services.append(charged[:INDEXDriverStatus + 1])
            waiting4Services.append(charged)

        elif new_service[INDEXDriverStatus] == STATUSStandBy:
            waiting4Services.append(new_service)

        waiting4Services = sortWaiting4Services(waiting4Services)

    return sortServices(new_services)

    # fazer funções afterCharge, sortWaiting4Services e sortServices
















