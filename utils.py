# Модуль функций
import numpy as np
import cv2 as cv
import random
import math
import os
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import VGG16
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # закомментировать для использования GPU
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'   # уровень 2 - только сообщения об ошибках

# Размер к которому приводить изображение
IMG_SIZE = 512
# Положение стрелки указывается по изображению прибора после ресайза к IMG_SIZE
# центр стрелки (ось вращения)
X_c = 252
Y_c = 309
# начало шкалы
X_0 = 61
Y_0 = 123
# середина шкалы
X_m = 252
Y_m = 46
# конец шкалы
X_1 = 449
Y_1 = 117


# Функция получения модели
def get_model():
    base_model = VGG16(weights='imagenet')
    model = Model(inputs=base_model.input, outputs=base_model.get_layer("fc2").output)
    return model


# Функция автокоррекции контраста
def autocontrast(img):
    # converting to LAB color space
    lab = cv.cvtColor(img, cv.COLOR_BGR2LAB)
    l_channel, a, b = cv.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv.merge((cl, a, b))

    # Converting image from LAB Color model to BGR color spcae
    result = cv.cvtColor(limg, cv.COLOR_LAB2BGR)
    return result


# Функция подготовки изображения прибора
# Использует файл Voltmeter-NoNeedle.jpg (оригинальное фото прибора с затертой стрелкой)
# Записывает файл Voltmeter-Blank.jpg (значащая часть циферблата без стрелки)
def gauge_img_preparing():
    # Загружаем изображение
    img = cv.imread('Voltmeter-NoNeedle.jpg')

    # Рассчитаем коэффициент для изменения размера
    height = img.shape[0]
    width = img.shape[1]
    if width > height:
        scale_img = IMG_SIZE / width
    else:
        scale_img = IMG_SIZE / height
    # и новые размеры изображения
    new_width = int(width * scale_img)
    new_height = int(height * scale_img)

    # делаем автокоррекцию контраста
    # img = autocontrast(img)

    # делаем ресайз
    img = cv.resize(img, (new_width, new_height), interpolation=cv.INTER_AREA)

    # cv.imshow('image', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    cv.imwrite('Voltmeter-Blank.jpg', img)


def gauge_needle_preparing(img):
    # Стрелка в начале шкалы (слева)
    # line_thickness = 3
    # cv.line(img, (X_0, Y_0), (X_c, Y_c), (0, 255, 0), thickness=line_thickness)
    L_0 = ((X_0 - X_c) ** 2 + (Y_0 - Y_c) ** 2) ** 0.5
    # print('Длина стрелки в начале шкалы: {}'.format(L_0))

    # Стрелка в середине шкалы
    # line_thickness = 3
    # cv.line(img, (X_c, Y_c), (X_m, Y_m), (0, 255, 0), thickness=line_thickness)
    L_m = ((X_c - X_m) ** 2 + (Y_c - Y_m) ** 2) ** 0.5
    # print('Длина стрелки в середине шкалы: {}'.format(L_m))

    # Стрелка в конце шкалы (справа)
    # line_thickness = 3
    # cv.line(img, (X_1, Y_1), (X_c, Y_c), (0, 255, 0), thickness=line_thickness)
    L_1 = ((X_1 - X_c) ** 2 + (Y_1 - Y_c) ** 2) ** 0.5
    # print('Длина стрелки в конце шкалы: {}'.format(L_1))

    # Усредненная длина стрелки
    L = int((L_0 + L_m + L_1) / 3)
    # print('Усредненная длина стрелки: {}'.format(L))

    # Угол отсчитываем по часовой стрелке от angle_0 до angle_1
    angle_0 = math.atan2(Y_c - Y_0, X_c - X_0)
    # print('Угол стрелки в начале шкалы: {:.2f}'.format(angle_0))
    # Посчитаем угол наклона стрелки в конце шкалы
    angle_1 = math.pi - math.atan2(Y_c - Y_1, X_1 - X_c)
    # print('Угол стрелки в конце шкалы: {:.2f}'.format(angle_1))
    return L, angle_0, angle_1


# Получить случайное показание прибора
def get_random_measurement(img, L, angle_0, angle_1):
    # берем случайное показание прибора в диапазоне от 0 до 1
    r = random.uniform(0, 1)
    # print('Случайное значение показания: {:.2f}'.format(r))

    # пересчитываем случайное показание в случайный угол
    angle_r = angle_0 + r * (angle_1 - angle_0)
    # print('Получили случайный угол {:.2f}'.format(angle_r))

    # рисуем стрелку в случайном положении angle_r, длины L
    X_r = X_c - int(L * math.cos(angle_r))
    Y_r = Y_c - int(L * math.sin(angle_r))
    #
    line_thickness = 4
    cv.line(img, (X_r, Y_r), (X_c, Y_c), (0, 0, 0), thickness=line_thickness)

    # убираем шум
    kernel = np.ones((3, 3), np.uint8)
    img = cv.dilate(img, kernel, iterations=1)
    img = cv.erode(img, kernel, iterations=1)
    # преобразуем по порогу
    ret, img = cv.threshold(img, 180, 255, cv.THRESH_BINARY)
    # делаем автокоррекцию контраста
    # img = autocontrast(img)

    # Отрежем часть рисунка где нет шкалы
    img = img[:175, :]
    return img, r


# Функция получение картинки измерения по углу и длине стрелки
def get_angle_measurement(img, L, angle_r):
    # рисуем стрелку в заданном положении angle_r, длины L
    X_r = X_c - int(L * math.cos(angle_r))
    Y_r = Y_c - int(L * math.sin(angle_r))
    #
    line_thickness = 4
    cv.line(img, (X_r, Y_r), (X_c, Y_c), (0, 0, 0), thickness=line_thickness)

    # убираем шум
    kernel = np.ones((3, 3), np.uint8)
    img = cv.dilate(img, kernel, iterations=1)
    img = cv.erode(img, kernel, iterations=1)
    # преобразуем по порогу
    ret, img = cv.threshold(img, 180, 255, cv.THRESH_BINARY)
    # делаем автокоррекцию контраста
    # img = autocontrast(img)

    # Отрежем часть рисунка где нет шкалы
    img = img[:175, :]
    return img
