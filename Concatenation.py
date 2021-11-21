# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 12:41:02 2021

@author: Bryan Albani Van-Fouques L3 Trec7 UNC
"""
#Script permettant la concatenation des données (exemple pluie et leptospirose)

from pandas import read_csv
import pandas as pd


#Importer les différents fichier
pluie = read_csv('pluie_Regen.csv', usecols=[0], engine='python')
temps = read_csv('temps.txt',sep='\t' , engine='python')

lepto= read_csv('leptoLucas.txt',sep='\t' , engine='python')

#Créaation de DataFrame pour chaque fichier de données
df1=pd.DataFrame()
df1[["Date","Time"]]=temps


df2=pd.DataFrame()
df2["float"]=pluie

#Ajout de df2 dans une colonne de df1
df1["Qte"] = df2["float"]

#Normalise la date et l'heure

df1['Date'] = pd.to_datetime(df1['Date'], format=' %d-%b-%Y').dt.date
df1['Time'] = pd.to_datetime(df1['Time'], format='%H:%M:%S').dt.time
lepto['Date']=pd.to_datetime(lepto['Date'],format='%m/%d/%y').dt.date
lepto['Time']=pd.to_datetime(lepto['Time'],format='%H:%M %p').dt.time


#df1 contient la quantité de pluie toutes les 6 minutes donc il faut faire une moyenne par jours 



#Permet d'obtenir un jeu de donnée où la leptospirose est dupliqué

#liste vide
l=[]

for i in lepto.index:
    for j in df1.index:
        if lepto["Date"][i]==df1["Date"][j] and lepto["Time"][i].hour==df1["Time"][j].hour:
            l.append((df1["Date"][j],df1["Time"][j],df1["Qte"][j],lepto["Lepto"][i]))
            
#Nouvelle DataFrame contenant nos données dupliquer                       
jeuDuplique=pd.DataFrame()
jeuDuplique[["Date","Time","Qte_eau","Qte_lepto"]]=l       

#print(jeuDuplique)


