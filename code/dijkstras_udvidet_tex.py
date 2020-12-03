#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 15:12:40 2020

@author: beatemarcussen
"""

import numpy as np

q_max       = [10,10,10,10,8,8,8,8,10,10,10,10]      #Maks beholdning i lager
sorted_q_max = q_max.copy()
sorted_q_max.sort() 
q_min       = [0,0,0,4,4,6,6,4,4,0,0,0]              #Minimum beholdning i lager
sorted_q_min = q_min.copy()
sorted_q_min.sort() 
i_max       = [4,4,2,2,1,1,1,1,2,2,4,4]              #Maks koeb pr. tid
u_max       = [4,4,2,2,1,1,1,1,2,2,4,4]              #Maks salg pr. tid
T           = 12                #Antal tidsperioder
q_0         = 5                 #Start beholdning
q_T         = 0                 #Slut beholdning
p_0         = 0                 #Start kapital
straffaktor = 0.7
r           = 0.04              #Diskonteringsfaktor
p           = [20, 22, 25, 18, 15, 15, 20, 19, 21, 12, 22 ,25]      #Forward priser
p_disc      = [np.e**(-r*t/T) for t in range(1, T+1)]               #Diskonteringsvaerdi
infinity    = 9999              #Bruges som substitut for reelt uendelig
vertices    = [-infinity for i in range(q_min[0], q_max[-1]+1)]
graph       = [p_0]             #?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!!?!?!?!?!?!?
path        = []                #Tom list hvor vores fortjenester bliver gemt
pre_vertice = [q_0]             #Listen gemmer vores loebende beholdinger

#repræsentation af grafen (identitisk med den anden)
def get_graph():
    global graph
    global pre_vertice
    for i in range (T):
        graph.append(vertices.copy())
        pre_vertice.append(vertices.copy())
    graph.append(-infinity)
    pre_vertice.append(-infinity)

def get_profit():
    get_graph()
    global graph
    global pre_vertice
    for t in range(T):
        if t == 0:
            for q in range(q_0 - u_max[0], q_0 + i_max[0]+1):
                if q_min[0] <= q <= q_max[0]:
                    graph[1][q] = round(p_0 + p[0]*(q_0 - q)*p_disc[0],1)
                    pre_vertice[1][q] = q_0
        else:
            for i in range(2,T+1):
                for q_pre in range(q_min[i-2], q_max[i-2]+1): 
                    for q_change in range(-u_max[i-1],i_max[i-1]+1):
                        q_current = q_pre + q_change
                        if q_min[i-1] <= q_current <= q_max[i-1]:
                            value = round(graph[i-1][q_pre]-(p[i-1]* (q_change)* p_disc[i-1]),1)
                            if graph[i][q_current] < value:
                                graph[i][q_current] = value
                                pre_vertice[i][q_current] = q_pre
    for q_pre in range(q_min[-1], q_max[-1] + 1):
        value = graph[T][q_pre] +(p[T-1]*(q_pre-q_T)*p_disc[T-1])
        if graph[T+1] < value:
            graph[T+1] = value
            pre_vertice[T+1] = q_pre


# def get_path():
#     global path
#     get_profit()
#     path.append(q_T)
#     path.append(pre_vertice[T+1])
#     for t in range(T):
#         path.append(pre_vertice[T-t][path[t+1]])
#     path.reverse()