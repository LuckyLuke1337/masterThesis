import main as SOMAATO
import statistics
from tabulate import tabulate


fitness = 0
parameters = [[0.1,2.1,0.11]]


for inputs in parameters:
    data=[["function", "mean", "stddev"]]
    for costFunction in range(1,31):
        mean = 0
        values = []

        for i in range(1,51):
            fitness = SOMAATO.main(*inputs, "test.dat", costFunction)
            mean += fitness
            values.append(fitness)
            
        data.append(["f"+str(costFunction), mean/51, statistics.stdev(values)])
        print("calculated ", costFunction, " of 30 ", end="\r")

    print("table for input values: ",inputs)
    print(tabulate(data,headers='firstrow',tablefmt='grid'))


    
    