#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos

# module with functions related to the header of files

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


def getHeader(fileName):
    """Gets the header of a file.

    Requires:
    fileName is string with name of the file from which we want to get the header.
    This file is organized as in the examples provided in the general
    specification (omitted here for the sake of readability).
    Ensures:
    a list where each element corresponds to a header's line of the file
    with the name fileName.
    """

    file = open(fileName, 'r')
    header = file.readlines()[:NUMBEROfLinesInHeader]
    file.close()

    return header


def createNewHeader(fileName, new_period):
    """Creates a new header, with the new period.

    Requires:
    fileName is string with name of the file from which we want to get the header.
    This file is organized as in the examples provided in the general
    specification (omitted here for the sake of readability)
    new_period is a string corresponding to the next period,
    in the format HHHH (see general specifications).
    Ensures:
    a string with the header of the file named fileName,
    but in which the line corresponding to the period is
    substitued for the period in new_period.
    """

    # Changes the new_period format to the one used in the files
    new_period = changeFormatTime(new_period)

    header = getHeader(fileName)

    header[INDEXPeriod] = new_period

    # Turns header into string, each line separated by commas. To understand the
    # use of commas, see outputStatus.writeServicesFile
    header = ','.join(header)

    # Deletes newlines
    header = header.replace('\n', '')

    return header
