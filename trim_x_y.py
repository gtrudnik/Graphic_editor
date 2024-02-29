from PIL import Image
# функции для обрезки изображения по оси OX и OY


def trim_x(n_1, n_2, image):
    image = image
    x, y = image.size
    if n_1.isdigit():
        if int(n_1) < x:
            n_1 = int(n_1)
        else:
            n_1 = 0
    else:
        n_1 = 0
    if n_2.isdigit():
        if x - int(n_2) > int(n_1):
            n_2 = x - int(n_2)
        else:
            n_2 = n_1 + 1
    else:
        n_2 = x
    image = image.crop((n_1, 0, n_2, y))
    return image


def trim_y(n_1, n_2, image):
    image = image
    x, y = image.size

    if n_1.isdigit():
        if int(n_1) < y:
            n_1 = int(n_1)
        else:
            n_1 = 0
    else:
        n_1 = 0
    if n_2.isdigit():
        if x - int(n_2) > int(n_1):
            n_2 = y - int(n_2)
        else:
            n_2 = n_1 + 1
    else:
        n_2 = y
    image = image.crop((0, n_1, x, n_2))
    return image
