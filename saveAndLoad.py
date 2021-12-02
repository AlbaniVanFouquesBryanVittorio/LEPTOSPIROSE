# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 10:08:13 2021

@author: Bryan Albani Van-Fouques L3 Trec7 UNC


"""

# serialize model to JSON
def save(model,data_dir):
    model_json = model.to_json()
    with open(data_dir+"/model.json", "w") as json_file:
        json_file.write(model_json)
     

    print("Saved model to disk")
    

def load():
    model_dir = 'C:/Users/utilisateur/model.json'
      
    # load json and create model
    with open(model_dir, 'r') as json_file:
        loaded_model_json = json_file.read()
     
        print(loaded_model_json)
  
    print("Loaded model from disk")

