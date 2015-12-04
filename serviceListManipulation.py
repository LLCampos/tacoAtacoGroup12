#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos



from constants import *
from timeTT import *
from operator import itemgetter

# FALTA ESPECIFICAÇÕES
def afterCharge(servicesList_ac):

    servicesList_ac[INDEXClientName] = NOCLIENT
    servicesList_ac[INDEXArrivalHour] = add(servicesList_ac[INDEXArrivalHour], "01:00")
    servicesList_ac[INDEXDepartureHour] = servicesList_ac[INDEXArrivalHour]
    servicesList_ac[INDEXCircuitId] = NOCIRCUIT
    servicesList_ac[INDEXCircuitKms] = "0"
    servicesList_ac[INDEXDriverStatus] = STATUSStandBy

    return servicesList_ac


# PARA A PATRÍCIA FAZER
def noService(service):
    service[INDEXClientName] = NOCLIENT
    service[INDEXCircuitId] = NOCIRCUIT
    service[INDEXCircuitKms] = "0"
    service[INDEXDriverStatus] = STATUSStandBy

    return service


def sortWaitingServices(waiting4Services):

    sorted_Waiting4Services= sorted(waiting4Services,
                                        key=itemgetter(INDEXArrivalHour,
                                                    INDEXAccumulatedTime,
                                                    INDEXDriverName))

    return sorted_Waiting4Services


def sortServices(services):

    sorted_Services= sorted(services,
                            key=itemgetter(INDEXArrivalHour,
                                           INDEXDriverName))
    return sorted_Services


def resetVehic(service):
    """Changes the type of activity of a driver/vehicle to 'standby'

    Requires:
    service is a sublist of the output list of the function readServicesFile
    Ensures:
    list with every element identical to list service, but in which the last
    element is substituted for 'standby'
    """
    service[INDEXDriverStatus] = STATUSStandBy
    return service
