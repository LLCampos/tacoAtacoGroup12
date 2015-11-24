#-*- coding: utf-8 -*-

# 2015-2016 # 2015-2016 Fundamentos de Programação (FP)
# Grupo 12
# 43071 Ana Patrícia Dos Santos Abrantes
# 43134 Luís Filipe Leal Campos



# This module records the constants used in the application



# Limit of driver's daily allowed time to drive
TIMELimit = "05:00"

# Limit of driver's daily allowed time left to be able
# to be assigned a next service
TIMEThreshold = "00:30"

# Limit of vehicle's autonomy in kms left to be able
# to be assigned a next service
AUTONThreshold = 15

# No client assigned
NOCLIENT = "_no_client_"

# Duration of the recharging operation
RECHDURATION = "01:00"

# No circuit assigned
NOCIRCUIT = "_no_circuit_"



# In a file:
# Number of line in a header
NUMBEROfLinesInHeader = 7



# In a service list:
# Index of element with driver's name
INDEXDriverName = 0

# Index of element with vehicle's plate
INDEXVehiclePlate = 1

# Index of element with clients's name
INDEXClientName = 2

# Index of departure hour
INDEXDepartureHour = 3

# Index of arrival hour
INDEXArrivalHour = 4

# Index of circuit id
INDEXCircuitId = 5

# Index of circuit kms
INDEXCircuitKms = 6

# Index of driver's status
INDEXDriverStatus = 7

# Index of driver's accumlated time
INDEXAccumulatedTime = 8

# Index of element with car's autonomy in kms
INDEXINDEXVehicAutonomy = 9

# Index of element with accumulated kms
INDEXAccumulatedKms = 10

# Status of driver with no time left in the day
STATUSTerminated = "terminates"

# Status of car charging battery
STATUSCharging = "charges"

# Status of driver waiting for next service
STATUSStandBy = "standby"

# Status of driver with no service assigned yet
STATUSNoServiceYet = "00:00"



# In a reservation list:
# Index of element with requested start hour
INDEXClientNameInReservation = 0

# Index of element with requested start hour
INDEXRequestedStartHour = 1

# Index of element with requested start hour
INDEXRequestedEndHour = 2

# Index of circuit id
INDEXCircuitInReservation = 3

# Index of circuit length in kms
INDEXCircuitKmsInReservation = 4


# In a vehicles dict
# Index of element with vehicle's plate
INDEXVehiclePlateInDict = 0

# Index of element with vehicle's autonomy
INDEXVehicleAutonomyInDict = 1


# In a drivers dict
# Index of element with driver's beggining of activity time
INDEXDriverBeginInDict = 0

# Index of element with driver's accumulated time
INDEXAccumulatedTimeInDict = 1
