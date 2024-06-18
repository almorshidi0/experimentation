import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import cv2

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam

import matplotlib.image as mpimg
import imgaug as ia
import imgaug.augmenters as iaa

import random

#### STEP 1 - INITIALIZE DATA
def getName(filePath):
    myImagePathL = filePath.split('/')[-2:]
    myImagePath = os.path.join(myImagePathL[0], myImagePathL[1])
    return myImagePath

def importDataInfo(path):
    columns = ['Center', 'Speed', 'Angle']
    noOfFolders = len(os.listdir(path)) // 2
    data = pd.DataFrame()
    for x in range(17, 22):
        dataNew = pd.read_csv(os.path.join(path, f'log_{x}.csv'), names=columns)
        print(f'{x}:{dataNew.shape[0]} ', end='')
        #### REMOVE FILE PATH AND GET ONLY FILE NAME
        dataNew['Center'] = dataNew['Center'].apply(getName)
        data = data.append(dataNew, ignore_index=True)
    print(' ')
    print('Total Images Imported', data.shape[0])
    return data

def balanceData(data, display=True):
    nBin = 31
    samplesPerBin = 300
    
    # Compute histograms for both speed and angle
    hist_speed, bins_speed = np.histogram(data['Speed'], nBin)
    hist_angle, bins_angle = np.histogram(data['Angle'], nBin)
    
    if display:
        center_speed = (bins_speed[:-1] + bins_speed[1:]) * 0.5
        center_angle = (bins_angle[:-1] + bins_angle[1:]) * 0.5
        
        # Visualize speed histogram
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.bar(center_speed, hist_speed, width=0.03)
        plt.plot((np.min(data['Speed']), np.max(data['Speed'])), (samplesPerBin, samplesPerBin))
        plt.title('Speed Data Visualization')
        plt.xlabel('Speed')
        plt.ylabel('No of Samples')
        
        # Visualize angle histogram
        plt.subplot(1, 2, 2)
        plt.bar(center_angle, hist_angle, width=0.03)
        plt.plot((np.min(data['Angle']), np.max(data['Angle'])), (samplesPerBin, samplesPerBin))
        plt.title('Angle Data Visualization')
        plt.xlabel('Steering Angle')
        plt.ylabel('No of Samples')
        
        plt.tight_layout()
        plt.show()
    
    # Remove excess samples for both speed and angle
    removeindexList = []
    for j in range(nBin):
        binDataList = []
        for i in range(len(data)):
            if data['Speed'].iloc[i] >= bins_speed[j] and data['Speed'].iloc[i] <= bins_speed[j + 1] and \
               data['Angle'].iloc[i] >= bins_angle[j] and data['Angle'].iloc[i] <= bins_angle[j + 1]:
                binDataList.append(i)
                
        binDataList = shuffle(binDataList)
        binDataList = binDataList[samplesPerBin:]
        removeindexList.extend(binDataList)

    print('Removed Images:', len(removeindexList))
    data.drop(data.index[removeindexList], inplace=True)
    print('Remaining Images:', len(data))
    
    if display:
        hist_speed, _ = np.histogram(data['Speed'], (nBin))
        hist_angle, _ = np.histogram(data['Angle'], (nBin))
        
        # Visualize balanced data for speed
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.bar(center_speed, hist_speed, width=0.03)
        plt.plot((np.min(data['Speed']), np.max(data['Speed'])), (samplesPerBin, samplesPerBin))
        plt.title('Balanced Speed Data')
        plt.xlabel('Speed')
        plt.ylabel('No of Samples')
        
        # Visualize balanced data for angle
        plt.subplot(1, 2, 2)
        plt.bar(center_angle, hist_angle, width=0.03)
        plt.plot((np.min(data['Angle']), np.max(data['Angle'])), (samplesPerBin, samplesPerBin))
        plt.title('Balanced Angle Data')
        plt.xlabel('Steering Angle')
        plt.ylabel('No of Samples')
        
        plt.tight_layout()
        plt.show()
    
    return data

#### STEP 3 - PREPARE FOR PROCESSING
def loadData(path, data):
    imagesPath = []
    speeds = []
    angles = []
    for i in range(len(data)):
        indexed_data = data.iloc[i]
        imagesPath.append(os.path.join(path, indexed_data['Center']))
        speeds.append(float(indexed_data['Speed']))
        angles.append(float(indexed_data['Angle']))
    imagesPath = np.asarray(imagesPath)
    speeds = np.asarray(speeds)
    angles = np.asarray(angles)
    return imagesPath, speeds, angles

#### STEP 5 - AUGMENT DATA
def augmentImage(imgPath, speed, angle):
    img = mpimg.imread(imgPath)
    if np.random.rand() < 0.5:
        pan = iaa.Affine(translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)})
        img = pan.augment_image(img)
    if np.random.rand() < 0.5:
        zoom = iaa.Affine(scale=(1, 1.2))
        img = zoom.augment_image(img)
    if np.random.rand() < 0.5:
        brightness = iaa.Multiply((0.5, 1.2))
        img = brightness.augment_image(img)
    if np.random.rand() < 0.5:
        img = cv2.flip(img, 1)
        angle = -angle
    return img, speed, angle

#### STEP 6 - PREPROCESS
def preProcess(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img

#### STEP 7 - CREATE MODEL
def createModel():
    model = Sequential()

    model.add(Conv2D(24, (5, 5), (2, 2), input_shape=(66, 200, 3), activation='elu'))
    model.add(Conv2D(36, (5, 5), (2, 2), activation='elu'))
    model.add(Conv2D(48, (5, 5), (2, 2), activation='elu'))
    model.add(Conv2D(64, (3, 3), activation='elu'))
    model.add(Conv2D(64, (3, 3), activation='elu'))

    model.add(Flatten())
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='
    model.add(Dense(10, activation='elu'))
    model.add(Dense(1, name='angle_output'))  # Output for steering angle
    
    # Define outputs and compile the model
    model.compile(optimizer=Adam(lr=0.0001), loss={'angle_output': 'mse'})

    return model

#### STEP 8 - TRAINING
def dataGen(imagesPath, speedList, angleList, batchSize, trainFlag):
    while True:
        imgBatch = []
        speedBatch = []
        angleBatch = []

        for i in range(batchSize):
            index = random.randint(0, len(imagesPath) - 1)
            if trainFlag:
                img, speed, angle = augmentImage(imagesPath[index], speedList[index], angleList[index])
            else:
                img = mpimg.imread(imagesPath[index])
                speed = speedList[index]
                angle = angleList[index]
            img = preProcess(img)
            imgBatch.append(img)
            speedBatch.append(speed)
            angleBatch.append(angle)
        
        yield (np.asarray(imgBatch), {'speed_output': np.asarray(speedBatch), 'angle_output': np.asarray(angleBatch)})
