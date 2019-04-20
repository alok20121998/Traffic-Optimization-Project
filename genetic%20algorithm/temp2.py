import requests
import click
import json
import subprocess
from joblib import Parallel, delayed
import time
import numpy as np
import os
import shutil
import paramiko
import time
import random
import csv

def getPositions(timings):
    previousSave2 = 0
    request = [r'.\ForAlok'+'\SingleSimulation.exe']
    positionLocation = r'.\ForAlok\temp3_'
    for timing in timings:
        request.append(str(timing))
        positionLocation+=str(timing)+"_"
    positionLocation+="saved_state_2_"+str(previousSave2)+"_txt_"
    positionLocation+="saved_state_2_"+str((previousSave2+1)%2)+"_txt"
    positionLocation+="_temp3"
    request.append("saved_state_2_"+str(previousSave2)+".txt")
    request.append("saved_state_2_"+str((previousSave2+1)%2)+".txt")
    previousSave2 = (previousSave2 + 1)%2
    request.append("temp3")
    result = subprocess.Popen(request, stdout=subprocess.PIPE).communicate()[0]
    positions = {}
    
    with open(positionLocation+"//cars119.csv", 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            positions[row[0]] = [row[2], row[3]]
    shutil.rmtree(positionLocation)
    return positions
getPositions([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])

