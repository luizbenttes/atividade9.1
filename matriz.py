# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 22:57:35 2017

@author: rafaelaprm
"""
import pandas as pd

df = pd.read_csv('topologia1.csv', sep=r',')

new_list = []
grafo_adj = {}

for i in range(len(df)):
    string = df['Adjacencias'][i]
    string = string.replace('[','')
    string = string.replace(']','')
    string = string.replace(', ',',')
    string = string.replace("'","")
    string = string.split(',')
    new_list = new_list + [string]

print(new_list)
grafo = [[0 for _ in range(len(df))] for _ in range (len(df))]
print(grafo)
lista = []
listaNomes= ["No 1", "No 2", "No 3"]
for i in range (len(df)):
    for j in range(len(new_list[i])-1):
        for k in range (len(listaNomes)):
            if (listaNomes[k]==new_list[i][j]):
                grafo[i][k]=int(new_list[i][j+1])
    
    adjacents = []
    for l in range(len(grafo)):
        if grafo[i][l] != 0:
            adjacents.append(l)
    grafo_adj[i] = adjacents
    

print(grafo, grafo_adj)