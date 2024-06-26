import numpy as np
import cec2017.functions as functions
import cec2017.utils as utils

# libaries to work with arguments:
import argparse
import logging
import sys



def main(prt, pathLenght, step, DATFILE):
    #SOMA parameters
    # prt = 0.2
    # pathLenght = 2
    # step = 0.11
    migrations = 200
    pop_size = 10

    #general parameters
    dimension = 10
    min_s = [-500,-500, -500, -500, -500,-500,-500, -500, -500, -500]
    max_s = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500]

    class Individual:
        """Individual of the population. It holds parameters of the solution as well as the fitness of the solution."""
        def __init__(self, params, fitness):
            self.params = params
            self.fitness = fitness

        def __repr__(self):
            return '{} fitness: {}'.format(self.params, self.fitness)

    def evaluate(params, testFunction):
        """Returns fitness of the params"""
        return testFunction([params])[0]

    def bounded(params, min_s: list, max_s: list):
        """
        Returns bounded version of params
        All params that are outside of bounds (min_s, max_s) are reassigned by a random number within bounds
        """
        # return np.array([np.random.uniform(min_s[d], max_s[d])
        #         if params[d] < min_s[d] or params[d] > max_s[d] 
        #         else params[d] 
        #         for d in range(len(params))])

        out_of_bounds = np.any(params < min_s) | np.any(params > max_s)
        return np.where(out_of_bounds, np.random.uniform(min_s, max_s, size=params.shape), params)


    def generate_population(size, min_s, max_s, dimension, testFunction):
        def generate_individual():
            params = np.random.uniform(min_s, max_s, dimension)
            fitness = evaluate(params, testFunction)
            return Individual(params, fitness)
        return [generate_individual() for _ in range(size)]


    def generate_prt_vector(prt, dimension):
        return np.random.choice([0, 1], dimension, p=[prt, 1-prt])

    def get_leader(population):
        """Finds leader of the population by its fitness (the lower the better)."""
        # return np.anymin(population, key = lambda individual: individual.fitness[29])
        def calculate_fitness(individual):
        # Choose an aggregation method (e.g., mean, minimum, etc.)
            return np.mean(individual.fitness)  # Calculate the mean

        return min(population, key=calculate_fitness)

    def soma_all_to_one_rand(population, prt, pathLenght, step, migrations, min_s, max_s, dimension,testFunction):
        for generation in range(migrations):
            leading = np.random.choice(population)
            for individual in population:
                # print("individual:",individual)
                if individual is leading:
                    continue
                next_position = individual.params
                prt_vector = generate_prt_vector(prt, dimension)
                for t in np.arange(step, pathLenght, step):
                    current_position = individual.params + (leading.params - individual.params) * t * prt_vector
                    current_position = bounded(current_position, min_s, max_s)
                    # print("current position:", current_position)
                    fitness = evaluate(current_position, testFunction)

                    if np.any(fitness <= individual.fitness):
                        next_position = current_position
                        individual.fitness = fitness
                individual.params = next_position
        result = get_leader(population)
        return result.fitness

    # loop trought all functions
    # for i in functions.all_functions:
    #     population = generate_population(pop_size,min_s, max_s, dimension,i)
    #     result = soma_all_to_one_rand(population, prt, pathLenght, step, migrations, min_s, max_s, dimension,i)
    #     print("function: ",i, "result: ", result)

    population = generate_population(pop_size,min_s, max_s, dimension, functions.all_functions[functionIndex])
    result = soma_all_to_one_rand(population, prt, pathLenght, step, migrations, min_s, max_s, dimension,functions.all_functions[functionIndex])
    print(result)
    with open(DATFILE, 'w') as f:
	    f.write(str(result))


if __name__ == "__main__":
	# just check if args are ok
    # 
    with open('args.txt', 'w') as f:
	    f.write(str(sys.argv))

    # print("test")
    # functionIndex = 4
	# loading example arguments
    ap = argparse.ArgumentParser(description='Feature Selection using SOMA')
    ap.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	# 3 args to test values
	# ap.add_argument('--pop', dest='pop', type=int, required=True, help='Population size')
    ap.add_argument('--prt', dest='prt', type=float, required=True, help='Perturbation')
    ap.add_argument('--pathLenght', dest='pathLenght', type=float, required=True, help='Path lenght')
    ap.add_argument('--step', dest='step', type=float, required=True, help='Step size')
    ap.add_argument('--function', dest='function', type=int, required=True, help='Test function')
    
	# ap.add_argument('--fun', dest='testFunction', type=str, required=True, help='CEC2017 testfunction')
	# 1 arg file name to save and load fo value

    ap.add_argument('--datfile', dest='datfile', type=str, required=True, help='File where it will be save the score (result)')
    args = ap.parse_args()
    logging.debug(args)
    functionIndex = args.function - 1
    print(functions.all_functions[functionIndex])
    

    main(args.prt, args.pathLenght, args.step, args.datfile)
