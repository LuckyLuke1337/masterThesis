# --- SOMA Simple Program --- Version: SOMA PARETO (V1.0) August 25, 2020 -
# ------ Written by: Quoc Bao DIEP ---  Email: diepquocbao@gmail.com   ----
# -----------  See more details at the end of this file  ------------------
import numpy


import opfunu

# libaries to work with arguments:
import argparse
import logging
import sys


def main(nJumps, T1, T2, DATFILE, function):
    dimension = 10
    # functionIndex = function - 1
    # CostFunction = functions.all_functions[functionIndex]

    functionID=function
    problem = getattr(opfunu.cec_based, functionID)(ndim=dimension)
                                                          # Number of dimensions of the problem
    # -------------- Control Parameters of SOMA -------------------------------
    # nJumps = 10                                                         # Assign values ​​to variables: Step, PRT, PathLength
    PopSize, Max_Migration, Max_FEs = 100, 100, dimension*10**4         # Assign values ​​to variables: PopSize, Max_Migration
    # -------------- The domain (search space) --------------------------------
    VarMin, VarMax = -100, 100   # for Schwefel's function.                   # Define the search range
    # %%%%%%%%%%%%%%      B E G I N    S O M A    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ------------- Create the initial Population -----------------------------
    pop = VarMin + numpy.random.rand(dimension, PopSize) * (VarMax - VarMin) # Create the initial Population
    # pop = pop.T
    # fitness = CostFunction(pop.T)-function*100   
    fitness = [] 
    for i in pop.T:
        fitness = numpy.append(fitness, problem.evaluate(i))
                                             # Evaluate the initial population
    FEs = PopSize                                                       # Count the number of function evaluations
    the_best_cost = min(fitness)                                        # Find the Global minimum fitness value
    # ---------------- SOMA MIGRATIONS ----------------------------------------
    C = numpy.around(PopSize * 0.04).astype(int)                        # Calculation of parameters A-C-D, please refer to the paper for more details
    A = numpy.around(PopSize * 0.20).astype(int)                        # Calculation of parameters A-C-D, please refer to the paper for more details
    D = numpy.around(PopSize * 0.16).astype(int)                        # Calculation of parameters A-C-D, please refer to the paper for more details
    Migration = 0                                                       # Assign values ​​to variables: Migration
    while FEs+nJumps <= Max_FEs:                                        # Terminate when reaching Max_FEs
        Migration = Migration + 1                                       # Increase Migration value
        # ------------ Control parameters -------------------------------------
        PRT = 0.50 + 0.45*numpy.cos(T1*numpy.pi*FEs/Max_FEs+numpy.pi)      # Update PRT and Step parameters
        Step = 0.35 - 0.15*numpy.cos(T2*numpy.pi*FEs/Max_FEs)              # Update PRT and Step parameters
        # ------------ Sort POP -----------------------------------------------
        pop_sort = numpy.append(fitness.reshape(1, PopSize),pop,axis=0) # Gather pop and fit into one
        pop_sort = pop_sort[:, pop_sort[0].argsort()]                   # Sort Pop according to the fitness values
        fitness = pop_sort[0,:]                                         # Split pop and fitness
        pop = pop_sort[1:,:]                                            # Split pop and fitness
        # ------------- Moving process ----------------------------------------
        Migrant_idx = numpy.random.choice(range(A,A+D),1)               # Migrant selection
        Migrant = pop[:, Migrant_idx].reshape(dimension, 1)             # Get the Migrant position (solution values) in the current population
        # ------------ Leader selection: k ------------------------------------
        Leader_idx = numpy.random.choice(range(C),1)                    # Leader selection
        Leader = pop[:, Leader_idx].reshape(dimension, 1)               # Get the Migrant position (solution values) in the current population
        offspring_path = numpy.empty([dimension, 0])                    # Create an empty path of offspring
        for move in range(nJumps):                                      # From Step to PathLength: jumping
            nstep     = (move+1) * Step
            PRTVector = (numpy.random.rand(dimension, 1) < PRT) * 1     # If rand() < PRT, PRTVector = 1, else, 0
            #PRTVector = (PRTVector - 1) * (1 - FEs/Max_FEs) + 1              # If rand() < PRT, PRTVector = 1, else, FEs/Max_FEs
            offspring = Migrant + (Leader - Migrant)*nstep*PRTVector    # Jumping towards the Leader
            offspring_path = numpy.append(offspring_path, offspring, axis=1) # Store the jumping path
        size = numpy.shape(offspring_path)                              # How many offspring in the path
        # ------------ Check and put individuals inside the search range if it's outside
        for cl in range(size[1]):                                       # From column
            for rw in range(dimension):                                 # From row: Check
                if offspring_path[rw][cl] < VarMin or offspring_path[rw][cl] > VarMax:  # if outside the search range
                    offspring_path[rw][cl] = VarMin + numpy.random.rand() * (VarMax - VarMin) # Randomly put it inside
        # ------------ Evaluate the offspring and Update ----------------------
        # new_cost = CostFunction(offspring_path.T)-function*100 
        # 
        new_cost = []
        for i in offspring_path.T:
            new_cost = numpy.append(new_cost, problem.evaluate(i))

        FEs = FEs + size[1]                                             # Count the number of function evaluations
        min_new_cost = min(new_cost)                                    # Find the minimum fitness value of new_cost
        # ----- Accepting: Place the best offspring into the current population
        if min_new_cost <= fitness[Migrant_idx]:                        # Compare min_new_cost with fitness value of the moving individual
            idz = numpy.argmin(new_cost)                                # Find the index of minimum value in the new_cost list
            fitness[Migrant_idx] = min_new_cost                         # Replace the moving individual fitness value
            pop[:, Migrant_idx[0]] = offspring_path[:, idz]             # Replace the moving individual position (solution values)
            # ----- Update the global best value --------------------
            if min_new_cost <= the_best_cost:                           # Compare Current minimum fitness with Global minimum fitness
                the_best_cost = min_new_cost                            # Update Global minimun fitness value
                the_best_value = offspring_path[:, idz]                 # Update Global minimun position

    with open(DATFILE, 'w') as f:
	    f.write(str(the_best_cost))

    return(the_best_cost)


if __name__ == "__main__":
	# just check if args are ok
    # 
    with open('args.txt', 'w') as f:
	    f.write(str(sys.argv))

   
    ap = argparse.ArgumentParser(description='Feature Selection using SOMA')
    ap.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    ap.add_argument('--nJumps', dest='nJumps', type=int, required=True, help='nJumps')
    # ap.add_argument('--step', dest='step', type=float, required=True, help='step size')
    # ap.add_argument('--m', dest='m', type=int, required=True, help='m')
    ap.add_argument('--T1', dest='T1', type=float, required=True, help='n')
    ap.add_argument('--T2', dest='T2', type=float, required=True, help='k')
    ap.add_argument('--function', dest='function', type=str, required=True, help='Test function')
    


    ap.add_argument('--datfile', dest='datfile', type=str, required=True, help='File where it will be save the score (result)')
    args = ap.parse_args()
    logging.debug(args)
    
    
    

    main(args.nJumps, args.T1, args.T2, args.datfile, args.function)