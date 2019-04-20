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
        self.paramsListGA2 = ["crossover", "mutate", "select", "numGeneration2", "crossroads", "numIndividuals2", "timeStep", "fitnessGA2", "simulator", "densities", "population", "minLim", "maxLim"]
        self.paramsGA2 = dict((k, params[k]) for k in self.paramsListGA2 if k in params)
        
    def run2(self):
        timings = []
        self.params["simulator"].clear()
        fitness = 0
        for timeStep in range(self.params["timeSteps"]):
            print("Timtestep: " + str(timeStep))
            self.paramsGA2["densities"] = None
            self.paramsGA2["population"] = None
            ga2 = GA2(self.paramsGA2)
            best, population = ga2.run()
            timings.append(population[0])
            fitness+=best
            self.params["simulator"].setState(population)
            print(fitness)
            print(timings)
        print(fitness)
        print(timings)
        self.params["simulator"].exit()
        return ((worstFitness-bestFitness)/worstFitness)*100

NUM_INDIVIDUALS = 50
LOW = 0
UP = 119

params = {"crossover": {"operator": tools.cxTwoPoint},
          "mutate": {"operator": tools.mutShuffleIndexes, "indpb": 0.1},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "numGeneration1": 1,
          "numGeneration2": 10,
          "crossroads": 21,
          "timeSteps": 10,
          "numIndividuals1": 20,
          "numIndividuals2": NUM_INDIVIDUALS,
          "simulator": Simulator(10, 2, 3),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP}
controller = Controller(params)
print(controller.run2())
