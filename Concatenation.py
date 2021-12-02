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
def dupliqueLepto():
    
    #liste vide
    l=[]
    
    for i in lepto.index:
        for j in df1.index:
            if lepto["Date"][i]==df1["Date"][j] and lepto["Time"][i].hour==df1["Time"][j].hour:
                l.append((df1["Date"][j],df1["Time"][j],df1["Qte"][j],lepto["Lepto"][i]))
    return l





#Permet de formatter l'heure pour obtenir dans avoir une réccurence toutes les 30 minutes.
#ttime format de l'heure
def time_fomat(ttime):
    ho = ttime.strftime("%H")
    my_time = ttime.strftime("%H:%M:00")

    my_time = my_time.replace("59", "30").replace("05", "00").replace("54", "30")
    
    if ho == "05":
        my_time = my_time.replace("00", "05", 1)

    return my_time



#Fonction permettant d'obtenir des nouveaux jeux de données en foncion du parametre d. 
#On obtient donc des jeux de données  par 30 min, par heures, par jours et par mois. 
#d est un string qui est entré par l'utilisateur permettant de choisir si le jeu de données deviant par jours/heure/...
def traitement_donnee(d):
    liste=[]
    temp=0
    temp2=0
    cpt=0
    cpt2=0
    i=0
    
    
    if d == "minutes":
        
        #Moyenne de données par 30 min
        for i in range (len(df1)-1):
        
            if df1["Date"][i] == df1["Date"][i+1] and df1["Time"][i].hour == df1["Time"][i+1].hour:
                
                if df1["Time"][i].minute == 0:
                    temp += df1["Qte"][i]
                    cpt += 1
                 
                elif 0 < df1["Time"][i].minute < 30:
                     temp = temp+df1["Qte"][i]
                     cpt += 1
                     
                elif 31 <= df1["Time"][i].minute <= 59 :
                     
                     temp2 = temp2+df1["Qte"][i]
                     cpt2 += 1
                
                
            
            else:
                temp2 = temp2+df1["Qte"][i]
                cpt2 += 1
                mean1 = temp/(cpt)
                mean2 = temp2/(cpt2)
                cpt=0
                cpt2=0
                
                my_time = time_fomat(df1["Time"][i])
                my_time2 = time_fomat(df1["Time"][i+1])
     
                liste.append((df1["Date"][i],my_time,mean1))
                liste.append((df1["Date"][i],my_time2,mean2))
                temp=0
                temp2=0
            
           
    elif d == "heure":   
        
        #Moyenne de données par heures
        for i in range (len(df1)-1):
           
          
            if df1["Date"][i] == df1["Date"][i+1] and df1["Time"][i].hour==df1["Time"][i+1].hour:
                temp=temp+df1["Qte"][i+1]
                cpt=cpt+1
                
            else:
                
                mean =temp/cpt
                
                
                cpt=1
                temp=df1["Qte"][i+1]
                
                liste.append((df1["Date"][i],df1["Time"][i].hour,mean))
             
    
    elif d == "jours":
        
        #Moyenne de données par jours
        for i in range (len(df1)-1):
           
            
            if df1["Date"][i] == df1["Date"][i+1]:
                temp=temp+df1["Qte"][i+1]
                cpt=cpt+1
                
            else:
               
                mean =temp/cpt
                
                
                cpt=1
                temp=df1["Qte"][i+1]
                liste.append((df1["Date"][i],df1["Time"][i],mean))
                
         
    elif d == "mois": 
        
        #Moyenne de données par mois
        for i in range (len(df1)-1):
           
            
            if df1["Date"][i].month == df1["Date"][i+1].month:
                temp=temp+df1["Qte"][i+1]
                cpt=cpt+1
                
            else:
     
                mean =temp/cpt
         
                cpt=1
                temp=df1["Qte"][i+1]
                liste.append((df1["Date"][i].month,df1["Time"][i],mean))   
                
            
    else:
        print("ERREUR: Le praramètre utilisé n'est pas bon")

    
    
    return liste


         
#Permet d'obtenir un nouveau jeu de donnée x et y 
#x contenant les données de pluie n (jours/heures/...) avant
#y contenant la donnée lepto à l'instant t
#d est un string qui est entré par l'utilisateur permettant de choisir si le jeu de données devient par jours/heure/...
#n est un int disant combien de temps avant on prends les données pour x
def data_and_lepto(n,d):
    k=0
    F_Data=pd.DataFrame()
    d_pluie=pd.DataFrame()
    d_pluie[["Date","Time","Qte_eau"]]=traitement_donnee(d)
    #x une liste vide
    x=[]

    if d == "minutes":
        for i in range(len(lepto)):
            for j in range (len(d_pluie)):
                
                if lepto["Date"][i] == d_pluie["Date"][j] and lepto["Time"][i] == d_pluie["Time"][j]:
                    #print(lepto["Time"][i], d_pluie["Time"][j])
                    x.append([[d_pluie["Qte_eau"][j-3]],[d_pluie["Qte_eau"][j-2]],[d_pluie["Qte_eau"][j]]])
                    
                    
        F_Data["x"]=x 
        F_Data["y"]=lepto["Lepto"]
        
    elif d == "heure":
        for i in range(len(lepto)):
            for j in range (len(d_pluie)):
                if lepto["Date"][i] == d_pluie["Date"][j] and lepto["Time"][i].hour == d_pluie["Time"][j]:
                    x.append([[d_pluie["Qte_eau"][j-3]],[d_pluie["Qte_eau"][j-2]],[d_pluie["Qte_eau"][j]]])
            
        F_Data["x"]=x 
        F_Data["y"]=lepto["Lepto"]
        
    elif d == "jours":
        for i in range(len(lepto)):
            for j in range (len(d_pluie)):
                if lepto["Date"][i] == d_pluie["Date"][j] :
                    x.append([[d_pluie["Qte_eau"][j-3]],[d_pluie["Qte_eau"][j-2]],[d_pluie["Qte_eau"][j]]])
    

        
        F_Data["x"]=x 
        F_Data["y"]=lepto["Lepto"]
       

    elif d == "mois":
        for i in range(len(lepto)):
            for j in range (len(d_pluie)):
                
                if lepto["Date"][i].month == d_pluie["Date"][j] and k<=i:
                    k += 1
                    x.append([[d_pluie["Qte_eau"][j-3]],[d_pluie["Qte_eau"][j-2]],[d_pluie["Qte_eau"][j]]]) 
                    
                    
                    
        F_Data["x"]=x 
        F_Data["y"]=lepto["Lepto"]
       
    else: 
        print("ERREUR: Le praramètre utilisé n'est pas bon")

    

    
    
   
    return F_Data

def SaveFile(filename):
    filename.to_csv('test2.csv', sep=',', index=False)
    

"""

#Nouvelle DataFrame contenant nos données dupliquer                       
jeuDuplique=pd.DataFrame()
jeuDuplique[["Date","Time","Qte_eau","Qte_lepto"]]= dupliqueLepto()  
print(jeuDuplique)
SaveFile(jeuDuplique)

 

datalepto=pd.DataFrame()
datalepto[["x","y"]]= data_and_lepto(3,"jours")  
print(datalepto)
"""