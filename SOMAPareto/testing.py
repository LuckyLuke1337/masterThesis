import main as SOMAPareto
import statistics
from tabulate import tabulate


fitness = 0
parameters = [[5,0.7385,1.5394],[7,1,0.4547],[7,0.7643,1.8242]]


for inputs in parameters:
    data=[["function", "mean", "stddev"]]
    for costFunction in range(1,31):
        mean = 0
        values = []

        for i in range(1,51):
            fitness = SOMAPareto.main(*inputs, "test.dat", costFunction)
            mean += fitness
            values.append(fitness)
            
        data.append(["f"+str(costFunction), mean/51, statistics.stdev(values)])
        print("calculated ", costFunction, " of 30 ", end="\r")

    print("table for input values: ",inputs)
    print(tabulate(data,headers='firstrow',tablefmt='grid'))


    