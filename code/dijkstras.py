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
p_goal      = 0                 #Tilfaeldigt tal for programmet virker
alpha       = 1                 #Der er ingen straffaktor naar alpha = 1
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
                                #Vaerdi efter diskonteringsfaktor
infinity    = 9999              #Bruges som substitut for reelt uendelig

#Udvidet problem
# q_max       = [10, 10, 10, 10, 8, 8, 8, 8, 10, 10, 10, 10]                
#                                 #Maks beholdning i lager
# q_min       = [0, 0, 0, 4, 4, 6, 6, 4, 4, 0, 0, 0]                 
#                                 #Minimum beholdning i lager
# i_max       = [4, 4, 2, 2, 1, 1, 1, 1, 2, 2, 4, 4]                 
#                                 #Maks koeb pr. tid
# u_max       = [4, 4, 2, 2, 1, 1, 1, 1, 2, 2, 4, 4]                    
#                                 #Maks salg pr. tid
# p_goal      = 5                 #Lagerbeholdnings aftale
# alpha       = 0.07              #Straffaktor                          
# T           = 12                #Antal tidsperioder
# q_0         = 5                 #Start beholdning
# q_T         = 0                 #Slut beholdning
# p_0         = 0                 #Start kapital
# r           = 0.04              #Diskonteringsfaktor
# p           = [20, 22, 25, 18, 15, 15, 20, 19, 21, 12, 22 ,25]      
#                                 #Forward priser
# disc        = [np.e**(-r*t/T) for t in range(1, T+1)]               
#                                 #Diskonteringsvaerdi
# p_disc      = [p[i]*disc[i] for i in range(T)]                      
#                                 #Vaerdi efter diskonteringsfaktor
# infinity    = 9999              #Bruges som substitut for reelt uendelig


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
    vertices.append('q_slut')
    for i in range(T+1):
        if i == 0:
            for j in range(-u_max[i], i_max[i]+1):
                addEdge(graph, vertices[i], vertices[i+1][q_0 + j], round(j*p_disc[i]+250,2))   
        elif i == 12:
            for k in range(q_min[i-1], q_max[i-1]+1):
                if k == p_goal:
                    addEdge(graph, vertices[i][k], vertices[i+1],round(-k*p_disc[i-1]+250,2))
                else:
                    addEdge(graph, vertices[i][k], vertices[i+1],round(-k*p_disc[i-1]+250,2)/alpha)
        else:
            for k in range(q_min[i-1], q_max[i-1]+1):
                current_units = k
                min_units = current_units - u_max[i]
                if min_units < q_min[i]:
                    min_units = q_min[i]
                max_units = current_units + i_max[i]
                if max_units > q_max[i]:
                    max_units = q_max[i]
                for j in range(min_units, max_units+1):
                    addEdge(graph, vertices[i][k], vertices[i+1][j],round((j-k)*p_disc[i]+250,2))
    addEdge(graph, vertices[len(vertices)-1], vertices[len(vertices)-2][0], 0)
    return graph



def optimization_of_gas_storage(graph , start , goal ): 
    shortest_distance = {}
    predecessor = {}
    unseen_nodes = graph
    path = []
    for node in unseen_nodes :
        shortest_distance[node] = infinity
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
    current_node = goal
    while current_node != start:
        path. insert (0,current_node)
        current_node = predecessor[current_node]
    path . insert (0 , start )
    if shortest_distance[goal] != infinity:
        longest_distance = (shortest_distance [ goal ] - 13 * 250) * (-1)
        print(f'The highest profit is {round(longest_distance,2)} Euro') 
        print(f'The path is {str(path)}')

    
optimization_of_gas_storage(graph_dict(), 'q0.5', 'q_slut')


# print(graph_dict())
















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
