#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos

from constants import *
from timeTT import *


def calculateDelay(old_service, reservation):
    """Calculates start and end times of the new_service, with delay, if that's the case.

    Requires:
    reservation is a sublist of a list with the structure as in the output of
    consultStatus.readReservationsFile; service is a sublist of a list with
    the structure as in the output of consultStatus.waiting4ServicesList
    Ensures:
    A two-element list in which the first element is the starting time of the service
    with or without delay and the second element is the end time of the service with
    or without delay.
    """
    delay = '00:00'

    if diff(old_service[INDEXArrivalHour], reservation[INDEXRequestedStartHour]) > '00:00':
        delay = diff(old_service[INDEXArrivalHour], reservation[INDEXRequestedStartHour])

    startHour = add(reservation[INDEXRequestedStartHour], delay)
    endHour = add(reservation[INDEXRequestedEndHour], delay)

    return [startHour, endHour]


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
    """Calculates how many kilometers a vehicle can still do

    Requires:
    service is a sublist of a list with the structure as in the output of
    consultStatus.waiting4ServicesList
    Ensures:
    an int corresponding to the number of km the vehicle can still make
    """

    return int(service[INDEXINDEXVehicAutonomy]) - int(service[INDEXAccumulatedKms])
