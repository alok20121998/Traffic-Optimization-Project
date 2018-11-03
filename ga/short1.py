import array
import random
from long import GA1
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

class GA2:
    def __init__(self, params):
        self.numGeneration = params["numGeneration2"]
        self.densities = params["densities"]
        self.population = params["population"]
        self.crossroads = params["crossroads"]
        self.timeStep = params["timeStep"]
        minLim = params["minLim"]
        maxLim = params["maxLim"]
        self.numIndividuals = params["numIndividuals2"]
        self.simulator = params["simulator"]
        self.fitness = params["fitnessGA2"]
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()

        # Attribute generator
        self.toolbox.register("random", random.randint, minLim, maxLim)

        # Structure initializers
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.random, self.crossroads)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.fitnessFunction)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def fitnessFunction(self, individual):
        signals = numpy.ndarray((1, self.crossroads), dtype = numpy.uint8)
        signals[0] = individual[0:self.crossroads]
        if self.fitness=="1":
            self.simulator.getFitness1(signals)
        elif self.fitness=="2":
            self.simulator.getFitness2(signals)
        elif self.fitness=="3":
            self.simulator.getFitness3(signals, self.densities)
        return sum(individual),

    def run(self):
        random.seed(64)
        pop = self.population
        print(pop)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        
        pop, log = algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=self.numGeneration, 
                                       stats=stats, halloffame=hof, verbose=True)

