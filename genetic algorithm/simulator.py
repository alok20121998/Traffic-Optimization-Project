import requests
import click
import json
import subprocess
from joblib import Parallel, delayed
import time
import numpy as np

class Simulator:
    def __init__(self, stepDuration, areaOptimized, areaCalculated):
        self.stepDuration = stepDuration
        self.areaOptimized = areaOptimized
        self.areaCalculated = areaCalculated
        self.timings = None
        self.fitnesses = None

    def requestStats(self, i):
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
            result = int(json.loads(text)['score']) 
        except Exception as e:
            if(response.status_code==201):
                text = str(response.content,"utf-8") if isinstance(response.content, bytes) else response.content
                result = int(json.loads(text)['score'])
            else:
                print("error")
        self.fitnesses[i] = (self.fitnesses[i][0]+result, )

        
    def requestMany(self, number):
        N_JOBS = 32
        Parallel(n_jobs=N_JOBS, require='sharedmem')(delayed(self.requestStats)(i) for i in range(number))

    def getFitness1(self, population):
        self.fitnesses = [(0,)]*population.shape[0]
        for timeStep in range(population.shape[1]):
            self.timings = np.ndarray((population.shape[0], population.shape[2]))
            for i in range(population.shape[0]):
                self.timings[i] = population[i, timeStep]
            self.requestMany(population.shape[0])
        return self.fitnesses.copy()

    def getFitness2(self, population):
        self.fitnesses = [(0,)]*population.shape[0]
        for timeStep in range(population.shape[1]):
            self.timings = np.ndarray((population.shape[0], population.shape[2]))
            for i in range(population.shape[0]):
                self.timings[i] = population[i, timeStep]
            self.requestMany(population.shape[0])
        return self.fitnesses.copy()

    def getFitness3(self, population, densities):
        fitness = []
        for timing in timings:
            result = self.requestStats(timing.tolist())
            fitness+=result
            print(fitness)
        return fitness
