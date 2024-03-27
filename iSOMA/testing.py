import main as iSOMA
import statistics
from tabulate import tabulate

fitness = 0
parameters = [[10, 0.1638, 8, 5, 15],[11, 0.1668, 7, 6, 15],[16, 0.1625, 7, 3, 14]]


for inputs in parameters:
    data=[["function", "mean", "stddev"]]
    for costFunction in range(1,31):
        mean = 0
        values =[]

        for i in range(1,51):
            fitness = iSOMA.main(*inputs, "test.dat", costFunction)
            mean += fitness 
            values.append(fitness)
            
        
        data.append(["f"+str(costFunction), mean/51, statistics.stdev(values)])
        print("calculated ", costFunction, " of 30 ", end="\r")

    print("table for input values: ",inputs)
    print(tabulate(data,headers='firstrow',tablefmt='grid'))


    
    