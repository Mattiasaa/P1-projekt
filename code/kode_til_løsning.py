#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:45:26 2020

@author: beatemarcussen
"""

"""
  Gaslager optimering
C1-14 5 """

import math as math
import matplotlib.pyplot as plt
min_lager = 0
max_lager = 10 #Hoejeste antal enheder lager kan indeholde
T = 12 #Antal tider
start_lager = 5 #Enheder i lageret til tid 0
slut_lager = 0 #Enheder i lageret til T+1
start_kapital = 0.0 #Penge til tid nul
r = 0.04 #Diskonteringsrenten
max_change = 4 #Stoereste aendring i lager der kan forekomme til t 
sats = [20,22,25,18,15,15,20,19,21,12,22,25] #Til P1: [20,22,25,18,15,15,20,19,21,12,22,25] 
defineret_sidste_sats = False #Saet True hvis der er angivet en sats
      #til til tiden for slut_lager (Saettes False i P0)

afrunding = 2 #Antal decimaler i grafens vaerdier
savefig = True #Gemmer figuren hvis True

dis_list = [math.exp((-r)*(t/T)) for t in range(1,T+1)]
lager = [-1000000 for j in range(min_lager,max_lager+1)]
graf = [start_kapital] #Start_lager bliver lagt ind til tiden 0
path_list = []
Predecessor = [start_lager]
x_list=[i for i in range(0,T+2)]

#repræsentation af grafen:
for i in range(0,T): #Alle knuderne tilfoejes i grafen
    graf.append(lager.copy())
    Predecessor.append(lager.copy())
graf.append(-1000000) #Det endelige antal enheder i lageret tilfoejes
Predecessor.append(-100000)

#den maksimale profit
for q in range(start_lager-max_change,start_lager+max_change+1):
      #Foerste kolonne beregnes for sig selv
      if min_lager<=q<=max_lager:
          graf[1][q] = round(start_kapital+sats[0]*(start_lager -
                                                    q)*dis_list[0],2)
          Predecessor[1][q]=start_lager

for t in range(2,T+1):
   for tidligere_q in range(min_lager,max_lager+1): #0,max_lager+1
      for change_q in range(-max_change,max_change+1):
        ny_q = tidligere_q + change_q
        if min_lager<=ny_q<=max_lager:
           value = round(graf[t-1][tidligere_q]-(sats[t-1]* (change_q)
               * dis_list[t-1]),afrunding)
           if graf[t][ny_q] < value:
              graf[t][ny_q] = value
              Predecessor[t][ny_q] = tidligere_q
              
if defineret_sidste_sats == True:
   for tidligere_q in range(min_lager,max_lager+1):
      value = graf[T][tidligere_q] +(sats[T]*(tidligere_q-slut_lager)*dis_list[T-1])
      if graf[T+1] < value:
        graf[T+1] = value
        Predecessor[T+1] = tidligere_q
else:
   for tidligere_q in range(min_lager,max_lager+1):
      value = graf[T][tidligere_q] +(sats[T-1]*(tidligere_q-slut_lager)*dis_list[T-1])
      if graf[T+1] < value:
        graf[T+1] = value
        Predecessor[T+1] = tidligere_q
max_profit = graf[T+1]


#vejen findes
path_list.append(slut_lager)
path_list.append(Predecessor[T+1])
for t in range(0,T):
      path_list.append(Predecessor[T-t][path_list[t+1]])
path_list.reverse()

#værdierne printes
plt.scatter(0,start_lager,c='gray')
for t in range(1,T+1):
   for q in range(min_lager,max_lager+1):
      plt.scatter(t,q,c='gray')
plt.scatter(T+1,slut_lager,c='gray')

plt.ylim(min_lager-0.4,max_lager+0.4)
plt.xlabel("Tid [t]")
plt.ylabel("Enheder i lager [qt]")
plt.title("Optimering af gaslager")
plt.plot(x_list,path_list,'r')

if savefig == True:
      plt.savefig('graph.png',dpi=300)
print("Under de angivede omstaendigheder er den hoejeste mulige profit {} Euro ved at foelge vejen {}.".format(round(max_profit,2),path_list))





