import requests
import click
import json
import subprocess
from joblib import Parallel, delayed
import time
import numpy as np
import os
import paramiko
import time
import random
import csv

def getPositions(timings):
    previousSave2 = 0
    request = [r'.\TSF_2'+'\SingleSimulation.exe']
    positionLocation = r'C:\Users\alok\Downloads\projects\project\traffic-signal-optimization\genetic%20algorithm\TSF_2\temp3_'
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
    
    with open(positionLocation, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            positions[row[0]] = [row[2], row[3]]
    return positions
print(os.path.dirname("temp2.py"))

