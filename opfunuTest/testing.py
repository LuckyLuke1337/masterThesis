import main as SOMAT3A
import statistics
from tabulate import tabulate

import opfunu


costFunctions = opfunu.get_functions_based_classname("2017")


index = 0
fitness = 0 
parameters = [[23,6,3,10]]


for inputs in parameters:
    data=[["function", "mean", "stddev"]]
    for costFunction in costFunctions:
        mean = 0
        values = []
        for i in range(1,6):
            fitness = SOMAT3A.main(*inputs, "test.dat", costFunction.__name__)
            mean += fitness
            values.append(fitness)
            
        data.append([str(costFunction.__name__), mean/5, statistics.stdev(values)])
        index += 1
        print("calculated ", index, " of ", len(costFunctions), end="\r")

    print("table for input values: ",inputs)
    print(tabulate(data,headers='firstrow',tablefmt='grid'))