# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 10:34:53 2021

@author: Bryan Albani Van-Fouques L3 Trec7 UNC
"""
#Modele LSTM prenant en X les données de pluie (une liste de données) et en Y la qte de leptospirose (une valeur)
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error



# convert an array of values into a dataset matrix
def create_datasetX(dataset, look_back=1):
    dataX = []

    for i in range(len(dataset)-look_back-1):
        
        a=dataset[i-look_back:(i), 0] 
        dataX.append(a)
   
       
    return np.array(dataX)

def create_datasetY(dataset, look_back=1):
	dataY = []
	for i in range(len(dataset)-look_back-1):
	

		dataY.append(dataset[i - look_back, 0])
	return np.array(dataY)


# fix random seed for reproducibility and number of epochs
np.random.seed(7)
epochs=10

# load the dataset
dataframeX = read_csv("heurelepto2.csv", usecols=[0,1,2], engine='python')

dataframeY = read_csv("heurelepto2.csv", usecols=[3], engine='python')


df1 = dataframeX.values
df1 = df1.astype('float32')


dfY = dataframeY.values
dfY = dfY.astype('float32')


# normalize the dataset
scaler = MinMaxScaler()

df1 = scaler.fit_transform(df1)

dfY = scaler.fit_transform(dfY)

# split into train and test sets
train_size = int(len(df1) * 0.50)+1
test_size =  int(len(df1) * 0.30)
validation_size = int( len(df1) * 0.20)

train,validation,test  = df1[0:train_size],df1[train_size:train_size+validation_size] ,df1[train_size+validation_size:len(df1)]



train_output = (int(len(dfY) * 0.50))+1
test_output = int(len(dfY) * 0.30)
validation_output = int(len(dfY) * 0.20)

trainOutput,validationOutput ,testOutput = dfY[0:train_output,:],dfY[train_output:train_output+validation_output,:] ,dfY[train_output+validation_output:len(dfY),:]

# reshape into X=t and Y=t+1
look_back = 3
trainX = create_datasetX(train, look_back)
validationX = create_datasetX(validation, look_back)
testX = create_datasetX(test, look_back)


trainY=create_datasetY(trainOutput, look_back)
validationY = create_datasetY(validationOutput,look_back)
testY=create_datasetY(testOutput, look_back)


# reshape input to be [samples, time steps, features]

trainX = trainX.reshape((trainX.shape[0], trainX.shape[1], 1))
testX = testX.reshape((testX.shape[0], testX.shape[1], 1))
validationX = validationX.reshape((validationX.shape[0],validationX.shape[1],1))

# create and fit the LSTM network
batch_size = 10
model = Sequential()
model.add(LSTM(10, batch_input_shape=(batch_size, look_back,1), stateful=True, return_sequences=True))
model.add(LSTM(10, batch_input_shape=(batch_size, look_back, 1), stateful=True))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
#for i in range(20):
model.fit(trainX, trainY, validation_data=(validationX,validationY), epochs=epochs, batch_size=batch_size, verbose=1, shuffle=False)
model.reset_states()
 
    
# make predictions
trainPredict = model.predict(trainX, batch_size=batch_size)
validationPredict = model.predict(validationX,  batch_size = batch_size)
model.reset_states()
testPredict = model.predict(testX, batch_size=batch_size)

# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

# shift train predictions for plotting
trainPredictPlot = np.empty_like(df1)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

# shift validation predictions for plotting
validationPredictPlot = np.empty_like(df1)
validationPredictPlot[:, :] = np.nan
validationPredictPlot[(len(trainPredict))+(look_back*2):(len(trainPredict)+len(validationPredict)+(look_back*2)), :] = validationPredict



# shift test predictions for plotting
testPredictPlot = np.empty_like(df1)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(df1)-1, :] = testPredict


# plot baseline and predictions
plt.plot(scaler.inverse_transform(dfY))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.title("Epochs:%s et look_back:%s"%(epochs,look_back))
plt.show()
