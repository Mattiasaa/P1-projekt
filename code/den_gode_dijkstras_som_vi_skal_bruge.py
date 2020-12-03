# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 12:03:31 2020

@author: marcu
"""

from collections import defaultdict
import numpy as np
 
q_max       = 10                #Maks beholdning i lager
q_min       = 0                 #Minimum beholdning i lager
i_max       = 4                 #Maks koeb pr. tid
u_max       = 4                 #Maks salg pr. tid
T           = 12                #Antal tidsperioder
q_0         = 5                 #Start beholdning
q_T         = 0                 #Slut beholdning
p_0         = 0                 #Start kapital
r           = 0.04              #Diskonteringsfaktor
p           = [20, 22, 25, 18, 15, 15, 20, 19, 21, 12, 22 ,25]      
                                #Forward priser
disc        = [np.e**(-r*t/T) for t in range(1, T+1)]               
                                #Diskonteringsvaerdi
p_disc      = [p[i]*disc[i] for i in range(T)]                      
                                #Værdi efter diskonteringsfaktor
infinity    = 9999              #Bruges som substitut for reelt uendelig



def addEdge(graph,u,v,e):
    if u in graph:
        graph[u].update( {v : e} )
    else:
        graph[u] = {v : e}



def graph_dict():
    graph = defaultdict(list)
    vertices = ['q00']
    for i in range(1,T+1):
        vertices.append(['q' + str(i) +'.'+ str(j) for j in range (q_max+1)])
    vertices.append('q_slut')
    for i in range(T+1):
        if i == 0:
            for j in range(-u_max, i_max+1):
                addEdge(graph, vertices[i][0], vertices[i+1][q_0 + j], round(j*p_disc[i],2))   
        elif i == 12:
            for k in range(q_min, q_max+1):
                addEdge(graph, vertices[i][k], vertices[i+1][0],round(k*p_disc[i-1],2))
        else:
            for k in range(q_min, q_max+1):
                current_units = k
                min_units = current_units - u_max
                if min_units < q_min:
                    min_units = q_min
                max_units = current_units + i_max
                if max_units > q_max:
                    max_units = q_max
                for j in range(min_units, max_units+1):
                    addEdge(graph, vertices[i][k], vertices[i+1][j],round((j-k)*p_disc[i],2))
    return graph

print(graph_dict())



















# print(graph_dict()['q'])


# def generate_edges(graph):
#     edges = []
 
#     # for each node in graph
#     for node in graph:
         
#         # for each neighbour node of a single node
#         for neighbour in graph[node]:
             
#             # if edge exists then append
#             edges.append((node, neighbour))
#     return edges
