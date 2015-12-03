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


def kmsLeftVehicle(service):
    """Calculates how many kilometes a vehicle can still do

    Requires:
    service is a sublist of a list with the structure as in the output of
    consultStatus.waiting4ServicesList
    Ensures:
    an int corresponding to the number of km the vehicle can still make
    """

    return int(service[INDEXINDEXVehicAutonomy]) - int(service[INDEXAccumulatedKms])


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

        print reservation
        for l in waiting4Services:
            print l
        print '\n'

        # checks if reservation would pass km limit of vehicle or time limit of driver and chooses another driver if that's the case
        i = 0
        while i < len(waiting4Services) and \
                (int(reservation[INDEXCircuitKmsInReservation]) >= kmsLeftVehicle(waiting4Services[i])
                or durationReservation(reservation) >= diff(TIMELimit, waiting4Services[i][INDEXAccumulatedTime])):
            i += 1

        # if there is no driver available to a reservation, try get some to work on next reservation
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

            for l in new_services:
                print l
            print '\n\n'

            # sorts waiting4Services so that drivers available earlier are assigned services first
            waiting4Services = sortWaitingServices(waiting4Services)

    return sortServices(new_services)


def afterCharge(servicesList_ac):

    servicesList_ac[INDEXClientName] = NOCLIENT
    servicesList_ac[INDEXArrivalHour] = add(servicesList_ac[INDEXArrivalHour], "01:00")
    servicesList_ac[INDEXDepartureHour] = servicesList_ac[INDEXArrivalHour]
    servicesList_ac[INDEXCircuitId] = NOCIRCUIT
    servicesList_ac[INDEXCircuitKms] = "0"
    servicesList_ac[INDEXDriverStatus] = STATUSStandBy

    return servicesList_ac


def sortWaitingServices(waiting4Services):

    sorted_Waiting4Services= sorted(waiting4Services, \
                                        key=itemgetter(INDEXArrivalHour, \
                                                    INDEXAccumulatedTime, \
                                                    INDEXDriverName))

    return sorted_Waiting4Services


def sortServices(services):

    sorted_Services= sorted(services, \
                                     key=itemgetter(INDEXArrivalHour, \
                                                    INDEXDriverName))
    return sorted_Services


#def afterCharge(service):
#    service[INDEXClientName] = NOCLIENT
#    service[INDEXCircuitId] = NOCIRCUIT
#    service[INDEXCircuitKms] = '0'
#    service[INDEXArrivalHour] = add(service[INDEXArrivalHour], '01:00')
#    service[INDEXDepartureHour] = service[INDEXArrivalHour]
#    service[INDEXDriverStatus] = STATUSStandBy
#
#    return service
#
#
#def sortWaitingServices(services):
#    return sorted(services, key=itemgetter(INDEXArrivalHour, INDEXAccumulatedTime, INDEXDriverName))
#
#
#def sortServices(services):
#    return sorted(services, key=itemgetter(INDEXArrivalHour, INDEXDriverName))

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

