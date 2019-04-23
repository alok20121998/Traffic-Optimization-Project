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

class Simulator:
    def __init__(self, stepDuration, areaOptimized, areaCalculated):
        self.stepDuration = stepDuration
        self.areaOptimized = areaOptimized
        self.areaCalculated = areaCalculated
        self.timings = None
        self.fitnesses = None
        self.timeStepNum = 0
        self.savingState = False
        self.useSave = False
        self.previousSave = 0
        self.previousSave2 = 0
        self.sshClient = self.openConnection("35.178.166.231", 22, "ubuntu", paramiko.RSAKey.from_private_key_file(r"alokprivatekey.pem"))
        self.TSF_instances = 9

    def openConnection(self, hostname, port, username, key):
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.load_system_host_keys()
        sshClient.connect(hostname, port, username, pkey = key)
        return sshClient

    def exit(self):
        self.clear()
        self.sshClient.exec_command("exit")
        pass

    def setState(self, individual):
        self.savingState = True
        self.timings[0] = individual
        self.requestStats3(0)
        self.savingState = False
        self.previousSave = (self.previousSave + 1)%2

    def clear(self):
        self.sshClient.exec_command("find . -type f -name end_\* -exec rm {} \;")
        self.sshClient.exec_command("find . -type f -name saved_state_\* -exec rm {} \;")
        if os.path.exists("saved_state_2_1.txt"):
            os.remove("saved_state_2_1.txt")
        if os.path.exists("saved_state_2_0.txt"):
            os.remove("saved_state_2_0.txt")

    def changeRoutes(self):
        pass

    def getPositions(self, timings):
        request = [r'.\TSF_1'+'\SingleSimulation.exe']
        positionLocation = r'.\TSF_1\temp3_'
        for timing in timings:
            request.append(str(timing))
            positionLocation+=str(timing)+"_"
        positionLocation+="saved_state_2_"+str(self.previousSave2)+"_txt_"
        positionLocation+="saved_state_2_"+str((self.previousSave2+1)%2)+"_txt"
        positionLocation+="_temp3"
        request.append("saved_state_2_"+str(self.previousSave2)+".txt")
        request.append("saved_state_2_"+str((self.previousSave2+1)%2)+".txt")
        self.previousSave2 = (self.previousSave2 + 1)%2
        request.append("temp3")
        result = subprocess.Popen(request, stdout=subprocess.PIPE).communicate()[0]
        positions = {}
        with open(positionLocation+"//cars119.csv", 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                positions[row[0]] = [row[2], row[3]]
        shutil.rmtree(positionLocation)
        return positions

    def setTimeInterval(self, intervalSize):
        pass

##Method 3: Use a virtual machine provided by Dr. Pawel Gora
    def requestStats3(self, i):
        time.sleep(random.randint(1, 3))
        timings = [int(j) for j in self.timings[i].tolist()]
        request = r'TSF1/TSF1/SingleSimulation.exe '
        for timing in timings:
            request = request + (str(timing) + " ")
        if self.savingState:
            request = request + ("saved_state_"+str(self.previousSave)+".txt")
            request = request + (" saved_state_"+str((self.previousSave+1)%2)+".txt")
        elif self.useSave:
            request = request + ("saved_state_"+str(self.previousSave)+".txt")
            request = request + (" end_"+str((self.timeStepNum+1)%2)+"_"+str(i)+".txt")
        else:
            request = request + ("end_"+str(self.timeStepNum%2)+"_"+str(i)+".txt")
            request = request + (" end_"+str((self.timeStepNum+1)%2)+"_"+str(i)+".txt")

        stdin, stdout, stderr = self.sshClient.exec_command(request)
        time.sleep(1)
        stdout.channel.recv_exit_status()
        result = stdout.read()
##        result = random.randint(1, 10)
        self.fitnesses[i] = (self.fitnesses[i][0]+int(result), )

## Method 2: locally run modified version of TSF
    def requestStats2(self, i):
        timings = [int(j) for j in self.timings[i].tolist()]
        request = [r'.\TSF'+str(i%self.TSF_instances+1)+'\SingleSimulation.exe']
        for timing in timings:
            request.append(str(timing))
        request.append("end_"+str(self.timeStepNum%2)+"_"+str(i)+".txt")
        request.append("end_"+str((self.timeStepNum+1)%2)+"_"+str(i)+".txt")
        
        result = subprocess.Popen(request, stdout=subprocess.PIPE).communicate()[0]
        result = int(result)
        self.fitnesses[i] = (self.fitnesses[i][0]+result, )

## Method 1: Use TSF microservice
    def requestStats1(self, i):
        username = 'pgora'
        password = 'Ghzf8ftb'
        address = 'http://13.81.247.156:25041/compute'
        timings = [int(i) for i in self.timings[i].tolist()]
        data = str(timings)
        headers = {'Content-type': 'application/json',}

        data = '{"settings": "' + str(data) + '"}'

        response = ''
        result = 0
        try:
            response = requests.post(address, headers=headers, data=data)
            text = str(response.content,"utf-8") if isinstance(response.content, bytes) else response.content
            print(text)
            result = int(json.loads(text)['score']) 
        except Exception as e:
            if(response.status_code==201):
                text = str(response.content,"utf-8") if isinstance(response.content, bytes) else response.content
                result = int(json.loads(text)['score'])
            else:
                print("error")
        self.fitnesses[i] = (self.fitnesses[i][0]+result, )

        
    def requestMany(self, number):
        N_JOBS = self.TSF_instances
        Parallel(n_jobs=N_JOBS, require='sharedmem')(delayed(self.requestStats3)(i) for i in range(number))

    def getFitness1(self, population, rm = True):
        if rm:
            self.sshClient.exec_command("find . -type f -name end_\* -exec rm {} \;")
        self.timeStepNum = 0
        self.fitnesses = [(0,)]*population.shape[0]
        for timeStep in range(population.shape[1]):
            self.timings = np.ndarray((population.shape[0], population.shape[2]))
            for i in range(population.shape[0]):
                self.timings[i] = population[i, timeStep]
            self.requestMany(population.shape[0])
            self.timeStepNum+=1
        self.timeStepNum = 0
        if rm:
            self.sshClient.exec_command("find . -type f -name end_\* -exec rm {} \;")
        return self.fitnesses.copy()

    def getFitness2(self, population, rm = False):
        self.fitnesses = [(0,)]*population.shape[0]
        self.timeStepNum = 0
        for timeStep in range(population.shape[1]):
            self.timings = np.ndarray((population.shape[0], population.shape[2]))
            for i in range(population.shape[0]):
                self.timings[i] = population[i, timeStep]
            self.requestMany(population.shape[0])
            self.timeStepNum+=1
        return self.fitnesses.copy()

    def getFitness3(self, population, densities, rm = False):
        fitness = []
        for timing in timings:
            result = self.requestStats(timing.tolist())
            fitness+=result
            print(fitness)
        return fitness
