# -*- coding: utf-8 -*-
"""CNN Architectures.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sHNk9HK7xob5a4TP8slbjcT0Y_SFkUmT

#Intro

Convolution Neural network is a type of artificial neural network used in image recognition and processing that is specifically designed to process pixel data.They are used for image recognition and classification tasks.

This notebook illustrates different types of CNN architecture and their working for different image dataset such as:

1.LeNet

2.AlexNet

3.ResNet50

4.VGG16

5.MobileNetV2

6.GoogleNet

#Import Libraries
"""

import os
from os import listdir
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras import Model
from keras.optimizers import SGD
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Flatten, Dense, Dropout, Conv2D, MaxPooling2D
import tensorflow_hub as hub

"""#Dataset 

1.The loaded dataset have images in their original resolution, thus they are of different shapes.
"""

folder_path='/Users/akridata/data/flower-new/Images/'
for dirname, _, filenames in os.walk(folder_path):
  print(dirname)

print('Total daisy images:', len(os.listdir(folder_path + 'daisy')))
print('Total rose images:', len(os.listdir(folder_path + 'rose')))
print('Total tulip images:', len(os.listdir(folder_path + 'tulip')))
print('Total dandelion images:', len(os.listdir(folder_path + 'dandelion')))
print('Total sunflower images:', len(os.listdir(folder_path + 'sunflower')))

"""Class labels defined for flower dataset:5 classes"""
 
 categories=['daisy','rose','tulip','dandelion','sunflower']

target_names = ['daisy','dandelion','rose','sunflower','tulips']
image_height = 150
image_width  = 150
batch_size = 32
train_datagen = ImageDataGenerator(
        rescale=1./255.,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split = 0.2)

train_data = train_datagen.flow_from_directory(
        folder_path,
        target_size=(image_height, image_width),
        color_mode="rgb",
        batch_size=batch_size,
        class_mode='categorical',
        subset = 'training',
        shuffle=False)
valid_data = train_datagen.flow_from_directory(
        folder_path,
        target_size=(image_height, image_width),
        color_mode="rgb",
        batch_size=batch_size,
        subset = 'validation',
        class_mode='categorical',
        shuffle=False)
# Function to get labels from generators to separate them
def get_labels(gen):
    labels = []
    sample_no = len(gen.filenames)
    call_no = int(math.ceil(sample_no / batch_size))
    for i in range(call_no):
        labels.extend(np.array(gen[i][1]))
    
    return np.array(labels)

for category in categories:
    fig, _ = plt.subplots(3,4)
    fig.suptitle(category)
    for k, v in enumerate(os.listdir(folder_path+category)[:12]):
        img = plt.imread(folder_path+category+'/'+v)
        plt.subplot(3, 4, k+1)
        plt.axis('off')
        plt.imshow(img)
    plt.show()

"""#CNN Architectures

##VGG16
"""

from tensorflow.keras.applications import VGG16,ResNet50,MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

input_tensor = Input(shape=(150,150,3))
model = VGG16(weights='imagenet', include_top=False,input_tensor = input_tensor)

model.summary()

model.predict()

from keras.layers import Dropout, Flatten, Dense, GlobalAveragePooling2D
for layer in model.layers[:5]:
    layer.trainable = False

#Adding custom Layers 
x = model.output
x = Flatten()(x)
x = Dense(1024, activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(1024, activation="relu")(x)
predictions = Dense(1, activation="sigmoid")(x)

# creating the final model 
model_final =  Model(inputs=model.input, outputs=predictions)

model_final.compile(loss='binary_crossentropy',optimizer="adam",metrics=['acc'])

model_final.summary()

history=model_final.fit_generator(train_data,epochs=2,validation_data=valid_data,validation_steps=50)

"""##Resnet50"""

resnet_model = ResNet50(weights = "imagenet", include_top=False, input_shape = (150, 150, 3))

for layer in resnet_model.layers[:5]:
    layer.trainable = False

#Adding custom Layers 
x = resnet_model.output
x = Flatten()(x)
x = Dense(512, activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(1024, activation="relu")(x)
x = Dropout(0.5)(x)
predictions = Dense(1, activation="sigmoid")(x)

# creating the final model 
model_final1 =  Model(inputs=resnet_model.input, outputs=predictions)
model_final1.compile(loss='binary_crossentropy',optimizer="adam",metrics=['acc'])

model_final1.summary()

history=model_final1.fit_generator(train_data,epochs=2,validation_data=valid_data,validation_steps=50)

"""##MobilenetV2"""

mobile_model = MobileNetV2(input_shape=(150,150,3), weights='imagenet', include_top=False)

for layer in mobile_model.layers[:5]:
    layer.trainable = False

#Adding custom Layers 
x = mobile_model.output
x = Flatten()(x)
x = Dense(512, activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(1024, activation="relu")(x)
x = Dropout(0.5)(x)
predictions = Dense(1, activation="sigmoid")(x)

# creating the final model 
model_final2 =  Model(inputs=mobile_model.input, outputs=predictions)
model_final2.compile(loss='binary_crossentropy',optimizer="adam",metrics=['acc'])

model_final2.summary()

history=model_final2.fit_generator(train_data,epochs=2,validation_data=valid_data,validation_steps=50)