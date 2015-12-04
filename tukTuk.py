#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos

import sys
from consultStatus import *
from planning import updateServices
from outputStatus import writeServicesFile

nextPeriod = sys.argv[1]
driversFileName = sys.argv[2]
vehiclesFileName = sys.argv[3]
servicesFileName = sys.argv[4]
reservationsFileName = sys.argv[5]

def update(nextPeriod, driversFileName, vehiclesFileName, \
           servicesFileName, reservationsFileName):
    """Obtains the planning for a period of activity.

    Requires:
    nextPeriod is a str from the set 0911, 1113, ..., 1921 indicating the
    2 hour period to be planned;
    driversFileName is a str with the name of a .txt file containing a list
    of drivers organized as in the examples provided;
    vehiclesFileName is a str with the name of a .txt file containing a list
    of vehicles organized as in the examples provided;
    servicesFileName is a str with the name of a .txt file containing a list
    of services organized as in the examples provided;
    reservationsFileName is a str with the name of a .txt file containing
    a list of reserved services organized as in the examples provided;
    the files whose names are driversFileName, vehiclesFileName,
    servicesFileName and reservationsFileName concern the same company and
    the same day;
    the file whose name is reservationsFileName concerns the period
    indicated by nextPeriod;
    the files whose names are driversFileName, vehiclesFileName,
    servicesFileName concern the period immediately preceding the period
    indicated by nextPeriod;
    the file name reservationsFileName ends (before the .txt extension) with
    the string nextPeriod;
    the file names driversFileName, vehiclesFileName and servicesFileName
    end (before their .txt extension) with the string representing
    the period immediately preceding the one indicated by nextPeriod,
    from the set 0709, 0911, ..., 1719;
    Ensures:
    writing of .txt file containing the updated list of services for
    the period nextPeriod according to the requirements in the general
    specifications provided (omitted here for the sake of readability);
    the name of that file is outputXXYY.txt where XXYY represents
    the nextPeriod.
    """
    outputFileName = 'output' + 'nextPeriod'

    drivers = readDriversFile(driversFileName)
    vehicles = readVehiclesFile(vehiclesFileName)
    services = readServicesFile(servicesFileName)
    reservations = readReservationsFile(reservationsFileName)

    waiting4Services = waiting4ServicesList(drivers, vehicles, services)

    newServices = updateServices(reservations, waiting4Services)

    writeServicesFile(newServices, outputFileName, header)














