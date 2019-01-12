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

toolbox = base.Toolbox()
toolbox.register("mate", tools.cxTwoPoint)
a = [1, 2, 3, 4]
b = [1, 2, 3, 4]
print(toolbox.mate(a, b))
print(a, b)
