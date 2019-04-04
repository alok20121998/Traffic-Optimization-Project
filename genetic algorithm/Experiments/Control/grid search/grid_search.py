from long import GA1
from short1 import GA2
from simulator import Simulator
import time
from deap import tools
import os.path
import pickle
import math
from collections import Sequence
from itertools import repeat
import random
from GA_operators import *

class Controller:
    def __init__(self):
        pass

    def run(self, params):
        timeSteps = params["timeSteps"]
        paramsListGA1 = ["crossover", "mutate", "select", "numGeneration1", "crossroads", "timeSteps", "numIndividuals1", "fitnessGA1", "simulator", "minLim", "maxLim"]
        paramsGA1 = dict((k, params[k]) for k in paramsListGA1 if k in params)
        ga1 = GA1(paramsGA1)
        bestIndividual, score, improvement = ga1.run()
        params["simulator"].exit()
        return improvement

NUM_INDIVIDUALS = 40
LOW = 0
UP = 119

crossovers = [{"operator": tools.cxOnePoint},
              {"operator": tools.cxTwoPoint},
              {"operator": tools.cxUniform, "indpb":0.5},
              {"operator": cxSimulatedBinaryBounded, "eta": 1},
              {"operator": cxSimulatedBinaryBounded, "eta": 10},
              {"operator": cxSimulatedBinaryBounded, "eta": 100}]
mutations = [{"operator": mutGaussian, "mu": 60, "sigma": 50, "low": LOW, "up": UP, "indpb": 0.1},
             {"operator": mutPolynomialBounded, "eta": 1, "low": LOW, "up": UP, "indpb": 0.1},
             {"operator": mutPolynomialBounded, "eta": 10, "low": LOW, "up": UP, "indpb": 0.1},
             {"operator": mutPolynomialBounded, "eta": 100, "low": LOW, "up": UP, "indpb": 0.1},
             {"operator": tools.mutShuffleIndexes, "indpb": 0.1},
             {"operator": tools.mutUniformInt, "low": LOW, "up": UP, "indpb": 0.1}]
selections = [{"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
              {"operator": tools.selTournament, "k": int(math.sqrt(NUM_INDIVIDUALS//2)), "tournsize": 2*int(math.sqrt(NUM_INDIVIDUALS//2))},
              {"operator": tools.selStochasticUniversalSampling, "k": int(math.sqrt(NUM_INDIVIDUALS//2))}]
combinations = []
for crossover in crossovers:
    combinations.append({"crossover":crossover, "mutate":{"operator": tools.mutUniformInt, "low": LOW, "up": UP, "indpb": 0.1}, "select":{"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS/2))}})
for mutation in mutations:
    combinations.append({"crossover":{"operator": tools.cxTwoPoint}, "mutate":mutation, "select":{"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS/2))}})
for selection in selections:
    combinations.append({"crossover":{"operator": tools.cxTwoPoint}, "mutate":{"operator": tools.mutUniformInt, "low": LOW, "up": UP, "indpb": 0.1}, "select":selection})
controller = Controller()
simulator = Simulator(10, 2, 3)
if os.path.exists("grid_search_iterations_executed.txt"):
    f = open("grid_search_iterations_executed.txt", "rb")
    num = f.read()
    startingCombination = int(num)+1
    f.close()
else:
    startingCombination = 0
if os.path.exists("best_combination.txt"):
    f = open("best_combination.txt", "rb")
    bestCombination = pickle.load(f)
    bestImprovement = bestCombination["improvement"]
else:
    bestCombination = {}
    bestImprovement = 0
    
for i in range(startingCombination, len(combinations)):
    print(combinations[i])
    params = {"crossover": combinations[i]["crossover"],
              "mutate": combinations[i]["mutate"],
              "select": combinations[i]["select"],
              "numGeneration1": 3,
              "numGeneration2": 2,
              "crossroads": 21,
              "timeSteps": 3,
              "numIndividuals1": NUM_INDIVIDUALS,
              "numIndividuals2": 40,
              "simulator": simulator,
              "fitnessGA1": "1",
              "fitnessGA2": "1",
              "minLim": LOW,
              "maxLim": UP}
    improvement = controller.run(params)
    combinations[i]["improvement"] = improvement
    print(combinations[i])
    if (improvement>bestImprovement):
        bestImprovement = improvement
        bestCombination = combinations[i]
        f = open("best_combination.txt", "wb")
        pickle.dump(combinations[i], f)
        f.close()
    f = open("grid_search_iterations_executed.txt", "w")
    f.write(str(i))
    f.close()
    
print(bestCombination)
