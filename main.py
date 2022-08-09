# Программа берет изображение прибора без стрелки,
# и рисует стрелку случайным оразом
import numpy as np
import cv2 as cv
import random
import math
import utils

# Положение стрелки (подбирается по прибору):
# центр (ось вращения)
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



#
if __name__ == '__main__':
    # Подготовим изображение датчика
    utils.gauge_preparing()


    # Загружаем изображение
    img = cv.imread('Voltmeter-Blank.jpg')

    # Рисуем стрелку в положение слева
    # line_thickness = 3
    # cv.line(img, (X_0, Y_0), (X_c, Y_c), (0, 255, 0), thickness=line_thickness)
    # Посчитаем длину стрелки в начале шкалы
    L_0 = ((X_0 - X_c)**2 + (Y_0 - Y_c)**2) ** 0.5
    print('Длина стрелки в начале шкалы: {}'.format(L_0))

    # Рисуем стрелку от середины шкалы
    # line_thickness = 3
    # cv.line(img, (X_c, Y_c), (X_m, Y_m), (0, 255, 0), thickness=line_thickness)
    # Посчитаем длину стрелки
    L_m = ((X_c - X_m)**2 + (Y_c - Y_m)**2) ** 0.5
    print('Длина стрелки в середине шкалы: {}'.format(L_m))

    # Рисуем стрелку в положение справа
    # line_thickness = 3
    # cv.line(img, (X_1, Y_1), (X_c, Y_c), (0, 255, 0), thickness=line_thickness)
    # Посчитаем длину стрелки в конце шкалы
    L_1 = ((X_1 - X_c)**2 + (Y_1 - Y_c)**2) ** 0.5
    print('Длина стрелки в конце шкалы: {}'.format(L_1))
    # Усредненная длина стрелки
    L = int((L_0 + L_m + L_1) / 3)
    print('Усредненная длина стрелки: {}'.format(L))

    # Посчитаем угол наклона стрелки в начале шкалы
    # Угол отсчитываем с конца шкалы (против часовой стрелки)
    angle_0 = math.pi - math.atan2(Y_c-Y_0, X_c-X_0)
    print('Угол наклона в начале шкалы: {}'.format(angle_0))
    # Посчитаем угол наклона стрелки в конце шкалы
    angle_1 = math.atan2(Y_c-Y_1, X_1-X_c)
    print('Угол наклона в начале шкалы: {}'.format(angle_1))

    # берем случайное показание прибора в диапазоне от 0 до 1
    r = random.uniform(0, 1)
    print('Случайное показание прибора: {}'.format(int(300*(1-r))))

    # пересчитываем случайное показание в случайный угол
    angle_r = angle_1 + r * (angle_0 - angle_1)
    print('Получили случайный угол {}'.format(angle_r))

    # рисуем стрелку в случайном положении angle_r, длины L
    X_r = X_c + int(L * math.cos(angle_r))
    Y_r = Y_c - int(L * math.sin(angle_r))
    #
    line_thickness = 3
    cv.line(img, (X_r, Y_r), (X_c, Y_c), (0, 255, 0), thickness=line_thickness)


    cv.imshow('V='+str(int(300*(1-r))), img)
    cv.waitKey(0)
    cv.destroyAllWindows()

