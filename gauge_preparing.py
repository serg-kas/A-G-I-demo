# Программа подготовки изображения прибора
# Используется файл Voltmeter2.jpg - изображение прибора без стрелки.
# Необходимо запускать один раз, чтобы получить файл Voltmeter-blank.jpg

import numpy as np
import cv2 as cv
# import utils

# Размер к которому приводить изображение
IMG_SIZE = 512

# Загружаем изображение
img = cv.imread('Voltmeter2.jpg')

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

#
# kernel = np.ones((3, 3), np.uint8)
# img = cv.dilate(img, kernel, iterations=1)
# img = cv.erode(img, kernel, iterations=1)
#
# ret, img = cv.threshold(img, 180, 255, cv.THRESH_BINARY)

# делаем автокоррекцию контраста
# img = utils.autocontrast(img)

# делаем ресайз
img = cv.resize(img, (new_width, new_height), interpolation=cv.INTER_AREA)

cv.imshow('image', img)
cv.waitKey(0)
cv.destroyAllWindows()

cv.imwrite('Voltmeter-blank.jpg', img)
