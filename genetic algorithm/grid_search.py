from long import GA1
from short1 import GA2
from simulator import Simulator
import time
from deap import tools
import os.path
import pickle

class Controller:
    def __init__(self):
        pass

    def run(self, params):
        timeSteps = params["timeSteps"]
        paramsListGA1 = ["crossover", "mutate", "select", "numGeneration1", "crossroads", "timeSteps", "numIndividuals1", "fitnessGA1", "simulator", "minLim", "maxLim"]
        paramsGA1 = dict((k, params[k]) for k in paramsListGA1 if k in params)
        ga1 = GA1(paramsGA1)
        fitness = ga1.run()
        params["simulator"].exit()
        return fitness

crossovers = [{"operator": tools.cxOnePoint}, {"operator": tools.cxTwoPoint}, {"operator": tools.cxPartialyMatched}, {"operator": tools.cxOrdered}, {"operator": tools.cxUniform, "indpb":}, {"operator": tools.cxUniformPartialyMatched, "indpb":}, {"operator": tools.cxBlend, "alpha":}, {"operator": tools.cxSimulatedBinary, "eta":}, {"operator": tools.cxSimulatedBinaryBounded, "eta":, "low":, "up"}]
crossovers.append()
crossovers.append()
crossovers+=[()]
mutations = [{"operator": tools.mutGaussian, "}]
selections = []
combinations = []
for crossover in crossovers:
    for mutation in mutations:
        for selection in selections:
            combinations.append({"crossover":crossover, "mutation":mutation, "selection":selection})
controller = Controller()
simulator = Simulator(10, 2, 3)
if os.path.exists("grid_search_iterations_executed.txt"):
    f = open("grid_search_iterations_executed.txt", "r")
    startingCombination = f.read()+1
    f.close()
else:
    startingCombination = 0
if os.path.exists("best_combination.txt"):
    f = open("best_combination.txt", "r")
    bestCombination = pickle.load(f)
    bestFitness = bestCombination["fitness"]
else:
    bestCombination = {}
    bestFitness = 99999
    
for i in range(startingCombination, len(combinations)):
    params = {"crossover": combinations[i]["crossover"],
              "mutate": combinations[i]["mutate"],
              "select": combinations[i]["select"],
              "numGeneration1": 3,
              "numGeneration2": 2,
              "crossroads": 21,
              "timeSteps": 3,
              "numIndividuals1": 10,
              "numIndividuals2": 40,
              "simulator": simulator,
              "fitnessGA1": "1",
              "fitnessGA2": "1",
              "minLim": 10,
              "maxLim": 119}
    fitness = controller.run(params)
    combinations[i]["fitness"] = fitness
    if (fitness<bestFitness):
        bestFitness = fitness
        bestCombination = combinations[i]
        f = open("best_combination.txt", "w")
        pickle.dump(combinations[i], f)
        f.close()
        print(bestCombination)
    f = open("grid_search_iterations_executed.txt", "w")
    f.write(i)
    f.close()
    
print(bestCombination)

