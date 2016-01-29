#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos

# module with functions that manipulate service (or similar waiting4Services) lists

from constants import *
from timeTT import *
from operator import itemgetter


def afterCharge(servicesList_ac):
    """Updates a service to a after charge status.

    Requires:
    servicesList_ac is a list with a structure as in the output of consultStatus.waiting4ServicesList.
    Ensures:
    A list with the same strucure as the input, corresponding to the information about the driver/vehicle
    after one hour of charging, as described in the general specification (omitted here for the sake of
    readability)
    """

    servicesList_ac[INDEXClientName] = NOCLIENT
    servicesList_ac[INDEXArrivalHour] = add(servicesList_ac[INDEXArrivalHour], "01:00")
    servicesList_ac[INDEXDepartureHour] = servicesList_ac[INDEXArrivalHour]
    servicesList_ac[INDEXCircuitId] = NOCIRCUIT
    servicesList_ac[INDEXCircuitKms] = "0"
    servicesList_ac[INDEXDriverStatus] = STATUSStandBy

    return servicesList_ac


def noService(service):
    """Update a service's list when there is no service.

    Requires:
    service is a list with a structure as in the sublists of the
    output of consultStatus.readServicesFile.
    Ensures:
    a list with the structure of the sublists of consultStatus.readServicesFile where driver will
    have no client, no circuit, 0 circuit kms and a standby status.
    """
    service[INDEXClientName] = NOCLIENT
    service[INDEXCircuitId] = NOCIRCUIT
    service[INDEXCircuitKms] = "0"
    service[INDEXDriverStatus] = STATUSStandBy

    return service


def sortWaitingServices(waiting4Services):
    """Sorts a list of waiting4Services.

    Requires:
    waiting4Services is a list with the struture as in the output of consultStatus.waiting4ServicesList.
    Ensures:
    A list with the same structure as the input sorted by the
    arrival hour, then by the accumulated time, in case of ties,
    and at last by the driver's name in case of yet other ties.
    """

    sorted_Waiting4Services = sorted(waiting4Services,
                                     key=itemgetter(INDEXArrivalHour,
                                                    INDEXAccumulatedTime,
                                                    INDEXDriverName))

    return sorted_Waiting4Services


def sortServices(services):
    """Sorts a list of services.

    Requires:
    services is a list with the struture as in the output of consultStatus.readServicesFile.
    Ensures:
    A list with the same structure as the input sorted by the
    arrival hour and then by the driver's name, in the case of ties.
    """

    sorted_Services = sorted(services,
                             key=itemgetter(INDEXArrivalHour,
                                            INDEXDriverName))

    return sorted_Services


def resetVehic(service):
    """Changes the status of a driver/vehicle to 'standby'.

    Requires:
    service is a sublist of the output list of the function consultStatus.readServicesFile
    Ensures:
    A list with every element identical to list service, but in which the last
    element is substituted for 'standby'.
    """

    service[INDEXDriverStatus] = STATUSStandBy

    return service
