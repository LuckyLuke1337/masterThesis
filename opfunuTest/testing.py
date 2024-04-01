import main as SOMAT3A
import statistics
from tabulate import tabulate

import opfunu


costFunctions = opfunu.get_functions_based_classname("2017")

fitness = 0 
parameters = [[45,10,4,10]]


for inputs in parameters:
    data=[["function", "mean", "stddev"]]
    for costFunction in costFunctions:
        mean = 0
        values = []
        for i in range(1,51):
            fitness = SOMAT3A.main(*inputs, "test.dat", costFunction.__name__)
            mean += fitness
            values.append(fitness)
            
        data.append([str(costFunction.__name__), mean/51, statistics.stdev(values)])
        print("calculated ", costFunction, " of 30 ", end="\r")

    print("table for input values: ",inputs)
    print(tabulate(data,headers='firstrow',tablefmt='grid'))