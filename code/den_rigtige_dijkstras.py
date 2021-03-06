# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 13:01:59 2020

@author: beatemarcussen
"""
\UseRawInputEncoding

import numpy as np
import copy
import math

# q_max_list    = [10,10,10,10,10,10,10,10,10,10,10,10]                #Maks beholdning i lager
q_max_list  = [10,10,10,10,8,8,8,8,10,10,10,10]
# q_min_list       = [0,0,0,0,0,0,0,0,0,0,0,0]                #Minimum beholdning i lager
q_min_list  = [0,0,0,4,4,6,6,4,4,0,0,0]
# i_max_list       = [4,4,4,4,4,4,4,4,4,4,4,4]              #Maks koeb pr. tid
i_max_list  = [4,4,2,2,1,1,1,1,2,2,4,4]
# u_max_list       = [4,4,4,4,4,4,4,4,4,4,4,4]              #Maks salg pr. tid
u_max_list  = [4,4,2,2,1,1,1,1,2,2,4,4]
T           = 12                #Antal tidsperioder
t           = 0
q_0         = 5                 #Start beholdning
q_goal      = 5
straffaktor = 0.7 #0 i basis
r           = 0.04              #Diskonteringsfaktor
p           = [20, 22, 25, 18, 15, 15, 20, 19, 21, 12, 22 ,25]      #Forward priser
p_disc      = [np.e**(-r*t/T) for t in range(1, T+1)]               #Diskonteringsvaerdi
infinity    = 9999              #Bruges som substitut for reelt uendelig
vertices    = [-infinity for i in range(q_min_list[0], q_max_list[0]+1)]




def optimization_of_gas_storage(graph , start , goal ): shortest_distance = {}
    shortest_distance={}
    predecessor = {}
    unseen_nodes = graph
    path = []
    infinity=9999
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
            if weight + shortest_distance [min_node] < shortest_distance[child_node]: 
                shortest_distance[child_node] = weight + shortest_distance [ min_node ]
                predecessor [ child_node ] = min_distance_node
        unseen_nodes.pop(min_distance_node)
    current_node = goal
    while current_node != start:
        path. insert (0,current_node)
        current_node = predecessor[current_node]
    path . insert (0 , start )
    if shortest_distance[goal] != infinity:
        longest_distance = shortest_distance [ goal ]* (-1)+(100*(len(path)-1)+200) 
        print(f'The_highest_profit_is_ + {str(longest_distance)}') 
        print(f'The_path_is_ + {str(path)}')
        
optimization_of_gas_storage(graph, ’q0’, ’q_end’)

 # convert_constant = 100 * ((len(path)) -1)+200 
#Output:
# The highest profit is 252.72
# The path is [’q0’, ’q1.8’, ’q2.4’, ’q3.0’, ’q4.2’, ’q5.6’, ’q6.10’,
# ’q7.6’, ’q8.10’, ’q9.6’, ’q10.10’, ’q11.10’, ’q12.8’, ’q_end’]