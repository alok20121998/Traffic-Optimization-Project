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

class Simulator:
    def __init__(self, stepDuration, areaOptimized, areaCalculated):
        self.stepDuration = stepDuration
        self.areaOptimized = areaOptimized
        self.areaCalculated = areaCalculated
        self.timings = None
        self.fitnesses = None
        self.timeStepNum = 0
        self.sshClient = self.openConnection("40.117.86.130", 22, "tensortraffic", "GAUserAlok1!")

    def openConnection(self, hostname, port, username, password):
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.load_system_host_keys()
        sshClient.connect(hostname, port, username, password)
        return sshClient

    def exit(self):
        self.sshClient.exec_command("exit")

##Method 3: Use a virtual machine provided by Dr. Pawel Gora
    def requestStats3(self, i):
        time.sleep(random.randint(1, 3))
        timings = [int(j) for j in self.timings[i].tolist()]
        request = r'TSF1/TSF1/SingleSimulation.exe '
        for timing in timings:
            request = request + (str(timing) + " ")
        request = request + ("end_"+str(self.timeStepNum%2)+"_"+str(i)+".txt")
        request = request + (" end_"+str((self.timeStepNum+1)%2)+"_"+str(i)+".txt")

        stdin, stdout, stderr = self.sshClient.exec_command(request)
        time.sleep(1)
        stdout.channel.recv_exit_status()
        result = stdout.read()
        print("Individual" + str(i+1) + " Total waiting time: " + str(result))

        self.fitnesses[i] = (self.fitnesses[i][0]+int(result), )

## Method 2: locally run modified version of TSF
    def requestStats2(self, i):
        timings = [int(j) for j in self.timings[i].tolist()]
        request = [r'C:\Users\alok\Downloads\projects\project\traffic-signal-optimization\genetic algorithm\ForAlok'+str(i%4+1)+'\SingleSimulation.exe']
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
        N_JOBS = 10
        Parallel(n_jobs=N_JOBS, require='sharedmem')(delayed(self.requestStats3)(i) for i in range(number))

    def getFitness1(self, population):
        self.fitnesses = [(0,)]*population.shape[0]
        for timeStep in range(population.shape[1]):
            print("Time step: " + str(timeStep+1))
            self.timings = np.ndarray((population.shape[0], population.shape[2]))
            for i in range(population.shape[0]):
                self.timings[i] = population[i, timeStep]
            self.requestMany(population.shape[0])
            self.timeStepNum+=1
            print("\n")
        for i in range(population.shape[0]):
            rm_file1 = "rm end_0_"+str(i)+".txt"
            rm_file2 = "rm end_1_"+str(i)+".txt"
            self.sshClient.exec_command("cd")
            self.sshClient.exec_command(rm_file1)
            self.sshClient.exec_command(rm_file2)

        return self.fitnesses.copy()

    def getFitness2(self, population):
        self.fitnesses = [(0,)]*population.shape[0]
        self.timeStepNum = 0
        for timeStep in range(population.shape[1]):
            self.timings = np.ndarray((population.shape[0], population.shape[2]))
            for i in range(population.shape[0]):
                self.timings[i] = population[i, timeStep]
            self.requestMany(population.shape[0])
            self.timeStepNum+=1
        return self.fitnesses.copy()

    def getFitness3(self, population, densities):
        fitness = []
        for timing in timings:
            result = self.requestStats(timing.tolist())
            fitness+=result
            print(fitness)
        return fitness
