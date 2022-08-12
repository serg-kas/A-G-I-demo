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
    # подготовим изображение для отправки в модель
    img_to_pred = curr_img.copy()
    img_to_pred = cv.resize(img_to_pred, (224, 224), cv.INTER_LINEAR)
    img_to_pred = img_to_pred / 255.
    img_to_pred = np.expand_dims(img_to_pred, axis=0)
    pred = feat_extractor.predict(img_to_pred)
    # определяем наиболее близкую картинку (ее индекс)
    cosPred = cosine_similarity(pred, feat_np)
    pred_idx = np.argmax(cosPred)
    #
    res_img = img.copy()
    res_angle = angles[pred_idx]
    res_img = u.get_angle_measurement(res_img, L, res_angle)
    res_r = (res_angle - angle_0) / (angle_1 - angle_0)

    # пересчитаем радианы в вольты
    curr_V = int(300 * curr_r)
    res_V = int(300 * res_r)

    # Напишем значение pred на картинке
    cv.putText(curr_img, "pred=" + str(res_V), (5, 25),
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv.imshow('V = ' + str(int(300 * curr_r)), curr_img)
    cv.waitKey(0)
    cv.destroyAllWindows()
