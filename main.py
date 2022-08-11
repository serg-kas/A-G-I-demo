# Программа берет изображение прибора без стрелки,
# получает случайное показание и отправляет картинку с ним на предикт.
# Результат визуализируется.
import cv2 as cv
import os
import utils as u

if __name__ == '__main__':
    # Подготовим изображение прибора (резайз и пр.)
    u.gauge_img_preparing()
    assert 'Voltmeter-Blank.jpg' in os.listdir('.')
    # Загружаем изображение прибора без стрелки
    img = cv.imread('Voltmeter-Blank.jpg')
    # Подготавливаем данные положения стрелки прибора
    L, angle_0, angle_1 = u.gauge_needle_preparing(img)

    # Получаем случайное показание прибора
    img, r, _, _ = u.get_random_measurement(img, L, angle_0, angle_1)
    print('Случайное показание прибора: {}'.format(int(300 * (1 - r))))

    # TODO: Случайное показание прибора отправляем на предикт и визуализируем результат

    cv.imshow('V = ' + str(int(300 * (1 - r))), img)
    cv.waitKey(0)
    cv.destroyAllWindows()
