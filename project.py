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
print("{}".format(startImage))
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
tmpNumbersOfFunction = list(map(int, tmpFunctionString))
tmpNumbersOfFunction.append(0)
coefficients.append(tmpNumbersOfFunction)
allNumbersOfFile_List = coefficients
print("Vollständig:")
print(np.asarray(allNumbersOfFile_List))
# TRANSPONIEREN...
print("Transponiere...")
fullArray = trans(allNumbersOfFile_List)
#lengthFullArray = len(fullArray)-1
#for index ,value in enumerate(fullArray[lengthFullArray]):
#    fullArray[lengthFullArray][index] = value * -1

print(np.asarray(fullArray))

def creationOfTableau(array):
    length = len(array)-1
    tmpCounterForOne = 0
    
    for index, value in enumerate(array):
        tmpCounterAdder = 0
        
        if index == length:
            
            while tmpCounterAdder < length:
                tmpLength = len(value)
                value.insert(tmpLength-1, 0)
                tmpCounterAdder+=1
                
        else:
            while tmpCounterAdder < length:
                #switch case 
                tmpLength = len(value)
                if  tmpCounterForOne == index and tmpCounterForOne == tmpCounterAdder:
                    tmpCounterForOne += 1
                    value.insert(tmpLength-1,1)
                
                else: 
                    value.insert(tmpLength-1, 0)
                tmpCounterAdder+=1
        
        
        array[index] = value
    return array

print("Tableau aufbauen...")
fullArrayTableau = creationOfTableau(fullArray)
print(np.asarray(fullArrayTableau))


def findIndexForPivotColumn(tableau):
    length = len(tableau)
    print(tableau[:length])
    indexArray = 0
    highestValue = 0
    for index, value in enumerate(tableau[:length]):
        if value > highestValue:
            highestValue = value
            indexArray = index

    return indexArray

def findIndexForPivotRow(pivotColumn, endColumn):
    length = len(pivotColumn)-1
    tmpPivotColumnWithoutLast = pivotColumn[:length]
    engpassColumn = []
    #Engpass erstellen
    for index, value in enumerate(tmpPivotColumnWithoutLast):
        if(endColumn[index] != 0):
            engpassColumn.append(endColumn[index]/value)
        else:
            engpassColumn.append(endColumn[index])

    #print("engpassColumn: {}".format(engpassColumn)) 

    minValue = min(engpassColumn)
    indexArray = engpassColumn.index(minValue)



    return indexArray

def createColumn(indexPivotColumn, tableau):
    pivotColumn = []
    for value in tableau:
        pivotColumn.append(value[indexPivotColumn])

    return pivotColumn   

def createRow(indexPivotRow, tableau):
    return tableau[indexPivotRow]
    


def findPivotElement(tableu, indexColumn, IndexRow):
    pivotElement = tableu[IndexRow][indexColumn]
    return pivotElement
#Funktion um das PivotElement auf 1 zu bekommen
def dividePivotRowByPivotElement(tableau, indexColumn, indexRow):
    pivotElement = tableau[indexRow][indexColumn]
    
    newPivotRow = []

    for value in tableau[indexRow]:
        newPivotRow.append(value/pivotElement)
    
    return newPivotRow

#Fuunktion um die Pivotspalte auf 0 zu bekommen bis auf das Pivotelement
def setAllElementInPivotColumToZero(tableau, indexColumn, indexRow):
    newPivotColumn = createColumn(indexColumn, tableau)
    #print("newPivotColumn: \n{}".format(newPivotColumn))
    newPivotRow = createRow(indexRow, tableau)
    #print("newPivotRow: \n{}".format(newPivotRow))
    pivotElement = newPivotColumn[indexRow] #TODO: BUG mit indexColumn
    #print("PivotElement: {}".format(pivotElement))
    #Alle Zeilen außer PivotRow und Endzeile
    length = len(tableau)-1
    tmpArrayWithoutEnding = tableau[:length]
    tmpArrayWithoutPivotRowAndEnding = tmpArrayWithoutEnding[:indexRow] + tmpArrayWithoutEnding[indexRow+1:]
    #print("tmpArray: \n{}".format(np.asarray(tmpArrayWithoutPivotRowAndEnding)))

    for indexOne, valueOne in enumerate(tmpArrayWithoutPivotRowAndEnding):
        #print("Iteration:{}".format(indexOne))
        #print("Zeile:{}".format(valueOne))
        Faktor = valueOne[indexColumn]
        if(valueOne[indexColumn] == pivotElement or valueOne[indexColumn] == 0):
            for indexTwo, valueTwo in enumerate(valueOne):
                result = valueTwo - newPivotRow[indexTwo]
                tmpArrayWithoutPivotRowAndEnding[indexOne][indexTwo] = result
        elif(valueOne[indexColumn] < pivotElement or valueOne[indexColumn] > pivotElement):
             for indexThree, valueThree in enumerate(valueOne):
                result = valueThree - (newPivotRow[indexThree]*Faktor)
                tmpArrayWithoutPivotRowAndEnding[indexOne][indexThree] = result
    #LineEnding:
    functionArray = []
    functionFaktor = tableau[length][indexColumn]
    functionLength = len(tableau[length])-1

    for index, value in enumerate(tableau[length]):
        result = value - newPivotRow[index]*functionFaktor
        functionArray.append(result)
    tmpArrayWithoutPivotRowAndEnding.append(functionArray)
    tmpArrayWithoutPivotRowAndEnding.insert(indexRow, newPivotRow)
    
    return tmpArrayWithoutPivotRowAndEnding
        
