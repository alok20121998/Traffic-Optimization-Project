import array
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import math

from simulator import Simulator

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
        self.toolbox.register("small_population", tools.initRepeat, list, self.toolbox.small_individual)
        self.toolbox.register("evaluate", self.fitnessFunction)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
        self.toolbox.register("select", tools.selBest)

    def fitnessFunction(self, population):
        fitnesses = [(3, )]*self.numIndividuals
        signals = numpy.ndarray((self.numIndividuals, self.timeSteps, self.crossroads), dtype = numpy.uint8)
        for individual in range(self.numIndividuals):
            for timeStep in range(self.timeSteps):
                timings = population[individual][self.crossroads*timeStep:self.crossroads*(timeStep+1)]
                signals[individual][timeStep] = timings
        if self.fitness=="1":
            fitnesses = self.simulator.getFitness1(signals)
        elif self.fitness=="2":
            fitnesses = self.simulator.getFitness2(signals)
        return fitnesses

    def getTimings(self, timeStep):
        signalTimings = self.toolbox.small_population(n=self.numIndividuals)
        print(type(signalTimings))
        index = 0
        for individual in self.population:
            temp = individual[self.crossroads*timeStep:self.crossroads*(timeStep+1)]
            small_individual = self.toolbox.small_individual()
            for i in range(len(temp)):
                small_individual[i] = temp[i]
            signalTimings[index] = small_individual
            index+=1
        return signalTimings

    def getDensities(self, timeStep):
        pass

    def run(self):
        random.seed(64)
        pop = self.toolbox.population(n=self.numIndividuals)

        CXPB, MUTPB = 0.5, 0.2
        print("generation 1")
        fitnesses = self.fitnessFunction(pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        worst = min([ind.fitness.values[0] for ind in pop])
        best = 0
        
        for generation in range(self.numGeneration):
            length = len(pop)
            fits = [ind.fitness.values[0] for ind in pop]
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std = abs(sum2 / length - mean**2)**0.5

            if (generation==self.numGeneration-1):
                best = min(fits)
            print("-----------------------------------------------------------")
            print("Generation statistics")
            print("  Min %s" % min(fits))
            print("  Max %s" % max(fits))
            print("  Avg %s" % mean)
            print("  Std %s" % std)
            print("-----------------------------------------------------------")
            bestIndividuals = self.toolbox.select(pop, int(math.sqrt(len(pop))))
            offspring = self.toolbox.population(n=self.numIndividuals)
            index = 0

            for child1 in bestIndividuals:
                for child2 in bestIndividuals:
                    temp1 = child1.__deepcopy__({})
                    temp2 = child2.__deepcopy__({})
                    temp = self.toolbox.mate(temp1, temp2)
                    offspring[index] = temp1
                    index+=1
            for mutant in offspring:
                if random.random() < MUTPB:
                    self.toolbox.mutate(mutant)

            print("generation " + str(generation))
            fitnesses = self.fitnessFunction(offspring)
            for ind, fit in zip(offspring, fitnesses):
                ind.fitness.values = fit
                
            pop[:] = offspring
            fits = [ind.fitness.values[0] for ind in pop]

        print("improvement: " + str((worst-best)*100/best) + "%")
        
        self.population = pop
