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
        self.ga1 = GA1(self.paramsGA1)

    def run1(self):
        self.params["simulator"].clear()
        individual, improvement = self.ga1.run()
        self.params["simulator"].exit()
        return score

NUM_INDIVIDUALS = 50
LOW = 0
UP = 119

params = {"crossover": {"operator": tools.cxTwoPoint},
          "mutate": {"operator": tools.mutShuffleIndexes, "indpb": 0.1},
          "select": {"operator": tools.selRoulette, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "populationGA1": None,
          "numGeneration1": 10,
          "numGeneration2": 3,
          "crossroads": 21,
          "timeSteps": 1,
          "numIndividuals1": NUM_INDIVIDUALS,
          "numIndividuals2": 10,
          "simulator": Simulator(10, 2, 3),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP}
controller = Controller(params)
print(controller.run1())
