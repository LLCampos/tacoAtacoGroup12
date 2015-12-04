#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos

from constants import *
from timeTT import changeFormatTime

def removeHeader(file):
    """Removes the header of any file (drivers, vehicles, reservations or services)

    Requires:
    file is of type file, containing a list of drivers, vehicles, reservations
    or services organized as in the examples provided in the general
    specification (omitted here for the sake of readability).
    Ensures:
    list where each element corresponds to each line after the header,
    that is, each element corresponds to information about a driver, vehicle,
    reservation or service
    """
    return file.readlines()[NUMBEROfLinesInHeader:]

# PATRICIA
def createNewHeader(serviceFileName, new_period):

    new_period = changeFormatTime(new_period)

    file = open(serviceFileName, 'r')

    header = file.readlines()[:NUMBEROfLinesInHeader]
    header[5] = new_period

    header = ','.join(header)
    header = header.replace('\n','')

    file.close()

    return header

