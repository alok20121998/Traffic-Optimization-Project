from long import GA1
from short1 import GA2
from simulator import Simulator
import time
from deap import tools
import math

class Controller:
    def __init__(self, params):
        self.params = params
        self.timeSteps = params["timeSteps"]
        self.paramsListGA1 = ["crossover", "mutate", "select", "numGeneration1", "crossroads", "timeSteps", "numIndividuals1", "fitnessGA1", "simulator", "minLim", "maxLim"]
        self.paramsGA1 = dict((k, params[k]) for k in self.paramsListGA1 if k in params)
        self.paramsListGA2 = ["crossover", "mutate", "select", "numGeneration2", "crossroads", "numIndividuals2", "timeStep", "fitnessGA2", "simulator", "densities", "population", "minLim", "maxLim"]
        self.paramsGA2 = dict((k, params[k]) for k in self.paramsListGA2 if k in params)
        self.ga1 = GA1(self.paramsGA1)
        

    def run(self):
        self.ga1.run()
        self.params["simulator"].changeRoutes()
        for timeStep in range(self.timeSteps):
            self.paramsGA2["timeStep"] = timeStep
            self.paramsGA2["densities"] = self.ga1.getDensities(timeStep)
            self.paramsGA2["population"] = self.ga1.getTimings(timeStep)
            ga2 = GA2(self.paramsGA2)
            ga2.run()
        self.params["simulator"].exit()

start = time.time()
params = {"crossover": {"operator": tools.cxOnePoint},
          "mutate": {"operator": tools.mutShuffleIndexes, "indpb": 0.1},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(10))},
          "numGeneration1": 4,
          "numGeneration2": 4,
          "crossroads": 1,
          "timeSteps": 5,
          "numIndividuals1": 10,
          "numIndividuals2": 40,
          "simulator": Simulator(10, 2, 3),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": 10,
          "maxLim": 119}
controller = Controller(params)
controller.run()
end = time.time()
print(end-start)
