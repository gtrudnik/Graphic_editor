from PIL import Image


# здесь написаны все фильтры изображений


def filter_black_white(image):
    image = image
    pixels = image.load()
    x1, y1 = image.size
    for i in range(x1):
        for j in range(y1):
            if len(pixels[i, j]) == 3:
                r1, g1, b1 = pixels[i, j]
                o = 1
            elif len(pixels[i, j]) == 4:
                r1, g1, b1, o = pixels[i, j]
            if (r1 >= 128 and g1 >= 128) or (b1 >= 128 and g1 >= 128) or (r1 >= 128 and b1 >= 128):
                r = int(255)
                g = int(255)
                b = int(255)
            else:
                r = int(0)
                g = int(0)
                b = int(0)
            pixels[i, j] = r, g, b, o
    return image


def filter_dark(image):
    image = image
    pixels = image.load()
    x1, y1 = image.size
    for i in range(x1):
        for j in range(y1):
            if len(pixels[i, j]) == 3:
                r1, g1, b1 = pixels[i, j]
                o = 1
            elif len(pixels[i, j]) == 4:
                r1, g1, b1, o = pixels[i, j]
            r = int(0.2 * r1)
            g = int(0.2 * g1)
            b = int(0.2 * b1)
            pixels[i, j] = r, g, b, o
    return image


def more_red(image):
    image = image
    pixels = image.load()
    x1, y1 = image.size
    for i in range(x1):
        for j in range(y1):
            if len(pixels[i, j]) == 3:
                r1, g1, b1 = pixels[i, j]
                o = 1
            elif len(pixels[i, j]) == 4:
                r1, g1, b1, o = pixels[i, j]
            pixels[i, j] = 255, g1, b1, o
    return image


def more_green(image):
    image = image
    pixels = image.load()
    x1, y1 = image.size
    for i in range(x1):
        for j in range(y1):
            if len(pixels[i, j]) == 3:
                r1, g1, b1 = pixels[i, j]
                o = 1
            elif len(pixels[i, j]) == 4:
                r1, g1, b1, o = pixels[i, j]
            pixels[i, j] = r1, 255, b1, o
    return image


def more_blue(image):
    image = image
    pixels = image.load()
    x1, y1 = image.size
    for i in range(x1):
        for j in range(y1):
            if len(pixels[i, j]) == 3:
                r1, g1, b1 = pixels[i, j]
                o = 1
            elif len(pixels[i, j]) == 4:
                r1, g1, b1, o = pixels[i, j]
            pixels[i, j] = r1, g1, 255, o
    return image


def contrast(image):
    image = image
    pixels = image.load()
    x1, y1 = image.size
    for i in range(x1):
        for j in range(y1):
            if len(pixels[i, j]) == 3:
                r1, g1, b1 = pixels[i, j]
                o = 1
            elif len(pixels[i, j]) == 4:
                r1, g1, b1, o = pixels[i, j]
            if r1 >= g1 and r1 >= b1:
                pixels[i, j] = 255, 0, 0, o
            elif g1 >= r1 and g1 >= b1:
                pixels[i, j] = 0, 255, 0, o
            elif b1 >= r1 and b1 >= g1:
                pixels[i, j] = 0, 0, 255, o
    image.save("image_process_save.png")
    return image


def only_red(image):
    image = image
    pixels = image.load()
    x1, y1 = image.size
    for i in range(x1):
        for j in range(y1):
            if len(pixels[i, j]) == 3:
                r1, g1, b1 = pixels[i, j]
                o = 1
            elif len(pixels[i, j]) == 4:
                r1, g1, b1, o = pixels[i, j]
            pixels[i, j] = r1, 0, 0, o
    return image


def only_green(image):
    image = image
    pixels = image.load()
    x1, y1 = image.size
    for i in range(x1):
        for j in range(y1):
            if len(pixels[i, j]) == 3:
                r1, g1, b1 = pixels[i, j]
                o = 1
            elif len(pixels[i, j]) == 4:
                r1, g1, b1, o = pixels[i, j]
            pixels[i, j] = 0, g1, 0, o
    return image


def only_blue(image):
    image = image
    pixels = image.load()
    x1, y1 = image.size
    for i in range(x1):
        for j in range(y1):
            if len(pixels[i, j]) == 3:
                r1, g1, b1 = pixels[i, j]
                o = 1
            elif len(pixels[i, j]) == 4:
                r1, g1, b1, o = pixels[i, j]
            pixels[i, j] = 0, 0, b1, o
    return image
