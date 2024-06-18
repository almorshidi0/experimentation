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
import imgaug.augmenters as iaa

import random

#### STEP 1 - INITIALIZE DATA
def getName(filePath):
    # Extracts only the filename from the path
    myImagePathL = filePath.split('/')[-2:]
    myImagePath = os.path.join(myImagePathL[0], myImagePathL[1])
    return myImagePath

def importDataInfo(path):
    # Reads CSV files and imports data while extracting filenames
    columns = ['Center', 'Speed', 'Angle']
    data = pd.DataFrame()
    for x in range(17, 22):
        dataNew = pd.read_csv(os.path.join(path, f'log_{x}.csv'), names=columns)
        dataNew['Center'] = dataNew['Center'].apply(getName)
        data = data.append(dataNew, ignore_index=True)
    print('Total Images Imported:', data.shape[0])
    return data

#### STEP 2 - VISUALIZE AND BALANCE DATA
def balanceData(data, display=True):
    # Balances data distribution for both speed and angle
    nBin = 31
    samplesPerBin = 300
    
    hist_speed, bins_speed = np.histogram(data['Speed'], nBin)
    hist_angle, bins_angle = np.histogram(data['Angle'], nBin)
    
    if display:
        center_speed = (bins_speed[:-1] + bins_speed[1:]) * 0.5
        center_angle = (bins_angle[:-1] + bins_angle[1:]) * 0.5
        
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.bar(center_speed, hist_speed, width=0.03)
        plt.plot((np.min(data['Speed']), np.max(data['Speed'])), (samplesPerBin, samplesPerBin))
        plt.title('Speed Data Visualization')
        plt.xlabel('Speed')
        plt.ylabel('No of Samples')
        
        plt.subplot(1, 2, 2)
        plt.bar(center_angle, hist_angle, width=0.03)
        plt.plot((np.min(data['Angle']), np.max(data['Angle'])), (samplesPerBin, samplesPerBin))
        plt.title('Angle Data Visualization')
        plt.xlabel('Steering Angle')
        plt.ylabel('No of Samples')
        
        plt.tight_layout()
        plt.show()
    
    # Remove excess samples to balance data
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
        
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.bar(center_speed, hist_speed, width=0.03)
        plt.plot((np.min(data['Speed']), np.max(data['Speed'])), (samplesPerBin, samplesPerBin))
        plt.title('Balanced Speed Data')
        plt.xlabel('Speed')
        plt.ylabel('No of Samples')
        
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
    # Loads image paths, speeds, and angles from the dataset
    imagesPath = np.array([os.path.join(path, img_path) for img_path in data['Center']])
    speeds = np.array(data['Speed'])
    angles = np.array(data['Angle'])
    return imagesPath, speeds, angles

#### STEP 5 - AUGMENT DATA
def augmentImage(imgPath, speed, angle):
    # Augments images with various techniques
    img = mpimg.imread(imgPath)
    seq = iaa.Sequential([
        iaa.Affine(translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)}),
        iaa.Affine(scale=(1, 1.2)),
        iaa.Multiply((0.5, 1.2)),
        iaa.Fliplr(1.0)
    ], random_order=True)

    augmented = seq.augment_image(img)
    if np.random.rand() < 0.5:
        augmented = cv2.flip(augmented, 1)
        angle = -angle
    
    return augmented, speed, angle

#### STEP 6 - PREPROCESS
def preProcess(img):
    # Preprocesses images (converts to YUV, applies blur, resizes, normalizes)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img

#### STEP 7 - CREATE MODEL
def createModel():
    # Defines the convolutional neural network model
    model = Sequential()

    model.add(Conv2D(24, (5, 5), (2, 2), input_shape=(66, 200, 3), activation='elu'))
    model.add(Conv2D(36, (5, 5), (2, 2), activation='elu'))
    model.add(Conv2D(48, (5, 5), (2, 2), activation='elu'))
    model.add(Conv2D(64, (3, 3), activation='elu'))
    model.add(Conv2D(64, (3, 3), activation='elu'))

    model.add(Flatten())
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))
    model.add(Dense(1, name='angle_output'))  # Output for steering angle
    
    model.compile(optimizer=Adam(lr=0.0001), loss={'angle_output': 'mse'})

    return model

#### STEP 8 - TRAINNING
def dataGen(imagesPath, speedList, angleList, batchSize, trainFlag):
    # Generates batches of augmented data for training or validation
    while True:
        imgBatch = []
        speedBatch = []
        angleBatch = []

        for _ in range(batchSize):
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
        
        yield (np.asarray(imgBatch), {'angle_output': np.asarray(angleBatch)})
