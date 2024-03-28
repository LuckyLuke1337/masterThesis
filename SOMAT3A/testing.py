import main as SOMAT3A
import statistics
from tabulate import tabulate


fitness = 0
parameters = [[26,2,1,12],[22,5,2,9],[18,5,4,4]]


for inputs in parameters:
    data=[["function", "mean", "stddev"]]
    for costFunction in range(1,31):
        mean = 0
        values = []

        for i in range(1,51):
            fitness = SOMAT3A.main(*inputs, "test.dat", costFunction)
            mean += fitness
            values.append(fitness)
            
        data.append(["f"+str(costFunction), mean/51, statistics.stdev(values)])
        print("calculated ", costFunction, " of 30 ", end="\r")

    print("table for input values: ",inputs)
    print(tabulate(data,headers='firstrow',tablefmt='grid'))