#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos



def hourToInt(time):
    """Splits time using : as a delimiter and obtain a list of substrings of time. 
    Then transforms substrings into integers and gives the hour of any time.
    Requires: time is of type string.
    Ensures: The transformation of the string time into integer and gives
    the zero position.
    """
    t = time.split(":")
    return int(t[0])
    


def minutesToInt(time):
    """Splits time using : as a delimiter and obtain a list of substrings of time.
    Then transforms substrings into integers and gives the minutes of any time.
    Requires: time is of type string.
    Ensures: The transformation of the string time into integer and gives
    the one position.
    """
    t = time.split(":")
    return int(t[1])

def intToTime(hour, minutes):
    """ Transforms hour and minutes into strings and gives the argument Time as a integer's type.
    Requires: hour and minutes are of the type integer.
    Ensures: The transformation of the integers hour and minutes into strings.
    """
    h = str(hour)
    m = str(minutes)

    if hour < 10:
        h = "0" + h
    else:
        h = h

    if minutes < 10:
        m = "0" + m
    else:
        m = m

    return h + ":" + m



def add(time1, time2):
    """ Adds a quantity of time to the working time already performed by the driver.
    Requires: time1 and time2 as strings.
    Ensures: A string with the accumulative time performed by the driver.
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
    """Removes a quantity of time to the working time already performed by the driver.
    Requires: time1 and time2 as strings.
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


