# -*- coding: utf-8 -*-
"""
SOMA-CLP implementation
Self-organizing Migrating Algorithm with Clustering-aided Migration and Adaptive Perturbation Vector Control
BCM: random

NP_L = 10% of NP

Created on Sat Apr  8 11:46:12 2023

@author: kadavy
"""
import random
import copy
import numpy as np
from sklearn.cluster import KMeans
import math
import matplotlib.pyplot as plt

import opfunu

# libaries to work with arguments:
import argparse
import logging
import sys


def sortLeaders(l):
    return l[1]

def leaderRank(leaders):
    _start = len(leaders)
    _max = (_start/2) * (2+_start-1)
    _rand = random.randint(0, _max)
    for l in leaders:
        l[1] = _start
        _start = _start - 1
    _start = 0
    for l in leaders:
        _start = _start + l[1]
        if _rand < _start:
            return l
    return leaders[-1]    

def SOMA_CL(pathA, stepA, path, step, DATFILE, function):

    lim = [(-100, 100) for i in range(10)] #bounds for each dim
    maxFES = 100000                     #maximum number of function evaluations
    NP = 100   
    
    # pathA = 3
    # stepA = 0.33
    # path = 2
    # step = 0.11

    #dim size
    dimension = len(lim)
    problem = getattr(opfunu.cec_based, function)(ndim=dimension)

    #initial population and cost
    _pop = [[random.uniform(lim[j][0], lim[j][1]) for j in range(dimension)] for i in range(NP)]
    _fpop = [problem.evaluate(i) for i in _pop]
    _FES = NP

    #select gBest
    _fgBest = min(_fpop)
    _gBest = _pop[_fpop.index(_fgBest)]
    _his = [[0, _fgBest]]
    _NPleaders = math.ceil(0.1 * NP)

    
    #main run
    while(_FES <= maxFES):
        #all to random
        #copy of the current population
        _cp = copy.deepcopy(_pop)
        _cpf = copy.deepcopy(_fpop)
        _temp = copy.deepcopy(_pop)
        _tempf = copy.deepcopy(_fpop)
        _allPoints = []
        on = True
        for i in range(NP):
            if on == False:
                break
            #select random leader
            _leader = i
            while(_leader == i):
                _leader = random.randint(0, NP-1)
            #move over path
            for t in np.arange(0, pathA, stepA):
                #generate PRT vector
                _prtA = 0.08 + 0.9 * (float(_FES)/float(maxFES))
                _prtVector = [0 for j in range(dimension)]
                for j in range(dimension):
                    if random.uniform(0, 1) > _prtA:
                        _prtVector[j] = 0
                    else:
                        _prtVector[j] = 1
                #move individual
                for j in range(dimension):
                    _temp[i][j] = _pop[i][j] + (_pop[_leader][j] - _pop[i][j]) * t * _prtVector[j]
                    #BCM: random
                    if _temp[i][j] < lim[j][0] or _temp[i][j] > lim[j][1]:
                        _temp[i][j] = random.uniform(lim[j][0], lim[j][1])
                #fit new position
                _tempf[i] = problem.evaluate(_temp[i])
                _FES = _FES + 1
                #new gBest?
                if _tempf[i] < _fgBest:
                    _fgBest = _tempf[i]
                    _gBest = copy.deepcopy(_temp[i])
                    _his.append([_FES, _fgBest])
                if _tempf[i] < _cpf[i]:
                    _cpf[i] = copy.deepcopy(_tempf[i])
                    _cp[i] = copy.deepcopy(_temp[i])
                #add points for clustering
                _allPoints.append([copy.deepcopy(_temp[i]), _tempf[i]])

                if _FES >= maxFES:
                    on = False
                    break
            #copy new pop
        _pop = copy.deepcopy(_cp)
        _fpop = copy.deepcopy(_cpf)
        
        if(_FES >= maxFES):
            on = False
            break
        
        #clustering
        kmeans = KMeans(n_clusters = _NPleaders)
        kmeans.fit([_allPoints[i][0] for i in range(len(_allPoints))])
        #pick only pBest from each cluster
        _leaders = [None for i in range(_NPleaders)]
        for i in range(len(_allPoints)):
            _c = kmeans.labels_[i]
            if _leaders[_c] == None:
                _leaders[_c] = [copy.deepcopy(_allPoints[i][0]), _allPoints[i][1]]
            else:
                if _allPoints[i][1] < _leaders[_c][1]:
                    _leaders[_c] = [copy.deepcopy(_allPoints[i][0]), _allPoints[i][1]]
            
        #all to cluster leader
        _cp = copy.deepcopy(_pop)
        _cpf = copy.deepcopy(_fpop)
        _temp = copy.deepcopy(_pop)
        _tempf = copy.deepcopy(_fpop)
       
        for i in range(NP):
            _leader = leaderRank(_leaders)
            if _FES >= maxFES:
                on = False
                break
            #move over path
            for t in np.arange(step, path, step):
                _prt = 0.08 + 0.9 * (float(_FES)/float(maxFES))
                _prtVector = [0 for j in range(dimension)]
                for j in range(dimension):
                    if random.uniform(0, 1) > _prt:
                        _prtVector[j] = 0
                    else:
                        _prtVector[j] = 1
                #move individual
                for j in range(dimension):
                    _temp[i][j] = _pop[i][j] + (_leader[0][j] - _pop[i][j]) * t * _prtVector[j]
                    #BCM: random
                    if _temp[i][j] < lim[j][0] or _temp[i][j] > lim[j][1]:
                        _temp[i][j] = random.uniform(lim[j][0], lim[j][1])
                #fit new position
                _tempf[i] = problem.evaluate(_temp[i])
                _FES = _FES + 1
                #new gBest?
                if _tempf[i] < _fgBest:
                    _fgBest = _tempf[i]
                    _gBest = copy.deepcopy(_temp[i])
                    _his.append([_FES, _fgBest])
                if _tempf[i] < _cpf[i]:
                    _cpf[i] = copy.deepcopy(_tempf[i])
                    _cp[i] = copy.deepcopy(_temp[i])

                if _FES >= maxFES:
                    on = False
                    break
            #copy new pop
        _pop = copy.deepcopy(_cp)
        _fpop = copy.deepcopy(_cpf)
        
        if(_FES >= maxFES):
            on = False
            break               
    
    with open(DATFILE, 'w') as f:
	    f.write(str(_fgBest))
    
    return _fgBest



if __name__ == "__main__":
    
    ap = argparse.ArgumentParser(description='Feature Selection using SOMAT3A')

    ap.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	
    ap.add_argument('--pathA', dest='pathA', type=float, required=True, help='PathA')
    ap.add_argument('--stepA', dest='stepA', type=float, required=True, help='StepA')
    ap.add_argument('--path', dest='path', type=float, required=True, help='Path')
    ap.add_argument('--step', dest='step', type=float, required=True, help='Step')

    ap.add_argument('--function', dest='function', type=str, required=True, help='Test function')

    ap.add_argument('--datfile', dest='datfile', type=str, required=True, help='File where it will be save the score (result)')
    args = ap.parse_args()
    logging.debug(args)
    

    
    
    
    SOMA_CL(args.pathA, args.stepA, args.path, args.step, args.datfile, args.function)
   