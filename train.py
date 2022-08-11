# Подготавливам и обучаем модель
import numpy as np
import cv2 as cv
import os
import utils as u

# import tensorflow as tf
# print(tf.__version__)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam, Adadelta
# from tensorflow.keras import utils
from tensorflow.keras.utils import Sequence
from tensorflow.keras.models import load_model, save_model

from PIL import Image

# Функция создания модели
def get_model():
    model = Sequential()
    # слой пакетной нормализации - входной
    model.add(BatchNormalization(input_shape=(58,170,1)))
    # первый сверточный слой
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    # второй сверточный слой - идентичен первому сверточному слою
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    # слой подвыборки
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # слой Dropout
    model.add(Dropout(0.25))
    # разворачиваем в вектор для перехода к полносвязным слоям
    model.add(Flatten())
    # первый полносвязный слой
    model.add(Dense(64, activation='relu'))
    # слой Dropout
    model.add(Dropout(0.25))
    # второй - выходной полносвязный слой
    model.add(Dense(1, activation='linear'))

    # Компилируем сеть
    model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    # model.compile(loss='mae', optimizer='adam', metrics=['mse'])
    return model


# Генератор данных
def generate_data(batchsize):
    x_data = []
    y_data = []
    batchcount = 0
    while True:
        curr_r, curr_img = u.get_random_measurement(img, L, angle_0, angle_1)
        x_data.append(curr_img)
        y_data.append(curr_r)
        batchcount += 1
        if batchcount >= batchsize:
            X = np.array(x_data, dtype='float32')
            X = X.reshape(batchsize, 58, 170, 1)  # добавляем ось
            y = np.array(y_data, dtype='float32')
            print(X.shape, y.shape)
            yield (X, y)
            x_data = []
            y_data = []
            batchcount = 0


if __name__ == '__main__':
    # Создаем модель
    model = get_model()
    # Напечатаем архитектуру
    # model.summary()
    # Сохраним модель
    model.save('model.h5')

    # Подготовим изображение прибора (резайз и пр.)
    u.gauge_img_preparing()
    assert 'Voltmeter-Blank.jpg' in os.listdir('.')
    # Загружаем изображение прибора без стрелки
    img = cv.imread('Voltmeter-Blank.jpg')
    # Подготавливаем данные положения стрелки прибора
    L, angle_0, angle_1 = u.gauge_needle_preparing(img)

    # Запускаем обучение
    batch_size = 50
    history = model.fit(generate_data(batch_size),
                        steps_per_epoch=1000 / batch_size, epochs=10)

