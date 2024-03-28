import main as iSOMA
import statistics
from tabulate import tabulate

data=[["function", "mean", "stddev"]]
fitness = 0

for costFunction in range(1,31):
    mean = 0
    values =[]
    for i in range(1,51):
        fitness = iSOMA.main(10, 0.3, 10, 5, 15, "test.dat", costFunction)
        mean += fitness
        values.append(fitness)
    print(values)    
    data.append(["f"+str(costFunction), mean/51, statistics.stdev(values)])
    print("calculated ", costFunction, " of 30" )

print(tabulate(data,headers='firstrow',tablefmt='grid'))


    
    