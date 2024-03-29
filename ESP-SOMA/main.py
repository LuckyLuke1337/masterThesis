import random
import numpy as np
import cec2017.functions as functions

# Define parameters
NP = 10 # Number of individuals in the population
D = 10# Dimension of the solution space
MAX_ITERATION = 10000000# Maximum number of iterations

# Parameters to be ptimized
gap = 20
pathLength = 3.0
step = 0.31
adaptivePrt = 1

testFunction = functions.f15



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
    # Update best fitness if necessary
    self.bestFitness = max(self.bestFitness or -float('inf'), self.fitness)

  def migrate(self, leader, prtVector):
    newPosition = []
    for i in range(D):
      if prtVector[i] < self.prt:
        newPosition.append(self.position[i] + step * (leader[i] - self.position[i]))
      else:
        newPosition.append(self.position[i])
    return newPosition


def main():
  # Initialize population
    population = []
    for _ in range(NP):
        position = [random.uniform(-100, 100) for _ in range(D)]
        strategy = random.choice(["AllToOne", "AllToRandom", "AllToAll"])
        prt = 0.3 if adaptivePrt == 0 else random.choice([0.1, 0.3, 0.5, 0.7, 0.9])
        
        population.append(Individual(position, strategy, prt))

    for i in population:
        i.updateFitness(testFunction)

  # Main loop
    for iteration in range(MAX_ITERATION):
        for i in range(NP):
            individual = population[i]
        # Update fitness if not already done
        #   if individual.fitness is None:
            # individual.updateFitness(testFunction)

        # Select leader based on strategy
            if individual.strategy == "AllToOne":
                leader = max(population, key=lambda x: x.fitness)
            elif individual.strategy == "AllToRandom":
                leader = random.choice(population)
            else:
            

                leaderCandidates = [p for p in population if p != individual]
                leader = max(leaderCandidates, key=lambda x: x.fitness)

        # Migration
        for t in np.arange(0, pathLength + 1, step):
            prtVector = [random.uniform(0, 1) for _ in range(D)]
            newPosition = individual.migrate(leader.position, prtVector)

            # Evaluate new position (assuming your_fitnessFunction exists)
            newIndividual = Individual(newPosition, individual.strategy, individual.prt)
            newIndividual.updateFitness(testFunction)

            # Update population if improvement
            if newIndividual.fitness > individual.fitness:
                population[i] = newIndividual

        # Adaptive strategy & prt update
        if individual.fitness <= individual.bestFitness:
            individual.counter += 1
            if individual.counter > gap:
                print("changing strategy to:")
                individual.counter = 0
                individual.prt = roulette([0.1, 0.3, 0.5, 0.7, 0.9], [individual.fitness] * 5)
                individual.strategy = roulette(["AllToOne", "AllToRandom", "AllToAll"], [individual.fitness] * 3)
                print(individual.prt, individual.strategy)
        # Record best solution (implementation depends on your needs)
        # Record best solution (implementation depends on your needs)
        bestIndividual = max(population, key=lambda x: x.fitness)
        # print(f"Best individual position: {bestIndividual.position}")
        print(f"Best fitness: {bestIndividual.fitness}")


if __name__ == "__main__":
    main()