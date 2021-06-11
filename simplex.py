import re
import numpy as np
from numpy.lib.shape_base import split

#Verwendeter Algorithmus
# 1. Zielfunktionszeile höchster Wert => Pivotspalte
# 2. Letzte Spalte durch Pivotspalte teilen
# 3. Ergebnisse = Engpass Einschränkung => kleinster Wert = Pivotzeile
# 4. Kreuzung zwischen Pivotspalte und Pivotzeile => Pivotelement
# Prüfe ob PivotElement = 1 --> Falls nicht auf eins Bringen --> Zeile durch PivotElement teilen
# 5. Alles in der Pivotspalte außer Pivotelement auf 0 bringen

def startSimplex(ProblemToHandle):
    splitLines = ProblemToHandle.splitlines()
    #Überprüfung, ob Minimierungs- oder Maximierungsproblem
    isMinProblem = checkIfMinOrMax(ProblemToHandle,splitLines)
    print("Status, ob Minimierungsproblem: ",isMinProblem)
    #Constraints auslesen
    constraints = readConstraints(ProblemToHandle, splitLines)
    #print(constraints)
    #Objectivefunction an den constraints anhängen
    constraintsWithFunction = addFunctionToList(splitLines, constraints)
    #Aufgebaute Matrix
    print("\nMatrix:")
    print(np.asarray(constraintsWithFunction))
    #Matrix transponieren falls Minimierungsproblem
    if isMinProblem:
        constraintsWithFunction = trans(constraintsWithFunction)
        print("\nTransponiere...")
        print(np.asarray(constraintsWithFunction))
    #Tableau aufbauen
    Tableau = createTableau(constraintsWithFunction)
    
    print("{}\n".format(np.asarray(Tableau)))
    startAlgorithm(Tableau, isMinProblem)

def checkIfMinOrMax(ProblemToHandle, splitLines):
    minOrMax = splitLines[1][:3]
    isMinProblem = False
    if minOrMax == "min":
        isMinProblem = True 
    elif minOrMax =="max":
        isMinProblem = False
    else:
        print("Etwas ist schiefgelaufen")
        #TODO: Programm neustarten
    
    return isMinProblem

def readConstraints(ProblemToHandle, lineCount):
    constraintsArray = lineCount[3:]
    coef_regex = re.compile(r"(\d+)(?:\*|;)")
    coef_string = [coef_regex.findall(i) for i in constraintsArray]
    coefficients = [list(map(int, x)) for x in coef_string]
    return coefficients

def addFunctionToList(splitLine, constraints):
    tmpFunction = splitLine[1][4:]
    tmpFunctionRegex = re.compile(r"(\d+)(?:\*)")
    tmpFunctionString = re.findall(tmpFunctionRegex, tmpFunction)
    tmpNumbersOfFunction = list(map(int, tmpFunctionString))
    tmpNumbersOfFunction.append(0)
    coefficients = constraints
    coefficients.append(tmpNumbersOfFunction)
    return coefficients

