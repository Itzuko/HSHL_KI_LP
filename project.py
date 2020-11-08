import os
import sys
startImage = ("""  ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
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
 |______|______|______|______|______|______|______|______|______|______""")
print(startImage)
print("\nWillkommen")
print("Folgende Probleme könne gelöst werden")
#Array for Files
fileListName = []
fileListPath = []

d = 'KI_Benchmarks'
for path in os.listdir(d):
    full_path = os.path.join(d, path)
    if os.path.isfile(full_path):
        fileListPath.append(full_path.split("\\")[0])
        fileListName.append(full_path.split("\\")[1])


tmpCounter = 0
for fileName in fileListName:
    print( "[%d] %s\r" %(tmpCounter, fileName))
    tmpCounter = tmpCounter + 1

#Userinput
choice = input("\n\rWelches Problem soll gelöst werden? [0 - " + str(tmpCounter-1) + " ]: ")

print("Es wurde gewählt", fileListName[int(choice)])


