# Модуль функций
import cv2 as cv


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
# Использует файл Voltmeter-NoArrow.jpg
# Записывает файл Voltmeter-Blank.jpg
def gauge_preparing():
    # Размер к которому приводить изображение
    IMG_SIZE = 512

    # Загружаем изображение
    img = cv.imread('Voltmeter-NoArrow.jpg')

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

    # cv.imshow('image', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    cv.imwrite('Voltmeter-Blank.jpg', img)
