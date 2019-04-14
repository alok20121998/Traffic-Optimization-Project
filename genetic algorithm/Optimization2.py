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
        self.paramsListGA2 = ["crossover", "mutate", "select", "populationGA2", "numGeneration2", "crossroads", "numIndividuals2", "fitnessGA2", "simulator", "densities", "minLim", "maxLim"]
        self.paramsGA2 = dict((k, params[k]) for k in self.paramsListGA2 if k in params)

    def run1(self):
        newPopulation = self.params["populationGA2"]
        bestIndividual = newPopulation[0][0:self.params["crossroads"]]
        self.params["simulator"].clear()
        self.params["simulator"].setState(bestIndividual)
        fitness = 0
        for timeStep in range(self.params["timeSteps"]):
            population = []
            for individual in newPopulation:
                population.append(individual[timeStep*self.params["crossroads"]:(timeStep+1)*self.params["crossroads"]])
            print("Timtestep: " + str(timeStep))
            self.paramsGA2["population"] = population
            ga2 = GA2(self.paramsGA2)
            best, bestIndividual = ga2.run()
            fitness+=best
            self.params["simulator"].setState(bestIndividual)
        print(fitness)
        self.params["simulator"].exit()
        return fitness

##Sample params
##params = {"numGeneration1": 10,
##          "timeSteps": 10,
##          "numIndividuals1": 50,
##          "populationGA2:" obtained from optimzation1}
def optimization2(params):
    NUM_INDIVIDUALS = params["numIndividuals2"]
    preDefinedParams = {"crossover": {"operator": tools.cxTwoPoint},
                        "mutate": {"operator": tools.mutShuffleIndexes,"indpb": 0.1},
                        "select": {"operator": tools.selRoulette, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
                        "crossroads": 21,
                        "densities": None,
                        "simulator": Simulator(10, 2, 3),
                        "fitnessGA2": "1",
                        "minLim": 0,
                        "maxLim": 119}
                        
    controller = Controller({**params, **preDefinedParams})
    return controller.run1()
