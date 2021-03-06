# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 12:03:31 2020

@author: marcus
"""



from math import exp
#Basisproblem
q_max       = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]                
                                #Maksimal beholdning i lager
q_min       = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]                 
                                #Minimum beholdning i lager
i_max       = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]                 
                                #Maksimal koeb pr. tid
u_max       = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]                    
                                #Maksimal salg pr. tid
q_goal      = 0                 #Tilfaeldigt tal. har kun betydning 
                                # naar kappa !=0
kappa       = 0                 #Der er ingen straffaktor naar kappa = 0
T           = 12                #Antal tidsperioder
q_0         = 5                 #Startbeholdning
r           = 0.04              #Diskonteringsfaktor
p           = [20, 22, 25, 18, 15, 15, 20, 19, 21, 12, 22, 25]      
                                #Forward-priser
disc        = [exp(-r*t/T) for t in range(1, T+1)]               
                                #Diskonteringsvaerdi
p_disc      = [round(p[i]*disc[i],2) for i in range(T)]                      
                                #Diskonterede priser
max_edge    = max(p) * q_max[len(p)-1]
                                #Den vaerdi vi laegger til alle kantvaegte



#Udvidet problem
q_max       = [10, 10, 10, 10, 8, 8, 8, 8, 10, 10, 10, 10]                
                                #Maksimal beholdning i lager
q_min       = [0, 0, 0, 4, 4, 6, 6, 4, 4, 0, 0, 0]                 
                                #Minimum beholdning i lager
i_max       = [4, 4, 2, 2, 1, 1, 1, 1, 2, 2, 4, 4]                 
                                #Maksimal koeb pr. tid
u_max       = [4, 4, 2, 2, 1, 1, 1, 1, 2, 2, 4, 4]                    
                                #Maksimal salg pr. tid
q_goal      = 5                 #Lagerbeholdnings aftale
kappa       = 0.7               #Straffaktor                          
T           = 12                #Antal tidsperioder
q_0         = 5                 #Startbeholdning
r           = 0.04              #Diskonteringsfaktor
p           = [20, 22, 25, 18, 15, 15, 20, 19, 21, 12, 22, 25]      
                                #Forward-priser
disc        = [exp(-r*t/T) for t in range(1, T+1)]               
                                #Diskonteringsvaerdi
p_disc      = [round(p[i]*disc[i],2) for i in range(T)]                      
                                #Diskonterede priser
max_edge    = p[len(p)-1] * q_max[len(p)-1]
                                #Den vaerdi vi laegger til alle kantvaegte




def add_edge(graph,u,v,e):
    if u in graph:
        graph[u].update( {v : e} )
    else:
        graph[u] = {v : e}


def graph_dict():
    graph = {}
    vertices = ['v0,5']
    for i in range(1,T+1):
        vertices.append(['v' + str(i) +','+ str(j) for j in range (q_max[i-1]+1)])
    vertices.append('q_end')
    t = 0
    for j in range(q_0-u_max[t], q_0+i_max[t]+1):
        add_edge(graph, vertices[t], vertices[t+1][j], (q_0-j)*p_disc[t]*(-1)+max_edge)
    t = 12
    for k in range(q_min[t-1], q_max[t-1]+1):
        if k == q_goal:
            add_edge(graph, vertices[t][k], vertices[t+1],k*p_disc[t-1]*(-1)+max_edge)
        else:
            add_edge(graph, vertices[t][k], vertices[t+1],(k*p_disc[t-1]*(-1)*(1-kappa)+max_edge))
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
                add_edge(graph, vertices[t][k], vertices[t+1][j],(k-j)*p_disc[t]*(-1)+max_edge)
    add_edge(graph, vertices[len(vertices)-1], vertices[len(vertices)-2][0], 0)
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
    if shortest_distance[end] != float('inf'):
        return shortest_distance[end], path


def get_profit(graph, start, end):
    shortest_distance, path = dijkstras(graph, start, end)
    longest_distance = round((shortest_distance - (len(path)-1) * max_edge) * (-1), 2)
    print(f'The highest profit is {round(longest_distance,2)} euro') 
    print(f'The path is {str(path)}')
    

get_profit(graph_dict(), 'v0,5', 'q_end')




