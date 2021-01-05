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

def trans(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]


#Füge die Funktion der Liste hinzu
tmpFunction = FileLineSplit[1][4:]
tmpFunctionRegex = re.compile(r"(\d+)(?:\*)")
tmpFunctionString = re.findall(tmpFunctionRegex, tmpFunction)
#print(tmpFunctionString)
tmpNumbersOfFunction = list(map(int, tmpFunctionString))
#print(tmpNumbersOfFunction)
tmpNumbersOfFunction.append(0)
#print(tmpNumbersOfFunction)
coefficients.append(tmpNumbersOfFunction)
allNumbersOfFile_List = coefficients
print("Vollständig:")
print(allNumbersOfFile_List)
#fullArray = np.transpose(allNumbersOfFile_List)
# TRANSPONIEREN...
print("Transponiere...")
fullArray = trans(allNumbersOfFile_List)
print(fullArray)

def creationOfTableau(array):
    length = len(array)-1
    print("Length: {}".format(length))
    arrayWithoutFunction = array[:length]
    tmpCounterForOne = 0
    #Nur Constraints
    for index, value in enumerate(arrayWithoutFunction):

        #print(value)
        #print(index)
        tmpCounterAdder = 0
        
        while tmpCounterAdder < length:
            tmpLength = len(value)
            #switch case 
            if  tmpCounterForOne == index and tmpCounterForOne == tmpCounterAdder:
                tmpCounterForOne += 1
                value.insert(tmpLength-1,1)
                
            else: 
                value.insert(tmpLength-1, 0)
            tmpCounterAdder+=1
        
        arrayWithoutFunction[index] = value
        #print("ArrayWithoutFunction: {}".format(arrayWithoutFunction))
    print("ArrayWithoutFunction: {}".format(arrayWithoutFunction))
    
    
    print(array[length])
    


creationOfTableau(fullArray)
