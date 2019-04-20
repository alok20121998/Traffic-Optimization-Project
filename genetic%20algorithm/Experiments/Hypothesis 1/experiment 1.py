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
        self.paramsGA1 = dict((k, params[k]) for k in self.paramsListGA1 if k in copy.deepcopy(params))
        self.paramsListGA2 = ["crossover", "mutate", "select", "numGeneration2", "crossroads", "numIndividuals2", "timeStep", "fitnessGA2", "simulator", "densities", "population", "minLim", "maxLim"]
        self.paramsGA2 = dict((k, params[k]) for k in self.paramsListGA2 if k in copy.deepcopy(params))
        self.ga1 = GA1(self.paramsGA1)

    def run1(self):
        individual, score = self.ga1.run()
        f = open("GA1_individual.txt", "wb")
        pickle.dump(individual, f)
        f.close()
        self.params["simulator"].exit()
        return score
        
NUM_INDIVIDUALS = 50
LOW = 0
UP = 119

params = {"crossover": {"operator": tools.cxTwoPoint},
          "mutate": {"operator": tools.mutShuffleIndexes, "indpb": 0.1},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "numGeneration1": 10,
          "numGeneration2": 3,
          "crossroads": 21,
          "timeSteps": 10,
          "numIndividuals1": NUM_INDIVIDUALS = 50,
          "numIndividuals2": 10,
          "simulator": Simulator(10, 2, 3),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP}
controller = Controller(params)
print(controller.run1())
