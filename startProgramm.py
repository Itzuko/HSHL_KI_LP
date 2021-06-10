import tkinter as tk
from tkinter import filedialog
import os

def start():
    
    __startImage__ = '''
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
 |______|______|______|______|______|______|______|______|______|______|'''

    print(__startImage__)
    print("\nWillkommen")
    print("Folgende Probleme können gelöst werden:")

#Array für die Dateien
fileListName = ['Eigene Datei auswählen']
fileListPath = ['LEER']

def showKIProblems():
    #Dateien Öffnen und zu den Arrays hinzufügen
    dir = 'KI_Benchmarks'
    for path in os.listdir(dir):
        full_path = os.path.join(dir, path)
        if os.path.isfile(full_path):
            fileListPath.append(full_path)
            fileListName.append(full_path.split("\\")[1])

    #Optionen Anzeigen
    tmpCounter = 0
    for fileName in fileListName:
        print( "[%d] %s\r" %(tmpCounter, fileName))
        tmpCounter = tmpCounter + 1

def getUserInput():
    #Auswahl vom User der Dateien
    choice = input("\n\rWelches Problem soll gelöst werden? [0 - " + str(len(fileListName) - 1) + " ]: ")
    print("Es wurde ''" + str(fileListName[int(choice)]) + "'' gewählt" )
    
    #Eigene Datei laden
    if int(choice) == 0:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        fileListPath[0] = file_path

    f = open(fileListPath[int(choice)])
    readFile = f.read()
    print('\n', readFile)
    return readFile


