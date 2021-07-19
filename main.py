
import sys
import numpy as np
import re
import startProgramm as start
import simplex
import os
#Lösung überprüft mit:
#http://simplex.tode.cz/en/ 

#Eigenes Github-Repo:
#https://github.com/Itzuko/HSHL_KI_LP


start.start()
start.showKIProblems()
usersChoice = start.getUserInput()
simplex.startSimplex(usersChoice)
print("----------------------------")
choice = input(
    "\n\rRun again? (y/n)\n")
choice = choice.lower()
if(choice == 'y'):
    def clear(): return os.system('cls')
    clear()
    os.execv(sys.executable, ['python'] + sys.argv)
    #os.system("python main.py")
    print("Restarting...")
    exit()
else:
    input("Press ENTER to exit")

