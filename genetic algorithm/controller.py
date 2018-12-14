from long import GA1
from short1 import GA2
from simulator import Simulator
import time

class Controller:
    def __init__(self, params):
        self.timeSteps = params["timeSteps"]
        self.paramsListGA1 = ["numGeneration1", "crossroads", "timeSteps", "numIndividuals1", "fitnessGA1", "simulator", "minLim", "maxLim"]
        self.paramsGA1 = dict((k, params[k]) for k in self.paramsListGA1 if k in params)
        self.paramsListGA2 = ["numGeneration2", "crossroads", "numIndividuals2", "timeStep", "fitnessGA2", "simulator", "densities", "population", "minLim", "maxLim"]
        self.paramsGA2 = dict((k, params[k]) for k in self.paramsListGA2 if k in params)
        self.ga1 = GA1(self.paramsGA1)

    def run(self):
        self.ga1.run()
        for timeStep in range(self.timeSteps):
            self.paramsGA2["timeStep"] = timeStep
            self.paramsGA2["densities"] = self.ga1.getDensities(timeStep)
            self.paramsGA2["population"] = self.ga1.getTimings(timeStep)
            ga2 = GA2(self.paramsGA2)
            ga2.run()

start = time.time()
params = {"numGeneration1": 10,
          "numGeneration2": 2,
          "crossroads": 21,
          "timeSteps": 10,
          "numIndividuals1": 40,
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
