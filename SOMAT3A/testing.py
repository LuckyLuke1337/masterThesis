
import main as SOMAT3A
import statistics
from tabulate import tabulate

data=[["function", "mean", "stddev"]]
fitness = 0

for costFunction in range(1,31):
    mean = 0
    values =[]
    for i in range(1,51):
        fitness = SOMAT3A.main(10,4,10,45,"test.dat",costFunction)
        mean += fitness
        values.append(fitness)
        
    data.append(["f"+str(costFunction), mean/51, statistics.stdev(values)])
    print("calculated ", costFunction, " of 30" )

print(tabulate(data,headers='firstrow',tablefmt='grid'))

data=[["function", "mean", "stddev"]]
fitness = 0

for costFunction in range(1,31):
    mean = 0
    values =[]
    for i in range(1,51):
        fitness = SOMAT3A.main(2,1,12,26,"test.dat",costFunction)
        mean += fitness
        values.append(fitness)
        
    data.append(["f"+str(costFunction), mean/51, statistics.stdev(values)])
    print("calculated ", costFunction, " of 30" )

print(tabulate(data,headers='firstrow',tablefmt='grid'))

data=[["function", "mean", "stddev"]]
fitness = 0

for costFunction in range(1,31):
    mean = 0
    values =[]
    for i in range(1,51):
        fitness = SOMAT3A.main(5,2,9,22,"test.dat",costFunction)
        mean += fitness
        values.append(fitness)
        
    data.append(["f"+str(costFunction), mean/51, statistics.stdev(values)])
    print("calculated ", costFunction, " of 30" )

print(tabulate(data,headers='firstrow',tablefmt='grid'))

data=[["function", "mean", "stddev"]]
fitness = 0

for costFunction in range(1,31):
    mean = 0
    values =[]
    for i in range(1,51):
        fitness = SOMAT3A.main(5,4,4,18,"test.dat",costFunction)
        mean += fitness
        values.append(fitness)
        
    data.append(["f"+str(costFunction), mean/51, statistics.stdev(values)])
    print("calculated ", costFunction, " of 30" )

print(tabulate(data,headers='firstrow',tablefmt='grid'))




