import array
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

class GA1:
    def __init__(self, params):
        self.numGeneration = params["numGeneration1"]
        self.crossroads = params["crossroads"]
        self.timeSteps = params["timeSteps"]
        minLim = params["minLim"]
        maxLim = params["maxLim"]
        self.numIndividuals = params["numIndividuals1"]
        self.simulator = params["simulator"]
        self.fitness = params["fitnessGA1"]
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()

        # Attribute generator
        self.toolbox.register("random", random.randint, minLim, maxLim)

        # Structure initializers
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.random, self.crossroads*self.timeSteps)
        self.toolbox.register("small_individual", tools.initRepeat, creator.Individual, self.toolbox.random, self.crossroads)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.fitnessFunction)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def fitnessFunction(self, individual):
        signals = numpy.ndarray((self.timeSteps, self.crossroads), dtype = numpy.uint8)
        for timeStep in range(self.timeSteps):
            timings = individual[self.crossroads*timeStep:self.crossroads*(timeStep+1)]
            signals[timeStep] = timings
        if self.fitness=="1":
            self.simulator.getFitness1(signals)
        elif self.fitness=="2":
            self.simulator.getFitness2(signals)
        return sum(individual),

    def getTimings(self, timeStep):
        signalTimings = []
        for individual in self.population:
            temp = individual[self.crossroads*timeStep:self.crossroads*(timeStep+1)]
            small_individual = self.toolbox.small_individual()
            for i in range(len(temp)):
                small_individual[i] = temp[i]
            signalTimings.append(small_individual)
        return signalTimings

    def getDensities(self, timeStep):
        pass    

    def run(self):
        random.seed(64)
        pop = self.toolbox.population(n=self.numIndividuals)
        self.population = pop
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        
        pop, log = algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=self.numGeneration, 
                                       stats=stats, halloffame=hof, verbose=True)
        self.population = pop
        print(self.population)
