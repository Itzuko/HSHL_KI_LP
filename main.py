
import sys
import numpy as np
import re
import startProgramm as start
import simplex
#Lösung überprüft mit:
#http://simplex.tode.cz/en/ 

#Eigenes Github-Repo:
#https://github.com/Itzuko/HSHL_KI_LP

start.start()
start.showKIProblems()
usersChoice =  start.getUserInput()
simplex.startSimplex(usersChoice)