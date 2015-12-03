#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos


def changeFormatTime(period):
    #recebo isto 1921 e quero 19:00 - 21:00 esta tudo em str
    H1 = period[0:2]
    H2 = period[2:4]

    return H1 + ":00 - " + H2 + ":00"


def makeHeader(company, date, p, type):
    """Constructs a header for a file

    Requires:
    company is a string with the name of the company
    date is a string with a date in the format "DD:MM:YYYY"
    p is a string with the format "HHHH" indicating a
    2 hour period
    type is one of the following strings: "Reservations",
    "Services", "Drivers", "Vehicles"
    Ensures:
    a string with a header concerning period p, as in
    the examples given in the general specification (ommited here for the
    sake of readability)
    """
    header = "Company:," + company + ",Day:," + date + ",Period:," + changeFormatTime(p) + "," + type + ":"

    return header


def writeServicesFile(services_p, file_name_p, header_p):
    """Writes a collection of services into a file.

    Requires:
    services_p is a list with the structure as in the output of
    updateServices representing the services in a period p;
    file_name_p is a str with the name of a .txt file whose end (before
    the .txt suffix) indicates the period p, as in the examples provided in
    the general specification (omitted here for the sake of readability);
    and header is a string with a header concerning period p, as in
    the examples provided in the general specification (omitted here for
    the sake of readability).
    Ensures:
    writing of file named file_name_p representing the collection of
    services in services_p and organized as in the examples provided in
    the general specification (omitted here for the sake of readability);
    in the listing in this file keep the ordering of services in services_p.
    """

    f = open(file_name_p + '.txt', 'w')

    h = header_p.split(',')

    for line in h:
        f.write(line + '\n')

    for line in services_p:
        line = ', '.join(line)
        f.write(line + '\n')

    f.close()









