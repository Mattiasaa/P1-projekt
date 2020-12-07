# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 12:03:31 2020

@author: marcu
"""

from collections import defaultdict
import numpy as np

#Basis problem
q_max       = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]                
                                #Maks beholdning i lager
q_min       = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]                 
                                #Minimum beholdning i lager
i_max       = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]                 
                                #Maks koeb pr. tid
u_max       = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]                    
                                #Maks salg pr. tid
q_goal      = 0                 #Tilfaeldigt tal
kappa       = 1                 #Der er ingen straffaktor naar kappa = 1
T           = 12                #Antal tidsperioder
q_0         = 5                 #Startbeholdning
q_T         = 0                 #Slutbeholdning
p_0         = 0                 #Startkapital
r           = 0.04              #Diskonteringsfaktor
p           = [20, 22, 25, 18, 15, 15, 20, 19, 21, 12, 22, 25]      
                                #Forward-priser
disc        = [np.e**(-r*t/T) for t in range(1, T+1)]               
                                #Diskonteringsvaerdi
p_disc      = [p[i]*disc[i] for i in range(T)]                      
                                #Vaerdi efter diskonteringsfaktor
max_edge    = max(p) * q_max[len(p)-1]
                                #Den værdi vi lægger til alle kantvægte

#Udvidet problem
q_max       = [10, 10, 10, 10, 8, 8, 8, 8, 10, 10, 10, 10]                
                                #Maks beholdning i lager
q_min       = [0, 0, 0, 4, 4, 6, 6, 4, 4, 0, 0, 0]                 
                                #Minimum beholdning i lager
i_max       = [4, 4, 2, 2, 1, 1, 1, 1, 2, 2, 4, 4]                 
                                #Maks koeb pr. tid
u_max       = [4, 4, 2, 2, 1, 1, 1, 1, 2, 2, 4, 4]                    
                                #Maks salg pr. tid
q_goal      = 5                 #Lagerbeholdnings aftale
kappa       = 0.7               #Straffaktor                          
T           = 12                #Antal tidsperioder
q_0         = 5                 #Startbeholdning
q_T         = 0                 #Slutbeholdning
p_0         = 0                 #Startkapital
r           = 0.04              #Diskonteringsfaktor
p           = [20, 22, 25, 18, 15, 15, 20, 19, 21, 12, 22, 25]      
                                #Forward-priser
disc        = [np.e**(-r*t/T) for t in range(1, T+1)]               
                                #Diskonteringsvaerdi
p_disc      = [p[i]*disc[i] for i in range(T)]                      
                                #Vaerdi efter diskonteringsfaktor
max_edge    = p[len(p)-1] * q_max[len(p)-1]
                                #Den værdi vi lægger til alle kantvægte



def addEdge(graph,u,v,e):
    if u in graph:
        graph[u].update( {v : e} )
    else:
        graph[u] = {v : e}


def graph_dict():
    graph = defaultdict(list)
    vertices = ['q0.5']
    for i in range(1,T+1):
        vertices.append(['q' + str(i) +'.'+ str(j) for j in range (q_max[i-1]+1)])
    vertices.append('q_end')
    t = 0
    for j in range(-u_max[t], i_max[t]+1):
        addEdge(graph, vertices[t], vertices[t+1][q_0 + j], round(j*p_disc[t]+max_edge,2))
    t = 12
    for k in range(q_min[t-1], q_max[t-1]+1):
        if k == q_goal:
            addEdge(graph, vertices[t][k], vertices[t+1],round(-k*p_disc[t-1]+max_edge,2))
        else:
            addEdge(graph, vertices[t][k], vertices[t+1],round(-k*p_disc[t-1]+max_edge,2)/kappa)
    for t in range(1,T):
        for k in range(q_min[t-1], q_max[t-1]+1):
            current_units = k
            min_units = current_units - u_max[t]
            if min_units < q_min[t]:
                min_units = q_min[t]
            max_units = current_units + i_max[t]
            if max_units > q_max[t]:
                max_units = q_max[t]
            for j in range(min_units, max_units+1):
                addEdge(graph, vertices[t][k], vertices[t+1][j],round((j-k)*p_disc[t]+max_edge,2))
    addEdge(graph, vertices[len(vertices)-1], vertices[len(vertices)-2][0], 0)
    return graph



def dijkstras(graph , start , end ): 
    shortest_distance = {}
    predecessor = {}
    unseen_nodes = graph
    path = []
    for node in unseen_nodes :
        shortest_distance[node] = float('inf')
    shortest_distance [ start ] = 0
    while unseen_nodes : 
        min_distance_node = None
        for node in unseen_nodes : 
            if min_distance_node is None :
                min_distance_node = node
            elif shortest_distance [node] < shortest_distance[min_distance_node]: 
                min_distance_node = node
        for child_node, weight in graph [ min_distance_node ].items ( ): 
            if graph.get(child_node) is None:
                pass
            else:
                if weight + shortest_distance [min_distance_node] < shortest_distance[child_node]: 
                    shortest_distance[child_node] = weight + shortest_distance [ min_distance_node ]
                    predecessor [ child_node ] = min_distance_node
        unseen_nodes.pop(min_distance_node)
    current_node = end
    while current_node != start:
        path. insert (0,current_node)
        current_node = predecessor[current_node]
    path . insert (0 , start )
    longest_distance = round((shortest_distance [ end ] - (len(path)-1) * max_edge) * (-1), 2)
    return longest_distance, path


def get_profit(graph, start, end):
    longest_distance, path = dijkstras(graph, start, end)
    print(f'The highest profit is {round(longest_distance,2)} Euro') 
    print(f'The path is {str(path)}')
    

get_profit(graph_dict(), 'q0.5', 'q_end')



