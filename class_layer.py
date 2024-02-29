from PIL import Image
from PIL import ImageDraw


class Layer:
    def __init__(self, is_image, image,  x, y, r, g, b, transparency):
        if is_image:
            self.image = image
            x, y = image.size
            self.x = x
            self.y = y
            self.pixels = image.load()
        else:
            self.color = (r, g, b, transparency)
            self.image = Image.new("RGBA", (x, y), self.color)
            self.pixels = self.image.load()
            self.x = x
            self.y = y

    def inf_size(self):
        return [self.x, self.y]

    def inf_pixel(self, x, y):
        return self.pixels[x, y]

    def get_image(self):
        return self.image

    def inf_pixels(self):
        return self.pixels

    def change_pixel(self, r, x, y, rgb):
        draw = ImageDraw.Draw(self.image)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(rgb))
        # self.pixels[x, y] = rgba

    def change_image(self, image):
        self.image = image
        x, y = image.size
        self.x = x
        self.y = y
        self.pixels = image.load()

    def paste_image(self, image):
        self.image.paste(image, (0, 0))
        self.pixels = image.load()


