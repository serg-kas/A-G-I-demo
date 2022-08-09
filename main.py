# Программа берет изображение прибора без стрелки,
# и рисует стрелку случайным оразом
import numpy as np
import cv2 as cv
import os
import utils

if __name__ == '__main__':
    # Подготовим изображение прибора (резайз и пр.)
    utils.gauge_img_preparing()
    assert 'Voltmeter-Blank.jpg' in os.listdir('.')
    # Загружаем изображение прибора без стрелки
    img = cv.imread('Voltmeter-Blank.jpg')
    # Подготавливаем данные положения стрелки прибора
    L, angle_0, angle_1 = utils.gauge_needle_preparing(img)

    # Получаем случайное показание прибора
    r, img = utils.get_random_measurement(img, L, angle_0, angle_1)
    print('Случайное показание прибора: {}'.format(int(300 * (1 - r))))

    cv.imshow('V = ' + str(int(300 * (1 - r))), img)
    cv.waitKey(0)
    cv.destroyAllWindows()
