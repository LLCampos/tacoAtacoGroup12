#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos


def hourToInt(time):
    """Gives the number of hours of time.

    Requires: time is of type string, with format "HH:MM".
    Ensures: returns an integer corresponding to the number of hours of time.
    """
    t = time.split(":")
    return int(t[0])


def minutesToInt(time):
    """Gives the number of minutes of time.

    Requires: time is of type string, with format "HH:MM".
    Ensures: returns an integer corresponding to the number of minutes of time.
    """
    t = time.split(":")
    return int(t[1])


def intToTime(hour, minutes):
    """ Gives time as a string.
    Requires: hour and minutes are of the type integer.
    Ensures: The transformation of the integers hour and minutes into strings.
    """
    h = str(hour)
    m = str(minutes)

    if hour < 10:
        h = "0" + h

    if minutes < 10:
        m = "0" + m

    return h + ":" + m


def add(time1, time2):
    """Calculates the sum between two times.

    Requires: time1 and time2 as strings with "hh:mm" format.
    Ensures: A string with the sum of time1 and time2.
    """
    t1Hour = hourToInt(time1)
    t1Minutes = minutesToInt(time1)
    t2Hour = hourToInt(time2)
    t2Minutes = minutesToInt(time2)

    hours = (t1Minutes + t2Minutes) / 60
    minutes = (t1Minutes + t2Minutes) % 60

    t1H = t1Hour + t2Hour + hours
    t1M = minutes

    return intToTime(t1H, t1M)


def diff(time1, time2):
    """Calculates the difference between two times.

    Requires: time1 and time2 as strings with "hh:mm" format.
    Ensures: A string with the difference between time1 and time2.
    """
    t1Hour = hourToInt(time1)
    t1Minutes = minutesToInt(time1)
    t2Hour = hourToInt(time2)
    t2Minutes = minutesToInt(time2)

    t1H = t1Hour - t2Hour
    minutes = t1Minutes - t2Minutes
    t1M = abs(minutes)

    if minutes < 0:
        t1H = t1H - 1
        t1M = 60 - t1M

    if t1H < 0:
        t1H = 0
        t1M = 0

    return intToTime(t1H, t1M)


def changeFormatTime(period):
    """Change format of a period from 'HHHH' into 'HH:MM - HH:MM'.

    Requires:
    period is a string with the format 'HHHH'.
    Ensures:
    string with format 'HH:MM - HH:MM'.
    """

    H1 = period[0:2]
    H2 = period[2:4]

    return H1 + ":00 - " + H2 + ":00"


def getPreviousPeriod(period):
    """Gets the time of the previous 2 hour period.

    Requires:
    period is a string with the format 'HHHH'
    corresponding to a 2 hour period.
    Ensures:
    A string in the same format as the input, corresponding
    to the previous 2 hour period.
    """

    H1 = period[0:2]

    newH1 = str(int(H1) - 2)

    if len(newH1) == 1:
        newH1 = '0' + newH1

    newH2 = H1

    return newH1 + newH2
