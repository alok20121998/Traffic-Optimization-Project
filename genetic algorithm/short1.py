import array
import random
from long import GA1
import numpy
import math
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
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
        self.toolbox.register("select", tools.selBest)

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
        random.seed(64)
        pop = self.population

        CXPB, MUTPB = 0.5, 0.2
        
        fitnesses = self.fitnessFunction(pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
            
        for generation in range(self.numGeneration):
            length = len(pop)
            fits = [ind.fitness.values[0] for ind in pop]
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std = abs(sum2 / length - mean**2)**0.5
            
            print("  Min %s" % min(fits))
            print("  Max %s" % max(fits))
            print("  Avg %s" % mean)
            print("  Std %s" % std)
            
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
                    
            fitnesses = self.fitnessFunction(offspring)
            for ind, fit in zip(offspring, fitnesses):
                ind.fitness.values = fit
                
            pop[:] = offspring
            fits = [ind.fitness.values[0] for ind in pop]