#reservations = [['Chris Cauly', '11:00', '11:30', 'baixa', '25'], ['Frank Gerry', '11:15', '11:45', 'belem', '40'], ['Michal Labelle', '11:35', '11:40', 'minibaixa', '15'], ['Zacarias Zack', '11:35', '11:45', 'minibaixa', '15'], ['Alfonso Dominguez', '11:40', '12:00', 'castelo', '45'], ['Chris Melga', '11:40', '12:40', 'castelo', '45'], ['Milan Kundera', '11:45', '12:35', 'sintra', '80'], ['John Smith', '12:00', '12:05', 'minibaixa', '20']]
#waiting4Services = [['Carlos Castro', '05-BB-99', 'Xavier Smith', '09:45', '10:15', 'baixa', '10', 'standby', '01:45', '175', '145'], ['Jonas Sousa', '17-GD-87', 'Yoshiro Kimoto', '09:50', '10:30', 'castelo', '45', 'standby', '01:00', '130', '50'], ['Alberto Campos', '19-HI-34', 'Paul Sondag', '09:30', '10:30', 'castelo', '45', 'standby', '01:50', '175', '150'], ['Duarte Silva', '17-GD-86', 'Jack London', '10:00', '10:45', 'bairroalto', '25', 'standby', '02:27', '175', '5']]
#result = [['Carlos Castro', '05-BB-99', 'Chris Cauly', '11:00', '11:30', 'baixa', '25', 'charges'], ['Alberto Campos', '19-HI-34', 'Michal Labelle', '11:35', '11:40', 'minibaixa', '15', 'charges'], ['Duarte Silva', '17-GD-86', 'Zacarias Zack', '11:35', '11:45', 'minibaixa', '15', 'standby'], ['Jonas Sousa', '17-GD-87', 'Frank Gerry', '11:15', '11:45', 'belem', '40', 'standby'], ['Duarte Silva', '17-GD-86', 'Alfonso Dominguez', '11:45', '12:05', 'castelo', '45', 'standby'], ['Jonas Sousa', '17-GD-87', 'John Smith', '12:00', '12:05', 'minibaixa', '20', 'standby'], ['Carlos Castro', '05-BB-99', '_no_client_', '12:30', '12:30', '_no_circuit_', '0', 'standby'], ['Alberto Campos', '19-HI-34', '_no_client_', '12:40', '12:40', '_no_circuit_', '0', 'standby'], ['Duarte Silva', '17-GD-86', 'Chris Melga', '12:05', '13:05', 'castelo', '45', 'standby'], ['Carlos Castro', '05-BB-99', 'Milan Kundera', '12:30', '13:20', 'sintra', '80', 'standby']]
#print updateServices(reservations, waiting4Services)
#
#print result
#print result == updateServices(reservations, waiting4Services)
#print '\n'


#
reservations = [['Conchita Gomez', '19:00', '19:30', 'baixa', '25'], ['Hugo Klim', '19:05', '19:35', 'baixa', '25'], ['Franz Beckenbauer', '19:15', '19:45', 'belem', '40'], ['Michelle Williams', '19:35', '19:40', 'minibaixa', '15'], ['Zoe Crimson', '19:35', '19:45', 'minibaixa', '15'], ['Albert Einstein', '19:40', '20:00', 'castelo', '45'], ['Chris Melga', '19:40', '20:40', 'castelo', '45'], ['Mike Shubert', '19:45', '20:35', 'sintra', '80'], ['John Malkovich', '20:00', '20:05', 'minibaixa', '20']]
waiting4Services = [['Catarina Castro', '05-BB-99', 'Susanne Smith', '17:45', '18:15', 'baixa', '10', 'standby', '01:45', '175', '145'], ['Nuno Santos', '34-TU-16', 'Maria Flick', '17:20', '18:20', 'mouraria', '30', 'standby', '03:20', '100', '30'], ['Ana Campos', '19-HI-34', 'Pierre Custeau', '17:30', '18:30', 'castelo', '45', 'standby', '01:50', '175', '150'], ['Jorge Sousa', '17-GD-87', 'Chris Simpson', '17:50', '18:30', 'castelo', '45', 'standby', '03:45', '130', '65'], ['Daniel Silva', '17-GD-86', '_no_client_', '18:45', '18:45', '_no_circuit_', '0', 'standby', '02:27', '175', '0']]
result = [['Catarina Castro', '05-BB-99', 'Conchita Gomez', '19:00', '19:30', 'baixa', '25', 'charges'], ['Nuno Santos', '34-TU-16', 'Hugo Klim', '19:05', '19:35', 'baixa', '25', 'standby'], ['Ana Campos', '19-HI-34', 'Michelle Williams', '19:35', '19:40', 'minibaixa', '15', 'charges'], ['Daniel Silva', '17-GD-86', 'Zoe Crimson', '19:35', '19:45', 'minibaixa', '15', 'standby'], ['Jorge Sousa', '17-GD-87', 'Franz Beckenbauer', '19:15', '19:45', 'belem', '40', 'standby'], ['Daniel Silva', '17-GD-86', 'Albert Einstein', '19:45', '20:05', 'castelo', '45', 'standby'], ['Nuno Santos', '34-TU-16', 'John Malkovich', '20:00', '20:05', 'minibaixa', '20', 'standby'], ['Catarina Castro', '05-BB-99', '_no_client_', '20:30', '20:30', '_no_circuit_', '0', 'standby'], ['Ana Campos', '19-HI-34', '_no_client_', '20:40', '20:40', '_no_circuit_', '0', 'standby'], ['Daniel Silva', '17-GD-86', 'Chris Melga', '20:05', '21:05', 'castelo', '45', 'standby'], ['Catarina Castro', '05-BB-99', 'Mike Shubert', '20:30', '21:20', 'sintra', '80', 'standby']]
a = updateServices(reservations, waiting4Services)
print a
print result
print a == result
print '\n'