def trans(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

def createTableau(array):
    print("\nTableau aufbauen...")
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

def startAlgorithm(tableau, isMinProblem):
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
        print("PivotElement:{}".format(pivotElement))
        #TODO:HIER LIEGT EIN FEHLER VOR
        if (pivotElement != 1 or pivotElement != 0):
            newPivotRow = dividePivotRowByPivotElement(tmpTableau,indexPivotColumn,indexPivotRow)
            #print("DividedRow: {}".format(newPivotRow))
            tmpTableau[indexPivotRow] = newPivotRow
            outputTableau = np.asarray(tmpTableau)
            print("Neues Tableau mit Pivotelement auf 1:")
            with np.printoptions(precision=3, suppress=True):
                print(outputTableau)

            #print("Neues Tableau mit Pivotelement auf 1: \n{}\n".format(outputTableau))
        #Row an der passenden Stelle einfügen
        
        iteration += 1
        print("Iteration: {}".format(iteration))
        tmpTableau = setAllElementInPivotColumToZero(tmpTableau,indexPivotColumn, indexPivotRow)
        
        with np.printoptions(precision=2, suppress=True):
            print(np.asarray(tmpTableau))

    print("\n--------------------")
    print("Ende")
    print("--------------------")
    tmpTableau = multiplyFunctionWithMinusOne(tmpTableau)
    if(isMinProblem):
        print("Is Min Problem")
        #print(np.asarray(tmpTableau))
        tmpTableau = trans(tmpTableau)
        #print(np.asarray(tmpTableau))
    forPrint = np.asarray(tmpTableau)
    print(" Finales Tableau:")
    with np.printoptions(precision=3, suppress=True):
        print(forPrint)
    #Formatiertes Tableau
    #print("\nFinales Tableau:\n {} \n".format(forPrintRounded))
    #Einzelne Werte
    getFinalValues(tmpTableau)
    #getFinalValuesOfVariables(tmpTableau)
    #Optimum bestimmen
    tableauLength = len(tmpTableau)-1
    finalValue = len(tmpTableau[tableauLength])-1
    resultValue = tmpTableau[tableauLength][finalValue]
    print("\nOptimum: {}".format(resultValue))

def findIndexForPivotColumn(tableau):
    length = len(tableau)
    #print(tableau[:length])
    indexArray = 0
    highestValue = 0
    for index, value in enumerate(tableau[:length]):
        if value > highestValue:
            highestValue = value
            indexArray = index

    return indexArray

engpassIndexKeineWerte = {}
def findIndexForPivotRow(pivotColumn, endColumn):
    length = len(pivotColumn)-1
    tmpPivotColumnWithoutLast = pivotColumn[:length]
    engpassColumn = []

    #Engpass erstellen
    for index, value in enumerate(tmpPivotColumnWithoutLast):
        if(endColumn[index] != 0):
            tmpValue = endColumn[index]/value
            engpassColumn.append(endColumn[index]/value)
            if (tmpValue < 0):
                engpassIndexKeineWerte[index] = True
        else:
            #Prüfe ob der Wert Null ist und falls ja ob dieser Bereits in der Liste engpassIndexKeineWerte existiert
            if(endColumn[index] == 0):
                if index in engpassIndexKeineWerte:
                    print("Existiert bereits");
                else:
                    engpassIndexKeineWerte[index] = False
            engpassColumn.append(endColumn[index])

    #Durch Engpass Iterieren. Werte die < 0 sind, ersetzen mit 999999
    for value in engpassIndexKeineWerte:
        if(engpassIndexKeineWerte[value] == True):
            engpassColumn[value] = 99999;
        elif(engpassIndexKeineWerte[value]==False):
            engpassIndexKeineWerte[value] = True
    
    print("engpassColumn: {}".format(engpassColumn)) 
    minValue = min(engpassColumn)
    indexFromLowestValue = engpassColumn.index(minValue)
    
    return indexFromLowestValue

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

    for index,value in enumerate(tableau[indexRow]):
        if index == indexColumn:
             #set pivotelement to 1
            tmpValue = pivotElement*(1/pivotElement)
        else:
            tmpValue = value/pivotElement
        newPivotRow.append(tmpValue)
       
    
    return newPivotRow

#Funktion um die Pivotspalte auf 0 zu bekommen bis auf das Pivotelement
def setAllElementInPivotColumToZero(tableau, indexColumn, indexRow):
    newPivotColumn = createColumn(indexColumn, tableau)
    #print("newPivotColumn: \n{}".format(newPivotColumn))
    newPivotRow = createRow(indexRow, tableau)
    #print("newPivotRow: \n{}".format(newPivotRow))
    pivotElement = newPivotColumn[indexRow]
    print("PivotElement: {}".format(pivotElement))
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
    #print(tableau[length-1])
    
    for value in tableau[length-1]:
        if value > 0:
            state = False
            break
        elif value <=0 :
            state = True

    return state

def multiplyFunctionWithMinusOne(tmpTableau):
    indexLastLine = len(tmpTableau)-1
    for index, value in enumerate(tmpTableau[indexLastLine]):
        tmpTableau[indexLastLine][index] = value * -1
    
    return tmpTableau

def getFinalValues(tableau):
    finalValueArray = []
    lengthOfTableauWithoutFunction = len(tableau)-1
    tableauWithoutFunction = tableau[:lengthOfTableauWithoutFunction]
    for value in tableauWithoutFunction:
        #print(value) 
        lengthOfValue = len(value)-1
        finalValue = value[lengthOfValue]
        finalValueArray.append(finalValue)

    roundedFinalValueArray= np.asarray(finalValueArray)
    roundedFinalValueArray = roundedFinalValueArray.round(2)
    for index, value in enumerate(roundedFinalValueArray):
        print("x{0} = {1}".format(index, roundedFinalValueArray[index])) 
