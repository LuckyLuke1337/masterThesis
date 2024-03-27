
# --- SOMA Simple Program --- Version: SOMA T3A (V2.0) January 06, 2022 ---
# ------ Written by: Quoc Bao DIEP ---  Email: diepquocbao@gmail.com   ----
# -----------  See more details at the end of this file  ------------------
import numpy
import cec2017.functions as functions

# libaries to work with arguments:
import argparse
import logging
import sys

def main(m, n, k, nJumps, DATFILE, function):

    Dim = 30
    functionIndex = function - 1
    costFunction = functions.all_functions[functionIndex]
    # -------------- Control Parameters of SOMA -------------------------------
    # nJumps = 45
    NP = 30
    Max_FEs = 300000
    # Max_Mig, Max_FEs = 300000, Dim*100*NP
    # m, n, k = 9, 5, 9
    # -------------- The domain (search space) --------------------------------
    VarMin = -100 + numpy.zeros(Dim)
    VarMax = 100 + numpy.zeros(Dim)


    # ------------- Create the initial Population -----------------------------
    VarMin = numpy.repeat(VarMin.reshape(Dim, 1),NP,axis=1)
    VarMax = numpy.repeat(VarMax.reshape(Dim, 1),NP,axis=1)
    # print("VarMax:",VarMax)
    # pop = VarMin + numpy.random.rand(Dim, NP) * (VarMax - VarMin)
    pop = VarMin + numpy.random.rand(Dim, NP) * (VarMax - VarMin)
    # print("initial population:",pop)

    # fit = CostFunction(pop)
    fit = costFunction(pop.T)-(100*function)
    # fit = functions.f5([pop])[0]

    # print("initial fitness:",fit)
    FEs = NP
    best_fit = min(fit)
    id = numpy.argmin(fit)
    best_val = pop[:, id]
    # ---------------- SOMA MIGRATIONS ----------------------------------------
    Mig = 0
    while FEs < Max_FEs:
        Mig = Mig + 1
        # ------------ Migrant selection: m -----------------------------------
        M = numpy.random.choice(range(NP),m,replace=False)
        # print("M:",M)
        M_sort = numpy.argsort(fit[M])
        newpop = numpy.zeros((Dim,n*nJumps))
        for j in range(n):
            Migrant = pop[:, M[M_sort[j]]].reshape(Dim, 1)
            # ------------ Leader selection: k --------------------------------
            K = numpy.random.choice(range(NP),k,replace=False)
            K_sort = numpy.argsort(fit[K])
            Leader = pop[:, K[K_sort[0]]].reshape(Dim, 1)
            if M[M_sort[j]] == K[K_sort[0]]:
                Leader = pop[:, K[K_sort[1]]].reshape(Dim, 1)
            PRT = 0.05 + 0.90*(FEs/Max_FEs)
            Step = 0.15 - 0.08*(FEs/Max_FEs)
            nstep = numpy.arange(0,nJumps)*Step+Step
            PRTVector = (numpy.random.rand(Dim, nJumps) < PRT) * 1
            indi_new = Migrant + (Leader - Migrant) * nstep * PRTVector
            # ------------ Check and put individuals inside the search range if it's outside
            for cl in range(nJumps):
                for rw in range(Dim):
                    if indi_new[rw,cl] < VarMin[rw,0] or indi_new[rw,cl] > VarMax[rw,0]:
                        indi_new[rw,cl] = VarMin[rw,0] + numpy.random.rand() * (VarMax[rw,0] - VarMin[rw,0])
            newpop[:,nJumps*j:nJumps*(j+1)] = indi_new
        # ------------ Evaluate the offspring and Update -------------
        newfitpop = costFunction(newpop.T)-(100*function)
        FEs = FEs + n*nJumps
        for j in range(n):
            newfit = newfitpop[nJumps*j:nJumps*(j+1)]
            min_newfit = min(newfit)
            # ----- Accepting: Place the best offspring into the current population
            if min_newfit <= fit[M[M_sort[j]]]:
                fit[M[M_sort[j]]] = min_newfit
                id = numpy.argmin(newfit)
                pop[:, M[M_sort[j]]] = newpop[:, (nJumps*j)+id]
                # ----- Update the global best value --------------------
                if min_newfit < best_fit:
                    best_fit = min_newfit
                    best_val = newpop[:, (nJumps*j)+id]


    
    with open(DATFILE, 'w') as f:
	    f.write(str(best_fit))
    return(best_fit)

if __name__ == "__main__":
	# just check if args are ok
    # 
    with open('args.txt', 'w') as f:
	    f.write(str(sys.argv))

    ap = argparse.ArgumentParser(description='Feature Selection using SOMAT3A')

    ap.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	
    ap.add_argument('--m', dest='m', type=int, required=True, help='Miigrants')
    ap.add_argument('--n', dest='n', type=int, required=True, help='Best n')
    ap.add_argument('--k', dest='k', type=int, required=True, help='Best k')
    ap.add_argument('--nJumps', dest='nJumps', type=int, required=True, help='Jumps count')

    ap.add_argument('--function', dest='function', type=int, required=True, help='Test function')

    ap.add_argument('--datfile', dest='datfile', type=str, required=True, help='File where it will be save the score (result)')
    args = ap.parse_args()
    logging.debug(args)
    
    # functionIndex = args.function - 1
    

    main(args.m, args.n, args.k, args.nJumps, args.datfile, args.function)

"""
This algorithm is programmed according to the descriptions in the papers 
listed below:

Link of paper: https://ieeexplore.ieee.org/abstract/document/8790202/
Diep, Q.B., 2019, June. Self-Organizing Migrating Algorithm Team To Team 
Adaptive–SOMA T3A. In 2019 IEEE Congress on Evolutionary Computation (CEC)
(pp. 1182-1187). IEEE.

The control parameters PopSize, nJumps, m, n, and k are closely related 
and greatly affect the performance of the algorithm. Please refer to the 
above paper to use the correct control parameters.
"""