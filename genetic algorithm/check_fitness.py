import os.path
import pickle
from simulator import Simulator
import numpy as np

class CheckFitness:
    def __init__(self, simulator):
        self.simulator = simulator

    def checkFitness(self, individual):
##        self.simulator.changeRoutes()
        print(simulator.getFitness1(individual))


f = open("GA1_individual.txt", "rb")
bestIndividual = pickle.load(f)
simulator = Simulator(1, 2, 3)
a = CheckFitness(simulator)
a.checkFitness(bestIndividual)
