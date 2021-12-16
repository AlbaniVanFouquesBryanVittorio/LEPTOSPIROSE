# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 10:08:13 2021

@author: Bryan Albani Van-Fouques L3 Trec7 UNC


"""
from pandas import read_csv
import json

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

"""
from keras.models import model_from_json

# serialize model to JSON
model_json = model.to_json()
with open(data_dir+"/model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights(data_dir+"/model.h5")
print("Saved model to disk")

model_dir = '/Users/rodriguegovan/Downloads/M2/Projet BigData/models&templates/model for 97.80% (more logic)/model_97.80%.json'
weight_dir = '/Users/rodriguegovan/Downloads/M2/Projet BigData/models&templates/model for 97.80% (more logic)/model_97.80%.h5'
# load json and create model
json_file = open(model_dir, 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(weight_dir)
print("Loaded model from disk")
"""
#df1 = df1.astype('float32')
