import random
import numpy as np
import cec2017.functions as functions


# libaries to work with arguments:
import argparse
import logging
import sys

def main(gap, pathLength, step, adaptivePrt, DATFILE, function):

    # Define parameters
    NP = 25 
    dimension = 30
    MAX_ITERATION = 10000*dimension

    # Parameters to be ptimized
    # gap = 7
    # pathLength = 3.0
    # step = 0.33
    # adaptivePrt = 1

    testFunction = functions.all_functions[function-1]
    print(testFunction)



    def roulette(options, fitnesses):
    # Implement roulette wheel selection based on fitnesses
        totalFitness = sum(fitnesses)
        probs = [f / totalFitness for f in fitnesses]
        selectionPoint = random.uniform(0, 1)
        currentProb = 0
        for i, prob in enumerate(probs):
            currentProb += prob
            if currentProb >= selectionPoint:
                return options[i]

    class Individual:
        def __init__(self, position, strategy, prt):
            self.position = position
            self.strategy = strategy
            self.prt = prt
            self.fitness = None  # Initialize fitness as None
            self.bestFitness = None  # Store the best fitness achieved
            self.counter = 0  # Counter for stagnation

        def updateFitness(self, fitnessFunction):
            self.fitness = fitnessFunction([self.position])[0]
            self.bestFitness = max(self.bestFitness or -float('inf'), self.fitness)

        def migrate(self, leader, prtVector):
            newPosition = []
            for i in range(dimension):
                if prtVector[i] < self.prt:
                    newPosition.append(self.position[i] + step * (leader[i] - self.position[i]))
                else:
                    newPosition.append(self.position[i])
            return newPosition



  # Initialize population
  
    population = []
    for _ in range(NP):
        position = [random.uniform(-100, 100) for _ in range(dimension)]
        strategy = random.choice(["AllToOne", "AllToRandom", "AllToAll"])
        prt = 0.3 if adaptivePrt == 0 else random.choice([0.1, 0.3, 0.5, 0.7, 0.9])
        
        population.append(Individual(position, strategy, prt))

    for i in population:
        i.updateFitness(testFunction)


    for iteration in range(MAX_ITERATION):
        for i in range(NP):
            individual = population[i]

        # Select leader based on strategy
            if individual.strategy == "AllToOne":
                leader = min(population, key=lambda x: x.fitness)
            elif individual.strategy == "AllToRandom":
                leader = random.choice(population)
            else:
                leaderCandidates = [p for p in population if p != individual]
                leader = min(leaderCandidates, key=lambda x: x.fitness)

        # Migration
        for t in np.arange(0, pathLength + 1, step):
            prtVector = [random.uniform(0, 1) for _ in range(dimension)]
            newPosition = individual.migrate(leader.position, prtVector)

            # Evaluate new position
            newIndividual = Individual(newPosition, individual.strategy, individual.prt)
            newIndividual.updateFitness(testFunction)

            # Update population if improvement
            if newIndividual.fitness < individual.fitness:
                population[i] = newIndividual

        # Adaptive strategy & prt update
        if individual.fitness >= individual.bestFitness:
            individual.counter += 1
            if individual.counter > gap:
                # print("changing strategy to:")
                individual.counter = 0
                individual.prt = roulette([0.1, 0.3, 0.5, 0.7, 0.9], [individual.fitness] * 5)
                individual.strategy = roulette(["AllToOne", "AllToRandom", "AllToAll"], [individual.fitness] * 3)
                # print(individual.prt, individual.strategy)

        
        bestIndividual = min(population, key=lambda x: x.fitness)
        # print(f"Best individual position: {bestIndividual.position}")
        # print(f"Best fitness: {bestIndividual.fitness}")

    with open(DATFILE, 'w') as f:
	    f.write(str(bestIndividual))

    return(bestIndividual)


if __name__ == "__main__":

   #
    with open('args.txt', 'w') as f:
	    f.write(str(sys.argv))

    ap = argparse.ArgumentParser(description='Feature Selection using SOMA')
    ap.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    ap.add_argument('--gap', dest='gap', type=int, required=True, help='Gap')
    ap.add_argument('--pathLenght', dest='pathLenght', type=float, required=True, help='Path lenght')
    ap.add_argument('--step', dest='step', type=float, required=True, help='Step size')
    ap.add_argument('--adaptivePrt', dest='adaptivePrt', type=int, required=True, help='Adaptive prt enablement')
    ap.add_argument('--function', dest='function', type=int, required=True, help='Test function')
    ap.add_argument('--datfile', dest='datfile', type=str, required=True, help='File where it will be save the score (result)')
    args = ap.parse_args()
    logging.debug(args)
    
    main(args.gap, args.pathLenght, args.step, args.adaptivePrt, args.datfile, args.function)