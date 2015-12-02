#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos

from constants import *
from timeTT import *
from copy import deepcopy
from operator import itemgetter


def durationReservation(reservation):
    """Calculates duration of a service

    Requires:
    reservation is a sublist of a list with the structure as in the output of
    consultStatus.readReservationsFile;
    Ensures:
    string in the format 'HH:MM' corresponding to the duration of the service
    """

    return diff(reservation[INDEXRequestedEndHour], reservation[INDEXRequestedStartHour])


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
    consultStatus.readServicesFile). See specifications of UpdateServices for more
    information
    """
    # Adds information to the new service
    new_service = []
    new_service.append(service[INDEXDriverName])
    new_service.append(service[INDEXVehiclePlate])
    new_service.append(reservation[INDEXClientNameInReservation])

    # checks if it's going to be a delay, if there's no driver available at the requested time
    delay = '00:00'
    if diff(service[INDEXArrivalHour], reservation[INDEXRequestedStartHour]) > '00:00':
        delay = diff(service[INDEXArrivalHour], reservation[INDEXRequestedStartHour])

    new_service.append(add(reservation[INDEXRequestedStartHour], delay))
    new_service.append(add(reservation[INDEXRequestedEndHour], delay))

    new_service.append(reservation[INDEXCircuitInReservation])
    new_service.append(reservation[INDEXCircuitKmsInReservation])

    # Calculates how much work time is left for the driver after this service
    duration = durationReservation(reservation)
    new_accumulated_hours = add(service[INDEXAccumulatedTime], duration)
    allowed_time_left = diff(TIMELimit, new_accumulated_hours)

    # Calculates how much kms are left fot the vehivle after this service
    new_accumulated_kms = int(service[INDEXAccumulatedKms]) + int(new_service[INDEXCircuitKms])
    allowed_kms_left = int(service[INDEXINDEXVehicAutonomy]) - new_accumulated_kms

    # Adds the rest of the information, depending on the allowed time and kms left
    if allowed_time_left < TIMEThreshold:
        new_service.append(STATUSTerminated)
    elif allowed_kms_left < AUTONThreshold:
        new_service.append(STATUSCharging)
        new_service.append(new_accumulated_hours)
        new_service.append(service[INDEXINDEXVehicAutonomy])
        new_service.append('0')
    else:
        new_service.append(STATUSStandBy)
        new_service.append(new_accumulated_hours)
        new_service.append(service[INDEXINDEXVehicAutonomy])
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

        #i = 0
        #while int(waiting4Services[i][INDEXINDEXVehicAutonomy]) - int(waiting4Services[i][INDEXAccumulatedKms]) < int(reservation[INDEXCircuitKmsInReservation]):
            #i += 1

        old_service = waiting4Services.pop(1)
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

    return sortServices(new_services)


def afterCharge(service):
    service[INDEXClientName] = NOCLIENT
    service[INDEXCircuitId] = NOCIRCUIT
    service[INDEXCircuitKms] = '0'
    service[INDEXArrivalHour] = add(service[INDEXArrivalHour], '01:00')
    service[INDEXDepartureHour] = service[INDEXArrivalHour]
    service[INDEXDriverStatus] = STATUSStandBy

    return service


def sortWaitingServices(services):
    return sorted(services, key=itemgetter(INDEXArrivalHour, INDEXAccumulatedTime, INDEXDriverName))


def sortServices(services):
    return sorted(services, key=itemgetter(INDEXArrivalHour, INDEXDriverName))

# for testing updateOneService:

# service = ['Carlos Castro', '05-BB-99', 'Xavier Smith', '09:45', '10:15', 'baixa', '10', 'standby', '01:45', '175', '145']
# reservation = ['Chris Cauly', '11:00', '11:30', 'baixa', '25']
# result = ['Carlos Castro', '05-BB-99', 'Chris Cauly', '11:00', '11:30', 'baixa', '25', 'charges', '02:15', '175', '0']

# print updateOneService(reservation, service)
# print result
# print '\n'

# service = ['Carlos Castro', '05-BB-99', 'Xavier Smith', '09:45', '10:15', 'baixa', '10', 'standby', '01:45', '600', '145']
# reservation = ['Chris Cauly', '11:00', '11:30', 'baixa', '25']
# result = ['Carlos Castro', '05-BB-99', 'Chris Cauly', '11:00', '11:30', 'baixa', '25', 'standby', '02:15', '600', '170']
#
# print updateOneService(reservation, service)
# print result
# print '\n'
#
# service = ['Carlos Castro', '05-BB-99', 'Xavier Smith', '09:45', '10:15', 'baixa', '10', 'standby', '04:46', '600', '145']
# reservation = ['Chris Cauly', '11:00', '11:30', 'baixa', '25']
# result = ['Carlos Castro', '05-BB-99', 'Chris Cauly', '11:00', '11:30', 'baixa', '25', 'terminates']
#
# print updateOneService(reservation, service)
# print result
# print '\n'


# for testing updateServices

reservations = [['Chris Cauly', '11:00', '11:30', 'baixa', '25'], ['Frank Gerry', '11:15', '11:45', 'belem', '40'], ['Michal Labelle', '11:35', '11:40', 'minibaixa', '15'], ['Zacarias Zack', '11:35', '11:45', 'minibaixa', '15'], ['Alfonso Dominguez', '11:40', '12:00', 'castelo', '45'], ['Chris Melga', '11:40', '12:40', 'castelo', '45'], ['Milan Kundera', '11:45', '12:35', 'sintra', '80'], ['John Smith', '12:00', '12:05', 'minibaixa', '20']]
waiting4Services = [['Carlos Castro', '05-BB-99', 'Xavier Smith', '09:45', '10:15', 'baixa', '10', 'standby', '01:45', '175', '145'], ['Jonas Sousa', '17-GD-87', 'Yoshiro Kimoto', '09:50', '10:30', 'castelo', '45', 'standby', '01:00', '130', '50'], ['Alberto Campos', '19-HI-34', 'Paul Sondag', '09:30', '10:30', 'castelo', '45', 'standby', '01:50', '175', '150'], ['Duarte Silva', '17-GD-86', 'Jack London', '10:00', '10:45', 'bairroalto', '25', 'standby', '02:27', '175', '5']]
result = [['Carlos Castro', '05-BB-99', 'Chris Cauly', '11:00', '11:30', 'baixa', '25', 'charges'], ['Alberto Campos', '19-HI-34', 'Michal Labelle', '11:35', '11:40', 'minibaixa', '15', 'charges'], ['Duarte Silva', '17-GD-86', 'Zacarias Zack', '11:35', '11:45', 'minibaixa', '15', 'standby'], ['Jonas Sousa', '17-GD-87', 'Frank Gerry', '11:15', '11:45', 'belem', '40', 'standby'], ['Duarte Silva', '17-GD-86', 'Alfonso Dominguez', '11:45', '12:05', 'castelo', '45', 'standby'], ['Jonas Sousa', '17-GD-87', 'John Smith', '12:00', '12:05', 'minibaixa', '20', 'standby'], ['Carlos Castro', '05-BB-99', '_no_client_', '12:30', '12:30', '_no_circuit_', '0', 'standby'], ['Alberto Campos', '19-HI-34', '_no_client_', '12:40', '12:40', '_no_circuit_', '0', 'standby'], ['Duarte Silva', '17-GD-86', 'Chris Melga', '12:05', '13:05', 'castelo', '45', 'standby'], ['Carlos Castro', '05-BB-99', 'Milan Kundera', '12:30', '13:20', 'sintra', '80', 'standby']]

print updateServices(reservations, waiting4Services)
print result
print result == updateServices(reservations, waiting4Services)
print '\n'

# for testing afterCharge

#service = ['Carlos Castro', '05-BB-99', 'Chris Cauly', '11:00', '11:30', 'baixa', '25', 'charges', '02:15', '175', '0']
#result = ['Carlos Castro', '05-BB-99', '_no_client_', '12:30', '12:30',  '_no_circuit_', '0', 'standby', '02:15', '175', '0']
#
#print afterCharge(service)
#print result

