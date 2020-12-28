import os
import sys
import numpy as np
import re

startImage = ("""
  ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
 |______|______|______|______|______|______|______|______|______|______|
  _    _  _____ _    _ _
 | |  | |/ ____| |  | | |                                               
 | |__| | (___ | |__| | |                                               
 |  __  |\___ \|  __  | |                                               
 | |  | |____) | |  | | |____                                           
 |_| _|_|_____/|_|  |_|______|
 |_  _ _____            _____           _      _    _                   
 | |/ /_   _|          |  __ \         (_)    | |  | |                  
 | ' /  | |    ______  | |__) | __ ___  _  ___| | _| |_                 
 |  <   | |   |______| |  ___/ '__/ _ \| |/ _ \ |/ / __|                
 | . \ _| |_           | |   | | | (_) | |  __/   <| |_                 
 |_|\_\_____|          |_|   |_|__\___/| |\___|_|\_\\__|                
 |_____                         _____ _/ |
 |  __ (_)                     / ____|__/       | |                     
 | |__) |  ___ _ __ _ __ ___  | (___  _   _  ___| | _____ _ __          
 |  ___/ |/ _ \ '__| '__/ _ \  \___ \| | | |/ __| |/ / _ \ '__|         
 | |   | |  __/ |  | | |  __/  ____) | |_| | (__|   <  __/ |            
 |_|   |_|\___|_|  |_|  \___| |_____/ \__,_|\___|_|\_\___|_|            
  ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
 |______|______|______|______|______|______|______|______|______|______|""")
print(startImage)
print("\nWillkommen")
print("Folgende Probleme können gelöst werden")
#Array für die Dateien
fileListName = []
fileListPath = []

#Dateien Öffnen und zu den Array hinzufügen
d = 'KI_Benchmarks'
for path in os.listdir(d):
    full_path = os.path.join(d, path)
    if os.path.isfile(full_path):
        fileListPath.append(full_path)
        fileListName.append(full_path.split("\\")[1])

#Anzeigen zwischen den Optionen
tmpCounter = 0
for fileName in fileListName:
    print( "[%d] %s\r" %(tmpCounter, fileName))
    tmpCounter = tmpCounter + 1

#Auswahl vom User der Dateien
choice = input("\n\rWelches Problem soll gelöst werden? [0 - " + str(tmpCounter-1) + " ]: ")
print("Es wurde gewählt", fileListName[int(choice)])

#Öffnen und Ausgabe der Datei
f = open(fileListPath[int(choice)])
readFile = f.read()
print(readFile)

def checkIfMin (stringToCheck):
    print("Überprüfe ob Min oder Max Problem")
    if stringToCheck == "min":
        print("min")
        return True 
    elif stringToCheck =="max":
        print("max")
        return False
    else:
        print("Etwas ist schiefgelaufen")
        #TODO: Programm neustarten

#Prüfe ob minimierungsproblem
FileLineSplit = readFile.splitlines()
minOrMax = FileLineSplit[1][:3]
print(minOrMax)
isMinProblem = checkIfMin(minOrMax)
print("Status ob minimierungsproblem: ",isMinProblem)

#Anzahl der Constraints
lineCount = readFile.splitlines()
constraintsArray = lineCount[3:]
coef_regex = re.compile(r"(\d+)(?:\*|;)")
coef_string = [coef_regex.findall(i) for i in constraintsArray]
coefficients = [list(map(int, x)) for x in coef_string]


#Füge zum Array die Funktion hinzu
tmpFunction = FileLineSplit[1][4:]
tmpFunctionRegex = re.compile(r"(\d+)(?:\*)")
tmpFunctionString = re.findall(tmpFunctionRegex, tmpFunction)
tmpNumbersOfFunction = list(map(int, tmpFunctionString))
tmpNumbersOfFunction.append("x")
coefficients.append(tmpNumbersOfFunction)
allNumbersOfFile = coefficients
print(allNumbersOfFile)