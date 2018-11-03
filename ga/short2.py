import array
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

class GA2b:
    def __init__(self, densities):
        self.numGeneration = 40
        self.densities = densities
        self.crossroads = 10
        minLim = 10
        maxLim = 100
        self.numIndividuals = 10
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()

        # Attribute generator
        self.toolbox.register("random", random.randint, minLim, maxLim)

        # Structure initializers
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.random, 2*self.crossroads)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.evalOneMax)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def simulate(self, individual):
        pass

    def evalOneMax(self, individual):
##        signals = numpy.ndarray((self.crossroads, 2*self.timeSteps), dtype = numpy.uint8)
##        for crossroad in range(self.crossroads):
##            crossroadTimings = individual[2*crossroad*self.timeSteps:2*(crossroad+1)*self.timeSteps]
##            signals[crossroad] = crossroadTimings
##        outputDensities = selfs.simulate(signals)
##        difference = outputDensities - self.densities
##        fitness = numpy.linalg.norm(difference)
        return sum(individual),

    def run(self):
        random.seed(64)
        pop = self.toolbox.population(n=self.numIndividuals)
        print(pop[0])
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        
        pop, log = algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=self.numGeneration, 
                                       stats=stats, halloffame=hof, verbose=True)

a = GA1(12)
a.run()
