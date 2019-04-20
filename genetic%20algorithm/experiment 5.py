from long import GA1
from short1 import GA2
from simulator import Simulator
import time
from deap import tools
import math
import copy
import os.path
import pickle
import numpy as np

class Controller:
    def __init__(self, params):
        self.params = params
        self.timeSteps = params["timeSteps"]
        self.paramsListGA1 = ["crossover", "mutate", "select", "populationGA1", "numGeneration1", "crossroads", "timeSteps", "numIndividuals1", "fitnessGA1", "simulator", "minLim", "maxLim"]
        self.paramsGA1 = dict((k, params[k]) for k in self.paramsListGA1 if k in params)
        self.paramsListGA2 = ["crossover", "mutate", "select", "numGeneration2", "crossroads", "numIndividuals2", "timeStep", "fitnessGA2", "simulator", "densities", "population", "minLim", "maxLim"]
        self.paramsGA2 = dict((k, params[k]) for k in self.paramsListGA2 if k in params)

    def addTimeStep(self, bestIndividuals):
        ga1 = GA1(self.paramsGA1)
        prevTimeSteps = (len(bestIndividuals[0])//self.paramsGA1["crossroads"])
        if (prevTimeSteps)<=self.timeSteps//2:
            newTimeSteps = prevTimeSteps*2
            self.paramsGA1["timeSteps"] = newTimeSteps
            for individual in bestIndividuals:
                individual+=individual
        else:
            newTimeSteps = self.timeSteps
            self.paramsGA1["timeSteps"] = newTimeSteps
            for individual in bestIndividuals:
                individual+=individual[len(individual)-(self.paramsGA1["crossroads"]*(newTimeSteps - prevTimeSteps)):len(individual)]
        ga1 = GA1(self.paramsGA1)
        newPopulation = ga1.makePopulation(bestIndividuals)
        del ga1
        return newPopulation

    def run1(self):
        timeStep = 1
        while timeStep<=self.timeSteps:
            self.paramsGA1["simulator"].clear()
            self.paramsGA1["timeSteps"] = timeStep
            ga1 = GA1(self.paramsGA1)
            bestIndividuals = ga1.run()
            newPopulation = self.addTimeStep(bestIndividuals)
            self.paramsGA1["populationGA1"] = newPopulation
            if timeStep<=self.timeSteps//2:
                timeStep*=2
            elif timeStep < self.timeSteps and timeStep > self.timeSteps//2:
                timeStep=self.timeSteps
            elif timeStep==self.timeSteps:
                break
        bestIndividual = newPopulation[0][0:self.params["crossroads"]]
        self.params["simulator"].clear()
        self.params["simulator"].setState(bestIndividual)
        fitness = 0
        for timeStep in range(self.params["timeSteps"]):
            population = []
            for individual in newPopulation:
                population.append(individual[timeStep*self.params["crossroads"]:(timeStep+1)*self.params["crossroads"]])
            print("Timtestep: " + str(timeStep))
            self.paramsGA2["densities"] = None
            self.paramsGA2["population"] = population
            ga2 = GA2(self.paramsGA2)
            best, bestIndividual = ga2.run()
            fitness+=best
            self.params["simulator"].setState(bestIndividual)
        print(fitness)
        self.params["simulator"].exit()
        return fitness
        
NUM_INDIVIDUALS = 50
LOW = 0
UP = 119

params = {"crossover": {"operator": tools.cxTwoPoint},
          "mutate": {"operator": tools.mutShuffleIndexes, "indpb": 0.1},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "populationGA1": None,
          "numGeneration1": 10,
          "numGeneration2": 3,
          "crossroads": 21,
          "timeSteps": 10,
          "numIndividuals1": NUM_INDIVIDUALS,
          "numIndividuals2": 10,
          "simulator": Simulator(10, 2, 3),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP}
controller = Controller(params)
print(controller.run1())
