#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos

# Especificações não dizem supostamente apenas o que a função faz e não como o faz?
# Falar de driver?


def hourToInt(time):
    """Gives the hour of any time.
    Requires: time is of type string.
    Ensures: The transformation of the string time into integer and gives
    the zeroth position.
    """
    t = time.split(":")
    return int(t[0])


def minutesToInt(time):
    """Gives the minutes of any time.
    Requires: time is of type string.
    Ensures: The transformation of the string time into integer and gives
    the first position.
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
    """ Adds a quantity of time to the working time elapsed.
    Requires: time1 and time2 as strings with "hh:mm" format.
    Ensures: A string with the accumulative time elapsed.
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
    """Removes a quantity of time to the working time time elapsed.
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
    #recebo isto 1921 e quero 19:00 - 21:00 esta tudo em str
    H1 = period[0:2]
    H2 = period[2:4]

    return H1 + ":00 - " + H2 + ":00"




