from PIL import Image
# здесь написаны функции для отражения и поворота изображения


def vertical_mirror(image):
    im = image
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im.save("image_process_save.png")
    return im


def horizontal_mirror(image):
    im = image
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im = im.transpose(Image.ROTATE_180)
    im.save("image_process_save.png")
    return im


def turn_right(image):
    image = image
    image = image.transpose(Image.ROTATE_270)
    image.save("image_process_save.png")
    return image


def turn_left(image):
    image = image
    image = image.transpose(Image.ROTATE_90)
    image.save("image_process_save.png")
    return image
