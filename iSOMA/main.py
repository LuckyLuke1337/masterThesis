# --- SOMA Simple Program --- Version: iSOMA (V1.0) August 25, 2020 -------
# ------ Written by: Quoc Bao DIEP ---  Email: diepquocbao@gmail.com   ----
# -----------  See more details at the end of this file  ------------------


import numpy
import cec2017.functions as functions

# libaries to work with arguments:
import argparse
import logging
import sys


def main(nJumps, step, m, n, k, DATFILE, function):
    dimension = 10                                                      # Number of dimensions of the problem
    # -------------- Control Parameters of SOMA -------------------------------
    # nJumps, step = 10, 0.3                                              # Assign values ​​to variables: step, PRT, PathLength
    PopSize, Max_Migration, Max_FEs = 100, 100, dimension*10**4         # Assign values ​​to variables: PopSize, Max_Migration
    # m, n, k = 10, 5, 15
    # -------------- The domain (search space) --------------------------------
    VarMin, VarMax = -100, 100
    functionIndex = function -1
    CostFunction = functions.all_functions[functionIndex]

    pop = VarMin + numpy.random.rand(dimension, PopSize) * (VarMax - VarMin) # Create the initial Population
    fitness = CostFunction(pop.T)-function*100                                         # Evaluate the initial population
    FEs = PopSize                                                       # Count the number of function evaluations
    the_best_cost = min(fitness)                                        # Find the Global minimum fitness value
    # ---------------- SOMA MIGRATIONS ----------------------------------------
    best_cost_old = the_best_cost
    Migration, Count = 0, 0                                             # Assign values ​​to variables: Migration
    while FEs < Max_FEs:                                                # Terminate when reaching Max_Migration / User can change to Max_FEs
        Migration = Migration + 1                                       # Increase Migration value
        # ------------ Migrant selection: m -----------------------------------
        M = numpy.random.choice(range(PopSize),m,replace=False)         # Migrant selection: m
        M_sort = numpy.argsort(fitness[M])
        for j in range(n):                                              # Choose n individuals move toward the Leader
            Migrant = pop[:, M[M_sort[j]]].reshape(dimension, 1)        # Get the Migrant position (solution values) in the current population
            # ------------ Leader selection: k --------------------------------
            K = numpy.random.choice(range(PopSize),k,replace=False)     # Leader selection: k
            K_sort = numpy.argsort(fitness[K])
            Leader = pop[:, K[K_sort[1]]].reshape(dimension, 1)         # Get the Migrant position (solution values) in the current population
            if M[M_sort[j]] == K[K_sort[1]]:                            # Don't move if it is itself
                Leader = pop[:, K[K_sort[2]]].reshape(dimension, 1)     # Get the Migrant position (solution values) in the current population
            # ------ Migrant move to Leader: Jumping --------------------------
            flag, move = 0, 1
            while (flag == 0) and (move <= nJumps):
                nstep = (nJumps-move+1) * step
                # ------ Update Control parameters: PRT -----------------------
                PRT = 0.1 + 0.9*(FEs / Max_FEs);                        # Update PRT parameter
                # ----- SOMA Mutation -----------------------------------------
                PRTVector = (numpy.random.rand(dimension,1)<PRT)*1      # If rand() < PRT, PRTVector = 1, else, 0
                #PRTVector = (PRTVector - 1) * (1 - FEs/Max_FEs) + 1     # If rand() < PRT, PRTVector = 1, else, FEs/Max_FEs
                offspring = Migrant + (Leader - Migrant) * nstep * PRTVector # Jumping towards the Leader
                # ------------ Check and put individuals inside the search range if it's outside
                for rw in range(dimension):                             # From row: Check
                    if offspring[rw]<VarMin or offspring[rw]>VarMax:    # if outside the search range
                        offspring[rw] = VarMin + numpy.random.rand() * (VarMax - VarMin) # Randomly put it inside
                # ------------ Evaluate the offspring and Update --------------
                new_cost = CostFunction(offspring.T)-function*100                      # Evaluate the offspring
                FEs = FEs + 1                                           # Count the number of function evaluations
                # ----- SOMA Accepting: Place the Best Offspring to Pop -------
                if new_cost <= fitness[M[M_sort[j]]]:                   # Compare min_new_cost with fitness value of the moving individual
                    flag = 1
                    fitness[M[M_sort[j]]] = new_cost                    # Replace the moving individual fitness value
                    pop[:, [M[M_sort[j]]]] = offspring                  # Replace the moving individual position (solution values)
                    if new_cost <= the_best_cost:                       # Compare Current minimum fitness with Global minimum fitness
                        the_best_cost = new_cost                        # Update Global minimun fitness value
                        the_best_value = offspring                      # Update Global minimun position
                    else:
                        Count = Count + 1
                move = move + 1
        if Count > PopSize*50:
            if the_best_cost == best_cost_old:
                rat = round(0.1*PopSize)
                pop_temp = VarMin + numpy.random.rand(dimension, rat)*(VarMax-VarMin)
                fit_temp = CostFunction(pop_temp.T)-function * 100
                FEs = FEs + rat
                D = numpy.random.choice(range(PopSize),rat,replace=False)
                pop[:,D] = pop_temp
                fitness[D] = fit_temp
            else:
                best_cost_old = the_best_cost
            Count = 0


    with open(DATFILE, 'w') as f:
	    f.write(str(the_best_cost[0]))

    return(the_best_cost[0])


if __name__ == "__main__":
	# just check if args are ok
    # 
    with open('args.txt', 'w') as f:
	    f.write(str(sys.argv))

   
    ap = argparse.ArgumentParser(description='Feature Selection using SOMA')
    ap.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    ap.add_argument('--nJumps', dest='nJumps', type=float, required=True, help='nJumps')
    ap.add_argument('--step', dest='step', type=float, required=True, help='step size')
    ap.add_argument('--m', dest='m', type=int, required=True, help='m')
    ap.add_argument('--n', dest='n', type=int, required=True, help='n')
    ap.add_argument('--k', dest='k', type=int, required=True, help='k')
    ap.add_argument('--function', dest='function', type=int, required=True, help='Test function')
    


    ap.add_argument('--datfile', dest='datfile', type=str, required=True, help='File where it will be save the score (result)')
    args = ap.parse_args()
    logging.debug(args)
    
    
    

    main(args.nJumps, args.step, args.m, args.n, args.k, args.datfile, args.function)