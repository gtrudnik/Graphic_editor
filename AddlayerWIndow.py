import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QComboBox, QDial, QDialog
from PyQt5.QtWidgets import QPushButton, QColorDialog, QLineEdit, QLabel, QSlider, QScrollBar
from PyQt5.QtGui import QPixmap
from const import language_translate
from PyQt5.QtGui import QPixmap, QPainter, QColor
from class_layer import Layer
from class_layer import Layer
layers = {}


class AddLayerWindow(QDialog):
    def __init__(self, name_of_button):
        super().__init__()
        self.name_of_button = name_of_button
        self.initUI()
        self.color = (255, 255, 255)
        self.working = True

    def initUI(self):
        self.setGeometry(200, 200, 600, 150)
        self.setWindowTitle(language_translate.get('Graphics editor')[0])
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(35, 35, 35))
        self.setPalette(p)

        self.pushButton_add_project = QPushButton(self.name_of_button, self)
        self.pushButton_add_project.resize(200, 30)
        self.pushButton_add_project.move(10, 10)
        self.pushButton_add_project.clicked.connect(self.add_layer)

        self.pushButton_colour = QPushButton('color', self)
        self.pushButton_colour.move(10, 40)
        self.pushButton_colour.resize(200, 30)
        self.pushButton_colour.pressed.connect(self.colour_layer)

        self.line_edit_name = QLineEdit('', self)
        self.line_edit_name.setPlaceholderText('name of layer')
        self.line_edit_name.move(220, 15)
        self.line_edit_name.resize(187, 20)

        self.line_edit_transparency = QLineEdit('', self)
        self.line_edit_transparency.setPlaceholderText(language_translate.get('transparency percentage')[0])
        self.line_edit_transparency.move(220, 45)
        self.line_edit_transparency.resize(187, 20)

        self.line_edit_width = QLineEdit('', self)
        self.line_edit_width.setPlaceholderText('width')
        self.line_edit_width.move(16, 70)
        self.line_edit_width.resize(187, 20)

        self.line_edit_height = QLineEdit('', self)
        self.line_edit_height.setPlaceholderText('height')
        self.line_edit_height.move(220, 70)
        self.line_edit_height.resize(187, 20)

    def colour_layer(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.getRgb()[0:-1]

    def add_layer(self):
        x = self.line_edit_width.text()
        y = self.line_edit_height.text()
        transparency = self.line_edit_transparency.text()
        name = self.line_edit_name.text()
        if x.isdigit() and y.isdigit() and transparency.isdigit() and 0 <= int(transparency) <= 100 and name:
            r, g, b = self.color
            layers[name] = Layer(False, 0, int(x), int(y), r, g, b, int(int(transparency) / 100 * 255))
            AddLayerWindow.close(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = AddLayerWindow('Add layer')
    Window.show()
    sys.exit(app.exec())
