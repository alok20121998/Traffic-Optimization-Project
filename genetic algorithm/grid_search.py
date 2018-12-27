from long import GA1
from short1 import GA2
from simulator import Simulator
import time
from deap import tools

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
        del ga1
        return fitness

crossovers = []
mutations = []
selections = []
bestCombination = {}
bestFitness = 99999
combinations = []
controller = Controller()
for combination in combinations:
    params = {"crossover": combination["crossover"],
              "mutate": combination["mutate"],
              "select": combination["select"],
              "numGeneration1": 3,
              "numGeneration2": 2,
              "crossroads": 21,
              "timeSteps": 3,
              "numIndividuals1": 10,
              "numIndividuals2": 40,
              "simulator": Simulator(10, 2, 3),
              "fitnessGA1": "1",
              "fitnessGA2": "1",
              "minLim": 10,
              "maxLim": 119}
    fitness = controller.run(params)
    del params
    if (fitness<bestFitness):
        bestFitness = fitness
        bestCombination = combination
print(bestCombination)