# reservations = [['Conchita Suarez', '15:00', '15:45', 'baixa', '25'], ['Franz Muller', '15:15', '16:45', 'belem', '40'], ['Michelle Pfeiffer', '15:35', '17:35', 'sintra', '80'], ['Zoe Ruiz', '15:35', '15:50', 'minibaixa', '15'], ['Albert Schumaker', '15:40', '16:40', 'castelo', '45'], ['Chris Smith', '15:40', '16:40', 'castelo', '45'], ['Mike Melga', '15:45', '17:45', 'sintra', '80'], ['John Stuart', '16:00', '16:05', 'minibaixa', '20']]
# waiting4Services = [['Daniel Pereira', '17-GD-86', '_no_client_', '14:15', '14:15', '_no_circuit_', '0', 'standby', '04:27', '175', '0'], ['Rita Carvalho', '19-HI-34', 'Cavaco Silva', '12:30', '14:50', 'cascais', '70', 'standby', '02:50', '175', '75'], ['Luis Gomes', '34-TU-16', 'Stelios Callas', '12:50', '14:50', 'cristorei', '40', 'standby', '03:15', '100', '70'], ['Steven Neale', '05-BB-99', 'Helena Rodriguez', '13:35', '15:15', 'castelo', '45', 'standby', '02:10', '175', '70'], ['Catarina Correia', '67-BH-87', 'John Wayne', '14:50', '16:50', 'sintra', '80', 'standby', '02:00', '175', '80'], ['Nuno Sousa', '17-GD-87', 'Charles Simpson', '14:45', '17:15', 'sintra', '80', 'standby', '03:00', '130', '90']]
# result  = [['Rita Carvalho', '19-HI-34', 'Conchita Suarez', '15:00', '15:45', 'baixa', '25', 'standby'],['Daniel Pereira', '17-GD-86', 'Zoe Ruiz', '15:35', '15:50', 'minibaixa', '15', 'terminates'],['Luis Gomes', '34-TU-16', 'John Stuart', '16:00', '16:05', 'minibaixa', '20', 'charges'],['Rita Carvalho', '19-HI-34', 'Albert Schumaker', '15:45', '16:45', 'castelo', '45', 'terminates'],['Steven Neale', '05-BB-99', 'Franz Muller', '15:15', '16:45', 'belem', '40', 'standby'],['Luis Gomes', '34-TU-16', '_no_client_', '17:05', '17:05', '_no_circuit_', '0', 'standby'],['Nuno Sousa', '17-GD-87', '_no_client_', '14:45', '17:15', '_no_circuit_', '0', 'standby'],['Steven Neale', '05-BB-99', 'Chris Smith', '16:45', '17:45', 'castelo', '45', 'terminates'],['Catarina Correia', '67-BH-87', 'Michelle Pfeiffer', '16:50', '18:50', 'sintra', '80', 'standby']]
#
# print updateServices(reservations, waiting4Services)
# print result
# print result == updateServices(reservations, waiting4Services)
# print '\n'

# for testing afterCharge

#service = ['Carlos Castro', '05-BB-99', 'Chris Cauly', '11:00', '11:30', 'baixa', '25', 'charges', '02:15', '175', '0']
#result = ['Carlos Castro', '05-BB-99', '_no_client_', '12:30', '12:30',  '_no_circuit_', '0', 'standby', '02:15', '175', '0']
#
#print afterCharge(service)
#print result
#
