#-*- coding: utf-8 -*-

# 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos


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