def isFinal(tableau):
    state = False
    #print("ENDE")
    length = len(tableau)
    
    for value in tableau[length-1]:
        if value > 0:
            return state
        else:
            state = True

    return state

def multiplyFunctionWithMinusOne(tmpTableau):
    indexLastLine = len(tmpTableau)-1
    for index, value in enumerate(tmpTableau[indexLastLine]):
        tmpTableau[indexLastLine][index] = value * -1
    
    return tmpTableau

def getFinalValuesOfVariables(tmpTableau):
    tmpArray = []
    indexForOnes = []
    length = len(tmpTableau)-1
    tmpTableauWithoutEnd = tmpTableau[:length]
    tmpTableauTrans = trans(tmpTableauWithoutEnd)
    lengthTrans = len(tmpTableauTrans)-1
    tmpTableauTransWithoutEnd = tmpTableauTrans[:lengthTrans]
    forPrint = np.asarray(tmpTableauTrans)
    forPrintRounded = forPrint.round(2)
    #print("tmpTableTrans: \n{}".format(forPrintRounded))

    #Überprüfe ob die Zeile nur aus 0 oder 1 besteht
    for value in tmpTableauTransWithoutEnd:
        onlyOneAndZeros = False
        for index ,line in enumerate(value):
            #check if value 0 or 1
            if line == 0 or line == 1:
                onlyOneAndZeros = True
                if line == 1:
                    indexForOnes.append(index) 
            else:
                onlyOneAndZeros = False
                break
        if onlyOneAndZeros == True:
            tmpArray.append(True)
        else:
            tmpArray.append(False)
    #print("tmpArray:{}".format(tmpArray))
    indices = np.where(tmpArray)[0]
    #print(len(indices))
    #print("TandF:{}".format((indices)))
    #print("Index:{}".format(indexForOnes))
    valueArray = []
    for value in indexForOnes:
        temp = tmpTableau[value]
        tmpLength = len(temp)-1
        valueArray.append(temp[tmpLength])
        
    for index, value in enumerate(indices):
        print("x{0} = {1}".format(value, valueArray[index]))
    

def startAlgorithm(tableau):
    iteration = 0
    tmpTableau = tableau
    results = []
    while isFinal(tmpTableau) == False:
        #Finde Pivotspalte (zuerst Index finden und dann aufstellen)
        length = len(tmpTableau)-1
        indexPivotColumn = findIndexForPivotColumn(tmpTableau[length])
        pivotColumn = createColumn(indexPivotColumn, tmpTableau)
        #print("pivotColumn: {}".format(pivotColumn))
        endIndex = len(tmpTableau[length])-1
        endColumn = createColumn(endIndex, tmpTableau)
        #print("EndColumn: {}".format(endColumn))
        indexPivotRow = findIndexForPivotRow(pivotColumn,endColumn)
        #print("indexPivotRow: {}".format(indexPivotRow))
        pivotRow = createRow(indexPivotRow, tmpTableau)
        #print("pivotRow: {}".format(pivotRow))
        pivotElement = findPivotElement(tmpTableau,indexPivotColumn,indexPivotRow)
        #print("PivotElement:{}".format(pivotElement))
        if (pivotElement > 1):
            newPivotRow = dividePivotRowByPivotElement(tmpTableau,indexPivotColumn,indexPivotRow)
            #print("DividedRow: {}".format(newPivotRow))
        #Row an der passenden Stelle einfügen
        tmpTableau[indexPivotRow] = newPivotRow
        #print("Neues Tableau: \n{}".format(np.asarray(tmpTableau)))
        iteration += 1
        print("Iteration: {}".format(iteration))
        tmpTableau = setAllElementInPivotColumToZero(tmpTableau,indexPivotColumn, indexPivotRow)
        forPrint = np.asarray(tmpTableau)
        forPrintRounded = forPrint.round(2)
        print("{}".format(forPrintRounded))

    if(isFinal(tmpTableau) == True):
        print("Ende.")
        tmpTableau = multiplyFunctionWithMinusOne(tmpTableau)
        forPrint = np.asarray(tmpTableau)
        forPrintRounded = forPrint.round(2)
        print("Finales Tableau:\n{}".format(forPrintRounded))
        getFinalValuesOfVariables(tmpTableau)
        tableauLength = len(tmpTableau)-1
        finalValue = len(tmpTableau[tableauLength])-1
        resultValue = tmpTableau[tableauLength][finalValue]
        print("result: {}".format(resultValue))

startAlgorithm(fullArrayTableau)
#Algorithmus
# 1. Zielfunktionszeile höchster Wert => Pivotspalte
# 2. Letzte Spalte drch Pivotspalte teilen
# 3. Ergebnise = Engpass Einschränkung
# -> leinster Wert = Pivotzeile
# 4. Krezung zwischen Pivotspalte und Pivotzeile = Pivotelement
# Prüfe ob PivotElement = 1 --> Falls nicht auf eins Bringen --> Zeile durch PivotElement teilen
# 5. Alles in der Pivotspalte außer Pivotelement auf 0 bringen