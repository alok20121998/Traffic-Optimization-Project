import array
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import math
import copy
from simulator import Simulator

class GA1:
    def __init__(self, params):
        self.crossover = copy.deepcopy(params["crossover"])
        self.mutate = copy.deepcopy(params["mutate"])
        self.select = copy.deepcopy(params["select"])
        self.population = params["populationGA1"]
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
        self.toolbox.register("mate", self.crossover["operator"])
        del self.crossover["operator"]
        self.toolbox.register("mutate", self.mutate["operator"])
        del self.mutate["operator"]
        self.toolbox.register("select", self.select["operator"])
        del self.select["operator"]
        self.toolbox.register("selectBest", tools.selBest)

    def fitnessFunction(self, population):
        self.simulator.clear()
        fitnesses = [(3, )]*self.numIndividuals
        signals = numpy.ndarray((self.numIndividuals, self.timeSteps, self.crossroads), dtype = numpy.uint8)
        for individual in range(self.numIndividuals):
            for timeStep in range(self.timeSteps):
                timings = population[individual][self.crossroads*timeStep:self.crossroads*(timeStep+1)]
                signals[individual][timeStep] = timings
        if self.fitness=="1":
            fitnesses = self.simulator.getFitness1(signals, rm = True)
        elif self.fitness=="2":
            fitnesses = self.simulator.getFitness2(signals, rm = True)
        for ind, fit in zip(population, fitnesses):
            print(ind, fit)
            ind.fitness.values = fit
        return fitnesses

    def getTimings(self, timeStep):
        signalTimings = self.toolbox.small_population(n=self.numIndividuals)
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

    def makePopulation(self, bestIndividuals):
        offspring = self.toolbox.population(n=self.numIndividuals)
        index = 0
        for child1 in bestIndividuals:
            for child2 in bestIndividuals:
                temp1 = child1.__deepcopy__({})
                temp2 = child2.__deepcopy__({})
                if(temp1==temp2):
                    offspring[index] = temp1
                    index+=1
                else:
                    params_crossover = copy.deepcopy(self.crossover)
                    params_crossover["ind1"] = temp1
                    params_crossover["ind2"] = temp2
                    self.toolbox.mate(**params_crossover)
                    del params_crossover
                    offspring[index] = temp1
                    offspring[index+1] = temp2
                    index+=2
                if (index>=len(offspring)-2):
                    break
            if (index>=len(offspring)-2):
                break
##        for mutant in offspring:
##            params_mutate = copy.deepcopy(self.mutate)
##            params_mutate["individual"] = mutant
##            self.toolbox.mutate(**params_mutate)
##            del params_mutate
        return offspring

    def selectIndividuals(self, pop):
        params_select = copy.deepcopy(self.select)
        params_select["individuals"] = pop
        bestIndividual = self.toolbox.selectBest(k = 1, individuals = pop)
        bestIndividuals = self.toolbox.select(**params_select)
        bestIndividuals[0] = bestIndividual[0]
        print("Selected individuals:")
        print(bestIndividuals)
        del params_select
        return bestIndividuals

    def printStats(self, worst, pop, generation):
        length = len(pop)
        fits = [ind.fitness.values[0] for ind in pop]
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        improvement = ((worst-min(fits))*100)/worst
        bestFitness = min(fits)

        print("-"*30)
        print("Generation %s statistics" % str(generation+1))
        print("          Min: %s" % min(fits))
        print("          Max: %s" % max(fits))
        print("          Avg: %s" % mean)
        print("          Std: %s" % std)
        print("  Improvement: %s" % improvement)
        print("-"*30)

    def removeDuplicates(self, pop):
        toRemove = []
        for i in range(len(pop)):
            for j in range(len(pop)):
                if i!=j and i not in toRemove and j not in toRemove:
                    matches = len([a for a, b in zip(pop[i], pop[j]) if a == b])
                    if (matches*100)/(self.crossroads*self.timeSteps)>70:
                        toRemove.append(j)
        toRemove.sort(reverse = True)
        print(toRemove)
        for j in range(len(toRemove)):
            del pop[toRemove[j]]
        return pop

    def run(self):
        if self.population is None:
            pop = self.toolbox.population(n=self.numIndividuals)
        else:
            pop = self.population

        print("Generation 1")
        fitnesses = self.fitnessFunction(pop)

        worst = min([ind.fitness.values[0] for ind in pop])
        bestFitness = 0
        bestIndividuals = None
        
        for generation in range(self.numGeneration):
            self.printStats(worst, pop, generation)
##            pop = self.removeDuplicates(pop)
            bestIndividuals = self.selectIndividuals(pop)
            if (generation==self.numGeneration-1):
                break
            offspring = self.makePopulation(bestIndividuals)
            print("Generation " + str(generation+2))
            fitnesses = self.fitnessFunction(offspring)
            pop[:] = offspring
            fits = [ind.fitness.values[0] for ind in pop]
        
        self.population = pop
        return bestFitness, (worst - bestFitness)*100/worst, bestIndividuals
