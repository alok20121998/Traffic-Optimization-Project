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
    request = [r'.\TSF_2'+'\SingleSimulation.exe']
    for timing in timings:
        request.append(str(timing))
    request.append("temp1.txt")
    request.append("temp2.txt")
    request.append("temp3")
    result = subprocess.Popen(request, stdout=subprocess.PIPE).communicate()[0]
    positions = {}
    with open(r'C:\Users\alok\Downloads\projects\project\traffic-signal-optimization\genetic%20algorithm\TSF_2\temp3_10_10_10_10_10_10_10_10_10_10_10_10_10_10_10_10_10_10_10_10_10_temp1_txt_temp2_txt_temp3\cars119.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            positions[row[0]] = [row[2], row[3]]
    return positions

print(getPositions([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]))
