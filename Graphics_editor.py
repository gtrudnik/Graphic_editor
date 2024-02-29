from PyQt5.QtWidgets import QFileDialog, QComboBox
from PyQt5.QtWidgets import QPushButton, QColorDialog, QLineEdit, QScrollBar
from filters import contrast, more_blue, more_green, more_red, filter_dark, filter_black_white
from filters import only_blue, only_green, only_red
from mirror_turn_right_left import vertical_mirror, horizontal_mirror, turn_left, turn_right
from transparency_blur import transparency, blur
from trim_x_y import trim_x, trim_y
from PIL import Image, ImageQt, ImageDraw
from const import language_translate, max_showing_image_size
import sys
from PyQt5.QtWidgets import QWidget, QSlider, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtGui import QPainter, QCursor
from AddlayerWIndow import AddLayerWindow, layers
from PyQt5.QtWidgets import QApplication, QMessageBox
import copy
x_max, y_max = max_showing_image_size


#def draw_cursor(size):
#    circle = Image.new("RGBA", (size, size), (255, 255, 255, 0))
#    ImageDraw.Draw(circle).ellipse(((0, 0), (size, size)), outline='white')
#    return circle


class UiMainWindow(QWidget):
    def __init__(self, first_layer):
        super().__init__()
        self.first_layer = first_layer
        self.setMouseTracking(True)
        # self.circle_cursor = QLabel(self)
        if 'первый слой' not in layers.keys():
            layers['первый слой'] = self.first_layer
        self.used_layers = ['первый слой']
        self.initUI()
        self.language = 0
        self.is_first = True
        self.possibility_step_back = False
        self.number_image = 0
        imageee = layers.get('первый слой').get_image()
        imageee = copy.copy(imageee)
        self.images_change = [{'первый слой': imageee}]
        self.lbl = QLabel(self)
        self.color_draw = (255, 255, 255)
        self.drawing = False
        self.radius = 50
        self.x = -300
        self.y = -300

        #self.cursor_drawing = draw_cursor(50)
        self.show_image()

    def initUI(self):
        imageee = layers.get('первый слой').get_image()
        imageee = copy.copy(imageee)
        x, y = imageee.size
        x_scroll_bar = x - x_max if x - x_max > 0 else 0
        y_scroll_bar = y - y_max if y - y_max > 0 else 0

        self.setGeometry(400, 400, 900, 900)
        self.setWindowTitle(language_translate.get('Graphics editor')[0])

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(35, 35, 35))
        self.setPalette(p)

        self.pushButton_open_file = QPushButton(language_translate.get('open file')[0], self)
        self.pushButton_open_file.resize(120, 30)
        self.pushButton_open_file.move(10, 10)
        self.pushButton_open_file.clicked.connect(self.open_path)

        self.pushButton_save_file = QPushButton(language_translate.get('save')[0], self)
        self.pushButton_save_file.resize(120, 30)
        self.pushButton_save_file.move(130, 10)
        self.pushButton_save_file.pressed.connect(self.save_path)

        self.pushButton_choose_language = QPushButton(language_translate.get('language')[0], self)
        self.pushButton_choose_language.resize(175, 30)
        self.pushButton_choose_language.move(250, 10)
        self.pushButton_choose_language.pressed.connect(self.choose_language)

        self.lineEdit_blur = QLineEdit('', self)
        self.lineEdit_blur.setPlaceholderText(language_translate.get('blur radius')[0])
        self.lineEdit_blur.resize(183, 20)
        self.lineEdit_blur.move(8, 80)
        self.lineEdit_blur.setObjectName("lineEdit")

        self.pushButton_blur = QPushButton(language_translate.get('blur')[0], self)
        self.pushButton_blur.resize(200, 30)
        self.pushButton_blur.move(0, 50)
        self.pushButton_blur.pressed.connect(lambda: self.choose_function("blur"))

        self.pushButton_step_back = QPushButton(language_translate.get('step back')[0], self)
        self.pushButton_step_back.resize(105, 30)
        self.pushButton_step_back.move(430, 10)
        self.pushButton_step_back.pressed.connect(self.step_back)

        self.pushButton_step_forward = QPushButton(language_translate.get('step forward')[0], self)
        self.pushButton_step_forward.resize(105, 30)
        self.pushButton_step_forward.move(530, 10)
        self.pushButton_step_forward.pressed.connect(self.step_forward)

        self.pushButton_vertical_mirror = QPushButton(language_translate.get('vertical mirror')[0], self)
        self.pushButton_vertical_mirror.resize(200, 30)
        self.pushButton_vertical_mirror.move(0, 105)
        self.pushButton_vertical_mirror.pressed.connect(lambda: self.choose_function("vertical_mirror"))

        self.pushButton_horizontal_mirror = QPushButton(language_translate.get('horizontal mirror')[0], self)
        self.pushButton_horizontal_mirror.resize(200, 30)
        self.pushButton_horizontal_mirror.move(0, 130)
        self.pushButton_horizontal_mirror.pressed.connect(lambda: self.choose_function("horizontal_mirror"))

        self.pushButton_transparency = QPushButton(language_translate.get('transparency')[0], self)
        self.pushButton_transparency.resize(200, 30)
        self.pushButton_transparency.move(0, 160)
        self.pushButton_transparency.pressed.connect(lambda: self.choose_function("transparency"))

        self.lineEdit_transparency = QLineEdit('', self)
        self.lineEdit_transparency.setPlaceholderText(language_translate.get('transparency percentage')[0])
        self.lineEdit_transparency.resize(183, 20)
        self.lineEdit_transparency.move(8, 190)
        self.lineEdit_transparency.setObjectName("lineEdit")

        self.pushButton_filters = QPushButton(language_translate.get('filter')[0], self)
        self.pushButton_filters.move(0, 215)
        self.pushButton_filters.resize(200, 30)
        self.pushButton_filters.pressed.connect(self.filters)

        self.comboBox_filters = QComboBox(self)
        self.comboBox_filters.move(0, 240)
        self.comboBox_filters.resize(200, 30)
        self.comboBox_filters.setObjectName("comboBox")
        self.comboBox_filters.addItems(['black & white',
                                        'contrast',
                                        'more red',
                                        'more green',
                                        'more blue',
                                        'dark',
                                        'only red',
                                        'only green',
                                        'only blue'])

        self.pushButton_x_axis = QPushButton(language_translate.get('trim along the x-axis')[0], self)
        self.pushButton_x_axis.move(0, 270)
        self.pushButton_x_axis.resize(200, 30)
        self.pushButton_x_axis.pressed.connect(lambda: self.choose_function("trim_x"))

        self.lineEdit_x_axis_left = QLineEdit('', self)
        self.lineEdit_x_axis_left.setPlaceholderText(language_translate.get('pixels left')[0])
        self.lineEdit_x_axis_left.resize(183, 20)
        self.lineEdit_x_axis_left.move(8, 300)
        self.lineEdit_x_axis_left.setObjectName("lineEdit")

        self.lineEdit_x_axis_right = QLineEdit('', self)
        self.lineEdit_x_axis_right.setPlaceholderText(language_translate.get('pixels right')[0])
        self.lineEdit_x_axis_right.resize(183, 20)
        self.lineEdit_x_axis_right.move(8, 325)
        self.lineEdit_x_axis_right.setObjectName("lineEdit")

        self.pushButton_y_axis = QPushButton(language_translate.get('trim along the y-axis')[0], self)
        self.pushButton_y_axis.move(0, 350)
        self.pushButton_y_axis.resize(200, 30)
        self.pushButton_y_axis.pressed.connect(lambda: self.choose_function("trim_y"))

        self.lineEdit_y_axis_top = QLineEdit('', self)
        self.lineEdit_y_axis_top.setPlaceholderText(language_translate.get('pixels on top')[0])
        self.lineEdit_y_axis_top.resize(183, 20)
        self.lineEdit_y_axis_top.move(8, 380)
        self.lineEdit_y_axis_top.setObjectName("lineEdit")

        self.lineEdit_y_axis_bottom = QLineEdit('', self)
        self.lineEdit_y_axis_bottom.setPlaceholderText(language_translate.get('pixels bottom')[0])
        self.lineEdit_y_axis_bottom.resize(183, 20)
        self.lineEdit_y_axis_bottom.move(8, 405)
        self.lineEdit_y_axis_bottom.setObjectName("lineEdit")

        self.pushButton_turn_right = QPushButton(language_translate.get('turn right')[0], self)
        self.pushButton_turn_right.move(490, 50 + y_max + 25)
        self.pushButton_turn_right.resize(200, 30)
        self.pushButton_turn_right.pressed.connect(lambda: self.choose_function("turn_right"))

        self.pushButton_turn_left = QPushButton(language_translate.get('turn left')[0], self)
        self.pushButton_turn_left.move(710, 50 + y_max + 25)
        self.pushButton_turn_left.resize(200, 30)
        self.pushButton_turn_left.pressed.connect(lambda: self.choose_function("turn_left"))

        self.information_label = QLabel(self)
        self.information_label.setText("")
        self.information_label.move(10, 505)

        self.information_size = QLabel(self)
        self.information_size.setText("")
        self.information_size.move(10, 525)

        self.sld_y = QScrollBar(self)
        self.sld_y.move(200 + x_max + 5, 53)
        self.sld_y.resize(15, y_max)
        self.sld_y.setMinimum(0)
        self.sld_y.setMaximum(y_scroll_bar)
        self.sld_y.setValue(y_scroll_bar // 2)
        self.sld_y.valueChanged.connect(self.chval)
        # self.sld.setTickPosition(QSlider.TicksBelow)
        # self.sld.setTickInterval(5)
        # self.sld.valueChanged.connect(self.change_opacity)

        self.sld_x = QScrollBar(Qt.Horizontal, self)
        self.sld_x.move(200, y_max + 53 + 5)
        self.sld_x.resize(x_max, 15)
        self.sld_x.setMinimum(0)
        self.sld_x.setMaximum(x_scroll_bar)
        self.sld_x.setValue(x_scroll_bar // 2)
        self.sld_x.valueChanged.connect(self.chval)

        self.pushButton_draw = QPushButton(language_translate.get('turn on draw')[0], self)
        self.pushButton_draw.move(650, 10)
        self.pushButton_draw.resize(150, 30)
        self.pushButton_draw.pressed.connect(self.change_draw)

        self.pushButton_colour = QPushButton(language_translate.get('color')[0], self)
        self.pushButton_colour.move(800, 10)
        self.pushButton_colour.resize(100, 30)
        self.pushButton_colour.pressed.connect(self.color)

        self.pushButton_add_layer = QPushButton(language_translate.get('add layer')[0], self)
        self.pushButton_add_layer.move(0, 430)
        self.pushButton_add_layer.resize(200, 30)
        self.pushButton_add_layer.pressed.connect(self.add_layer)

        self.pushButton_delete_layer = QPushButton(language_translate.get('delete layer')[0], self)
        self.pushButton_delete_layer.move(0, 480)
        self.pushButton_delete_layer.resize(200, 30)
        self.pushButton_delete_layer.pressed.connect(self.delete_layer)

        self.comboBox_layers = QComboBox(self)
        self.comboBox_layers.move(0, 455)
        self.comboBox_layers.resize(200, 30)
        self.comboBox_layers.setObjectName("comboBox")
        self.comboBox_layers.addItems(layers.keys())

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.move(900, 15)
        self.sld.setMinimum(1)
        self.sld.setMaximum(100)
        self.sld.setValue(50)
        self.sld.valueChanged.connect(self.change_radius)

        #pixmap = QPixmap(ImageQt.toqpixmap(draw_cursor(50)))
        #self.circle_cursor.setPixmap(pixmap)
        #self.circle_cursor.move(0, 0)
        #self.circle_cursor.resize(50, 50)

    def keyPressEvent(self, event):
        if event.key() == (Qt.Key_Control and Qt.Key_Z):
            self.step_back()


    def delete_layer(self):
        if self.comboBox_layers.currentText() != 'первый слой':
            del layers[self.comboBox_layers.currentText()]
            self.comboBox_layers.clear()
            self.comboBox_layers.addItems(layers.keys())
            self.show_image()

    def chval(self):
        if self.drawing:
            self.show_image()

    def change_draw(self):
        if self.drawing:
            self.pushButton_draw.setText(language_translate.get('turn on draw')[self.language])
            self.drawing = False

            layer_name = self.comboBox_layers.currentText()
            layer = layers.get(layer_name)
            image = layer.get_image()
            image = copy.copy(image)
            self.possibility_step_back = True
            self.number_image += 1
            image2 = image
            self.images_change.append({layer_name: image2})
            self.check_len_images()
            self.sld_y.setValue(y_max // 2)
            self.sld_x.setValue(x_max // 2)
            self.setCursor(QCursor(Qt.ArrowCursor))
            # сюда дописать код который будет добавлять изменения изображения
        else:
            self.setCursor(QCursor(Qt.CrossCursor))
            self.pushButton_draw.setText(language_translate.get('turn off draw')[self.language])
            self.drawing = True
            self.sld_y.setValue(0)
            self.sld_x.setValue(0)

        self.show_image()

    def change_radius(self):
        self.radius = self.sld.value()
        #pixmap = QPixmap(ImageQt.toqpixmap(draw_cursor(self.radius)))
        #self.circle_cursor.setPixmap(pixmap)
        #self.circle_cursor.resize(self.circle_cursor.sizeHint())


    def mouseMoveEvent(self, event):
        #x = event.x()
        #y = event.y()
        #print(x, y, self.drawing)
        #if self.drawing:
        #    self.circle_cursor.move(x - (self.radius // 2), y - (self.radius // 2))
        #    self.x = x
        #    self.y = y
        #    print(0)
        #else:
        #    self.circle_cursor.move(-300, -300)
        if self.drawing:
            x, y = event.x(), event.y()
            print(0)
            if 200 <= x <= 200 + x_max and 53 <= y <= 53 + y_max:
                layer = self.comboBox_layers.currentText()
                layer = layers.get(layer)
                layer.change_pixel(self.radius, x - 200 + self.sld_x.value(), y - 53 + self.sld_y.value(), self.color_draw)
                self.show_image()


    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("You sure?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def add_layer(self):
        self.new_project_window = AddLayerWindow('Add layer')
        code = self.new_project_window.exec_()
        self.refresh_layers()

    def refresh_layers(self):
        self.comboBox_layers.clear()
        self.comboBox_layers.addItems(layers.keys())
        self.show_image()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawFlag(qp)
        qp.end()

    def drawFlag(self, qp):
        qp.setBrush(QColor(200, 200, 200))
        qp.drawRect(200, 53, x_max, y_max)

    def color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_draw = color.getRgb()

    def check_len_images(self):
        if len(self.images_change) == 30:
            self.images_change = self.images_change[1:]
            self.number_image -= 1

    def show_image(self):
        self.is_first = False
        layers_showing = list(layers.values())
        size = layers_showing[0].inf_size()
        if self.drawing:
            x = x_max
            y = y_max
        else:
            x = size[0]
            y = size[1]
        image_showing = Image.new("RGBA", (x, y), (255, 255, 255, 0))
        for i in layers_showing:
            im = i.get_image()
            if self.drawing:
                im = im.crop((self.sld_x.value(), self.sld_y.value(),
                              self.sld_x.value() + x_max, self.sld_y.value() + y_max))
                #im = trim_x(str(self.sld_x.value()), str(-1),  im)
                #im = trim_y(str(self.sld_x.value()), str(-1), im)
            image_showing.paste(im, (0, 0))
        image = image_showing
        pixels = image.load()
        x, y = image.size
        x_inf = x
        y_inf = y
        k = 1

        # этот участок кода отвечает за то, что, если изображения очень большое
        # то оно всё равно выведится в пределах экрана
        if not self.drawing:
            if x // k > x_max or y // k > y_max:
                while x // k > x_max or y // k > y_max:
                    k += 1
                new_color = (256, 256, 256)
                image_mini = Image.new("RGBA", (x // k, y // k), new_color)
                pixels_2 = image_mini.load()
                for i in range(0, x // k):
                    for j in range(0, y // k):
                        pixels_2[i, j] = pixels[i * k, j * k]
                image = image_mini.copy()
                x, y = image_mini.size
        pixmap = QPixmap(ImageQt.toqpixmap(image))
        self.lbl.setPixmap(pixmap)

        if self.drawing:
            self.lbl.move(200, 53)
        else:
            self.lbl.move(200 + x_max // 2 - x // 2, 53 + y_max // 2 - y // 2)
        self.lbl.resize(self.lbl.sizeHint())


        # информация об изображении
        self.information_label.setText(language_translate.get('information')[self.language])
        self.information_label.resize(self.information_label.sizeHint())

        self.information_size.setText(f"{language_translate.get('size')[self.language]}: {int(x_inf)}, {int(y_inf)}")
        self.information_size.resize(self.information_size.sizeHint())

    def choose_function(self, name_function):
        # в этой функции идет выбор функции изменения изображения
        if not self.is_first and not self.drawing:
            self.setCursor(QCursor(Qt.WaitCursor))
            layer_name = self.comboBox_layers.currentText()
            layer = layers.get(layer_name)
            image = layer.get_image()
            layer = copy.copy(image)
            if name_function == "vertical_mirror":
                image = vertical_mirror(layer)
            elif name_function == "horizontal_mirror":
                image = horizontal_mirror(layer)
            elif name_function == "transparency" and self.lineEdit_transparency.text().isdigit() and 0 <= int(self.lineEdit_transparency.text()) <= 100:
                image = transparency(int(self.lineEdit_transparency.text()), layer)
            elif name_function == "blur" and self.lineEdit_blur.text().isdigit():
                image = blur(int(self.lineEdit_blur.text()), layer)
            elif name_function == "turn_right":
                image = turn_right(layer)
            elif name_function == "turn_left":
                image = turn_left(layer)
            elif name_function == "trim_x":
                n_1 = self.lineEdit_x_axis_left.text()
                n_2 = self.lineEdit_x_axis_right.text()
                if n_1.isdigit() or n_2.isdigit():
                    image = trim_x(n_1, n_2, layer)
                else:
                    self.setCursor(QCursor(Qt.ArrowCursor))
                    return
            elif name_function == "trim_y":
                n_1 = self.lineEdit_y_axis_top.text()
                n_2 = self.lineEdit_y_axis_bottom.text()
                if n_1.isdigit() or n_2.isdigit():
                    image = trim_y(n_1, n_2, layer)
                else:
                    self.setCursor(QCursor(Qt.ArrowCursor))
                    return
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))
                return
            layer = layers.get(layer_name)
            layer.change_image(image)
            self.images_change.append({layer_name: image})
            self.possibility_step_back = True
            self.number_image += 1
            self.images_change = self.images_change[:self.number_image + 1]
            self.check_len_images()
            self.show_image()
            self.setCursor(QCursor(Qt.ArrowCursor))

    def filters(self):
        # в этой функции выбирается какой фильтр будет применен
        type_filter = self.comboBox_filters.currentText()
        layer = self.comboBox_layers.currentText()
        layer = layers.get(layer)
        image = layer.get_image()
        layer = copy.copy(image)
        if not self.is_first and not self.drawing:
            self.setCursor(QCursor(Qt.WaitCursor))
            self.possibility_step_back = True
            if type_filter == 'black & white':
                image = filter_black_white(layer)
            elif type_filter == 'contrast':
                image = contrast(layer)
            elif type_filter == 'more red':
                image = more_red(layer)
            elif type_filter == 'more green':
                image = more_green(layer)
            elif type_filter == 'more blue':
                image = more_blue(layer)
            elif type_filter == 'only red':
                image = only_red(layer)
            elif type_filter == 'only green':
                image = only_green(layer)
            elif type_filter == 'only blue':
                image = only_blue(layer)
            elif type_filter == 'dark':
                image = filter_dark(layer)
            layer_name = self.comboBox_layers.currentText()
            layer = layers.get(layer_name)
            layer.change_image(image)
            self.images_change.append({layer_name: image})
            self.possibility_step_back = True
            self.number_image += 1
            self.images_change = self.images_change[:self.number_image + 1]
            self.check_len_images()
            self.show_image()
            self.setCursor(QCursor(Qt.ArrowCursor))

    def open_path(self):
        # открытие изображения
        filename = QFileDialog.getOpenFileName(self, 'Open file')[0]
        if filename and ((filename[-3:]) == 'jpg' or (filename[-3:]) == 'png'):
            self.setCursor(QCursor(Qt.WaitCursor))
            image = Image.open(filename)
            self.number_image = 0
            self.images_change = [{layers.get(self.comboBox_layers.currentText()): image}]
            layer = self.comboBox_layers.currentText()
            layer = layers.get(layer)
            layer.paste_image(image)

            self.show_image()
            self.setCursor(QCursor(Qt.ArrowCursor))

    def save_path(self):
        # сохранение изображения
        filename = QFileDialog.getSaveFileName(self, 'Save file', '', '*.png')[0]
        if not self.is_first and filename:
            layers_showing = list(layers.values())
            size = layers_showing[0].inf_size()
            x = size[0]
            y = size[1]
            image = Image.new("RGBA", (x, y), (255, 255, 255, 0))
            for i in layers_showing:
                im = i.get_image()
                image.paste(im, (0, 0))
            image.save(filename)

    def step_back(self):
        # возвращение к изображению находящемуся в списке перед текущим
        if self.possibility_step_back:
            self.number_image -= 1 if self.number_image != 0 else 0

            image = self.images_change[self.number_image]
            layer = list(image.keys())[0]

            layers.get(layer).change_image((image.get(layer)))
            self.show_image()

    def step_forward(self):
        # возвращение к изображению находящемуся в списке полсе текущего
        if self.possibility_step_back:

            self.number_image += 1 if self.number_image < len(self.images_change) - 1 else 0

            image = self.images_change[self.number_image]
            layer = list(image.keys())[0]
            layers.get(layer).change_image((image.get(layer)))
            self.show_image()

    def choose_language(self):
        # перевод названий виджетов
        self.language = 1 if self.language == 0 else 0
        self.setWindowTitle(language_translate.get('Graphics editor')[self.language])
        self.pushButton_open_file.setText(language_translate.get('open file')[self.language])
        self.pushButton_save_file.setText(language_translate.get('save')[self.language])
        self.pushButton_choose_language.setText(language_translate.get('language')[self.language])
        self.pushButton_blur.setText(language_translate.get('blur')[self.language])
        self.lineEdit_blur.setPlaceholderText(language_translate.get('blur radius')[self.language])
        self.pushButton_step_back.setText(language_translate.get('step back')[self.language])
        self.pushButton_vertical_mirror.setText(language_translate.get('vertical mirror')[self.language])
        self.pushButton_horizontal_mirror.setText(language_translate.get('horizontal mirror')[self.language])
        self.pushButton_transparency.setText(language_translate.get('transparency')[self.language])
        self.lineEdit_transparency.setPlaceholderText(language_translate.get('transparency percentage')[self.language])
        self.pushButton_filters.setText(language_translate.get('filter')[self.language])
        self.pushButton_step_forward.setText(language_translate.get('step forward')[self.language])
        self.pushButton_x_axis.setText(language_translate.get('trim along the x-axis')[self.language])
        self.pushButton_y_axis.setText(language_translate.get('trim along the y-axis')[self.language])
        self.lineEdit_x_axis_left.setPlaceholderText(language_translate.get('pixels left')[self.language])
        self.lineEdit_x_axis_right.setPlaceholderText(language_translate.get('pixels right')[self.language])
        self.lineEdit_y_axis_top.setPlaceholderText(language_translate.get('pixels on top')[self.language])
        self.lineEdit_y_axis_bottom.setPlaceholderText(language_translate.get('pixels bottom')[self.language])
        self.pushButton_turn_left.setText(language_translate.get('turn left')[self.language])
        self.pushButton_turn_right.setText(language_translate.get('turn right')[self.language])
        self.pushButton_colour.setText(language_translate.get('color')[self.language])
        self.pushButton_delete_layer.setText(language_translate.get('delete layer')[self.language])
        self.pushButton_add_layer.setText(language_translate.get('add layer')[self.language])

        if self.drawing:
            self.pushButton_draw.setText(language_translate.get('turn off draw')[self.language])
        else:
            self.pushButton_draw.setText(language_translate.get('turn on draw')[self.language])
        # перевод информации об изображении
        if not self.is_first:
            image = Image.open("image_process_save.png")
            x, y = image.size
            self.information_label.setText(language_translate.get('information')[self.language])
            self.information_label.resize(self.information_label.sizeHint())
            self.information_size.setText(f"{language_translate.get('size')[self.language]}: {int(x)}, {int(y)}")
            self.information_size.resize(self.information_size.sizeHint())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = UiMainWindow()
    MainWindow.show()
    sys.exit(app.exec())
