import array
import random
from long import GA1
import numpy
import math
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import copy

class GA2:
    def __init__(self, params):
        self.crossover = copy.deepcopy(params["crossover"])
        self.mutate = copy.deepcopy(params["mutate"])
        self.select = copy.deepcopy(params["select"])
        self.numGeneration = params["numGeneration2"]
        self.densities = params["densities"]
        self.population = params["population"]
        self.crossroads = params["crossroads"]
        minLim = params["minLim"]
        maxLim = params["maxLim"]
        self.numIndividuals = params["numIndividuals2"]
        self.simulator = params["simulator"]
        self.fitness = params["fitnessGA2"]
        self.simulator.useSave = True
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()

        # Attribute generator
        self.toolbox.register("random", random.randint, minLim, maxLim)

        # Structure initializers
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.random, self.crossroads)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.fitnessFunction)
        self.toolbox.register("mate", self.crossover["operator"])
        del self.crossover["operator"]
        self.toolbox.register("mutate", self.mutate["operator"])
        del self.mutate["operator"]
        self.toolbox.register("select", self.select["operator"])
        del self.select["operator"]

    def fitnessFunction(self, population):
        fitnesses = [(3, )]*self.numIndividuals
        signals = numpy.ndarray((self.numIndividuals, 1, self.crossroads), dtype = numpy.uint8)
        for individual in range(self.numIndividuals):
            for timeStep in range(1):
                timings = population[individual][self.crossroads*timeStep:self.crossroads*(timeStep+1)]
                signals[individual][timeStep] = timings
        if self.fitness=="1":
            fitnesses = self.simulator.getFitness1(signals)
        elif self.fitness=="2":
            fitnesses = self.simulator.getFitness2(signals)
        elif self.fitness=="3":
            fitnesses = self.simulator.getFitness3(signals, self.densities)
        return fitnesses

    def run(self):
        pop = self.toolbox.population(n=self.numIndividuals)
        if self.population is not None:
            for i in range(min(len(self.population), self.numIndividuals)):
                for j in range(min(self.crossroads, len(self.population[i]))):
                    pop[i][j] = self.population[i][j]

##        print("Generation 1")
        fitnesses = self.fitnessFunction(pop)
        for ind, fit in zip(pop, fitnesses):
##            print(ind, fit)
            ind.fitness.values = fit

        worst = min([ind.fitness.values[0] for ind in pop])
        bestFitness = 0
        worstFitness = 0
        bestIndividual = None
        
        for generation in range(self.numGeneration):
            length = len(pop)
            fits = [ind.fitness.values[0] for ind in pop]
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std = abs(sum2 / length - mean**2)**0.5
            improvement = ((worst-min(fits))*100)/worst
            bestFitness = min(fits)
            worstFitness = max(fits)
            
            print("-"*30)
            print("Generation %s statistics" % str(generation+1))
            print("          Min: %s" % min(fits))
            print("          Max: %s" % max(fits))
            print("          Avg: %s" % mean)
            print("          Std: %s" % std)
            print("  Improvement: %s" % improvement)
            print("-"*30)
            params_select = copy.deepcopy(self.select)
            params_select["individuals"] = pop
            bestIndividuals = self.toolbox.select(**params_select)
##            print("Selected individuals:")
##            print(bestIndividuals)
            bestIndividual = bestIndividuals[0]
            del params_select
            if (generation==self.numGeneration-1):
                break
            offspring = pop.copy()
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
##            for mutant in offspring:
##                params_mutate = copy.deepcopy(self.mutate)
##                params_mutate["individual"] = mutant
##                self.toolbox.mutate(**params_mutate)
##                del params_mutate

##            print("Generation " + str(generation+2))
            fitnesses = self.fitnessFunction(offspring)
            for ind, fit in zip(offspring, fitnesses):
##                print(ind, fit)
                ind.fitness.values = fit
                
            pop[:] = offspring
            fits = [ind.fitness.values[0] for ind in pop]
        return bestFitness, (worstFitness - bestFitness)*100/worstFitness, bestIndividual
