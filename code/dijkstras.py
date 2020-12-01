# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 11:30:15 2020

@author: marcu
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

'''Vi vil nu implementere Dijkstras algoritme i python, således vi kan bruge 
den til at løse vores problem i dets rigtige størrelse.
Vi vil først indsætte dataen i python og finde en måde hvorpå python kan generere
vores data uden at vi manuelt skal skrive alle kantvægte ind.'''

'''Indsætning af data'''
q_0             = 5
q_max           = 10
q_min           = 0
u_max           = 4
i_max           = 4
T               = 12
t               = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
p_t             = [20, 22, 25, 18, 15, 15, 20, 19, 21, 12, 22, 25]
r               = 0.04


'''Vi vil nu finde de reelle værdier for forwardpriserne i forhold til nutidsværdien.
Vi laver først en liste med interest som udregner hvor meget mere værd penge er
til tiden t med vores diskonteringsfaktor r. Derefter kan vi bruge denne liste 
til at beregne de reelle værdier for forward priserne'''


def interest():                         #Danner liste med diskonteringsværdier
    interest_rate = []
    for i in t:
        interest_i = np.e**(-r * i /T) 
        interest_rate.append(interest_i)
    return interest_rate


def get_interest_price():               #Danner liste med reelle værdier
    interest_price = []
    for i in range (len(t)):
        a = interest()[i]*p_t[i]
        interest_price.append(a)
    return interest_price



'''Vi vil nu generere en nabomatrix til grafen. Vi starter med at finde mængden
af knuder. Da vi ved at der er 12 måneder om vores beholding kan være fra 0 til 11
ved vi at der i grafen må være 12*11 knuder plus startknuden og slutknuden (når 
vi sælger til lejer'''
amount_vertices = 12 * 11 + 2
matrix = np.zeros((amount_vertices, amount_vertices))    #Laver en tom matrix 
print(matrix)


