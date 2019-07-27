
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import sys, os
sys.path.append('models')
from model_utils import gen_wrapper as gen

# config
batch_size = 128
num_epochs = 5 # 10mins each
train_dir = 'data/proc/new/224/'
model_name = 'models/h5/alexnet-3.h5'

model = Sequential()

# conv layers

model.add(Conv2D(filters=96, input_shape=(224,224,3), kernel_size=(11,11),strides=(4,4), padding='valid', activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='valid'))
#model.add(BatchNormalization())

model.add(Conv2D(filters=256, kernel_size=(11,11), strides=(1,1), padding='valid', activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='valid'))
#model.add(BatchNormalization())

#model.add(Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding='valid', activation='relu'))
#model.add(BatchNormalization())

#model.add(Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding='valid', activation='relu'))
#model.add(BatchNormalization())

model.add(Conv2D(filters=256, kernel_size=(3,3), strides=(1,1), padding='valid', activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='valid'))
#model.add(BatchNormalization())

# dense layers

model.add(Flatten())
#model.add(Dense(4096, input_shape=(224*224*3,), activation='relu'))
#model.add(Dropout(0.4))
#model.add(BatchNormalization())

#model.add(Dense(4096, activation='relu'))
#model.add(Dropout(0.4))
#model.add(BatchNormalization())

model.add(Dense(1000, activation='relu'))
model.add(Dense(1000, activation='relu'))
#model.add(Dropout(0.4))
#model.add(BatchNormalization())

model.add(Dense(5, activation='softmax'))

model.summary()

train_datagen = ImageDataGenerator(validation_split=0.1)

train_generator = train_datagen.flow_from_directory(
	train_dir, target_size=(224,224), batch_size=batch_size,
	class_mode='categorical', shuffle=True, color_mode='rgb',
	subset='training'
)

valid_generator = train_datagen.flow_from_directory(
	train_dir, target_size=(224,224), batch_size=batch_size,
	class_mode='categorical', shuffle=True, color_mode='rgb',
	subset='validation'
)

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

hist = model.fit_generator(
	generator=gen(train_generator),
	steps_per_epoch=(train_generator.n // batch_size),
	epochs=num_epochs,
	validation_data=gen(valid_generator),
	validation_steps=(valid_generator.n // batch_size),
	verbose=1
)

print(hist.history)
print('Trn Acc: ' + str(hist.history['acc'][-1]))
print('Val Acc: ' + str(hist.history['val_acc'][-1]))

num = [len(os.listdir(train_dir + str(cid))) for cid in range(5)]

print('Ran Acc: ' + str(max(num)/np.sum(num)))

model.save(model_name)
