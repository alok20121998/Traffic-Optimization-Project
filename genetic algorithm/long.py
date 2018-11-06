import array
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

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
        self.toolbox.register("evaluate", self.fitnessFunction)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

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

        CXPB, MUTPB = 0.5, 0.2
        
        fitnesses = self.fitnessFunction(pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        for generation in range(self.numGeneration):
            offspring = self.toolbox.select(pop, len(pop))
            offspring = list(map(self.toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
            for mutant in offspring:
                if random.random() < MUTPB:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values
                    
            fitnesses = self.fitnessFunction(offspring)
            for ind, fit in zip(offspring, fitnesses):
                ind.fitness.values = fit
                
            pop[:] = offspring
            fits = [ind.fitness.values[0] for ind in pop]

            length = len(pop)
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std = abs(sum2 / length - mean**2)**0.5
            
            print("  Min %s" % min(fits))
            print("  Max %s" % max(fits))
            print("  Avg %s" % mean)
            print("  Std %s" % std)
        self.population = pop
