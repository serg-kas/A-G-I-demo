# Программа берет изображение прибора без стрелки,
# получает случайное показание и отправляет картинку с ним на предикт.
# Результат визуализируется.
import numpy as np
import cv2 as cv
import os
from sklearn.metrics.pairwise import cosine_similarity
import utils as u

if __name__ == '__main__':
    # Подготовим изображение прибора (резайз и пр.)
    u.gauge_img_preparing()
    # Загружаем изображение прибора без стрелки
    assert 'Voltmeter-Blank.jpg' in os.listdir('.')
    img = cv.imread('Voltmeter-Blank.jpg')
    # Подготавливаем данные положения стрелки прибора
    L, angle_0, angle_1 = u.gauge_needle_preparing(img)
    # Загружаем массивы, подготовленные моделью VGG16
    assert 'angles.npy' in os.listdir('.')
    assert 'feat.npy' in os.listdir('.')
    angles = np.load('angles.npy')
    feat_np = np.load('feat.npy')
    # Получаем модель
    feat_extractor = u.get_model()

    # Получаем случайное показание прибора
    curr_img, curr_r = u.get_random_measurement(img.copy(), L, angle_0, angle_1)
    print('Случайное показание прибора: {}'.format(int(300 * curr_r)))
    angle_r = angle_0 + curr_r * (angle_1 - angle_0)

    # получаем предикт
    _, res_r = u.get_pred(feat_extractor, feat_np, angles, curr_img.copy(), L, angle_0, angle_1)
    # пересчитаем радианы в вольты
    curr_V = int(300 * curr_r)
    res_V = int(300 * res_r)
    print('Предсказанное по картинке значение: {}'.format(res_V))
    print('Ошибка: {}'.format(abs(curr_V - res_V)))
    # Напишем значения на картинке
    cv.putText(curr_img, "true=" + str(curr_V), (5, 25),
               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    if abs(curr_V - res_V) <= 5:
        text_color = (0, 255, 0)
    else:
        text_color = (0, 0, 255)
    cv.putText(curr_img, "pred=" + str(res_V), (5, 50),
               cv.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    # Увеличим картинку для записи в файл
    # out_height = curr_img.shape[0] * 2
    # out_width = curr_img.shape[1] * 2
    # out_img = cv.resize(curr_img, (out_width, out_height))
    cv.imwrite('result.jpg', curr_img)

    cv.imshow('Analog Gauge Inspection', curr_img)
    cv.waitKey(0)
    cv.destroyAllWindows()
