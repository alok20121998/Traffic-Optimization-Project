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
        self.paramsListGA1 = ["crossover", "mutate", "select", "numGeneration1", "crossroads", "timeSteps", "numIndividuals1", "fitnessGA1", "simulator", "minLim", "maxLim"]
        self.paramsGA1 = dict((k, params[k]) for k in self.paramsListGA1 if k in params)
        self.paramsListGA2 = ["crossover", "mutate", "select", "numGeneration2", "crossroads", "numIndividuals2", "timeStep", "fitnessGA2", "simulator", "densities", "population", "minLim", "maxLim"]
        self.paramsGA2 = dict((k, params[k]) for k in self.paramsListGA2 if k in params)
        self.ga1 = GA1(self.paramsGA1)

    def run1(self):
        individual, score, improvement = self.ga1.run()
        f = open("GA1_individual.txt", "wb")
        pickle.dump(individual, f)
        f.close()
        self.params["simulator"].exit()
        
    def run2(self):
        self.ga1.run()
        self.params["simulator"].changeRoutes()
        print("\n\n\nGA2:")
        print("*"*40)
        for timeStep in range(self.timeSteps):
            print("*"*40)
            print("Time step: " + str(timeStep+1))
            self.paramsGA2["densities"] = self.ga1.getDensities(timeStep)
            self.paramsGA2["population"] = self.ga1.getTimings(timeStep)
            ga2 = GA2(self.paramsGA2)
            ga2.run()
            print("*"*40)
        self.params["simulator"].exit()

NUM_INDIVIDUALS = 40
LOW = 0
UP = 119

params = {"crossover": {"operator": tools.cxOnePoint},
          "mutate": {"operator": tools.mutShuffleIndexes, "indpb": 0.1},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "populationGA1": None,
          "numGeneration1": 1,
          "numGeneration2": 3,
          "crossroads": 5,
          "timeSteps": 2,
          "numIndividuals1": NUM_INDIVIDUALS,
          "numIndividuals2": 10,
          "simulator": Simulator(10, 2, 3),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP}
controller = Controller(params)
controller.run1()
