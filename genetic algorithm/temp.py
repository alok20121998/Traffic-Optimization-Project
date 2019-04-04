from long import GA1
from short1 import GA2
from simulator import Simulator
import time
from deap import tools
import os.path
import pickle
import math

combination = {"crossover": {"operator": tools.cxOnePoint},
          "mutate": {"operator": tools.mutShuffleIndexes, "indpb": 0.1},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(10))}}
print(combination)
f = open("best_combination.txt", "wb")
pickle.dump(combination, f)
f.close()
f = open("best_combination.txt", "rb")
bestCombination = pickle.load(f)
print(bestCombination)
