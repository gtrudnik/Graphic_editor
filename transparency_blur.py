from PIL import Image
from PIL import ImageFilter
# функции управляющие прозрачностью и размытием изображения


def transparency(n, image):
    image = image
    image.putalpha(int(n / 100 * 255))
    image.save("image_process_save.png")
    return image


def blur(n, image):
    image = image
    image = image.filter(ImageFilter.GaussianBlur(radius=n))
    image.save("image_process_save.png")
    return image
