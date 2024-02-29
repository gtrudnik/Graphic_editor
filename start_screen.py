# pyinstaller --onefile --noconsole --exclude-module tkinter start_screen.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QComboBox, QDial
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QSlider, QScrollBar
from PyQt5.QtGui import QPixmap
from const import language_translate
from Graphics_editor import UiMainWindow
from add_project_window import AddProjectWindow
from PyQt5.QtGui import QPixmap, QPainter, QColor


class Start_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 600, 150)
        self.setWindowTitle(language_translate.get('Graphics editor')[0])
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(35, 35, 35))
        self.setPalette(p)

        self.pushButton_add_project = QPushButton('Add project', self)
        self.pushButton_add_project.resize(150, 50)
        self.pushButton_add_project.move(50, 20)
        self.pushButton_add_project.clicked.connect(self.add_project)

        self.pushButton_add_project = QPushButton('Open project', self)
        self.pushButton_add_project.resize(150, 50)
        self.pushButton_add_project.move(200, 20)
        self.pushButton_add_project.clicked.connect(self.open_project)

        self.comboBox_projects = QComboBox(self)
        self.comboBox_projects.move(50, 75)
        self.comboBox_projects.resize(400, 30)
        self.comboBox_projects.setObjectName("comboBox")
        self.comboBox_projects.addItems([])

    def add_project(self):
        self.Window = AddProjectWindow('Add project')
        self.Window.exec_()
        from AddlayerWIndow import layers
        if layers:
            Start_Window.close(self)
        else:
            pass

    def open_project(self):
        pass
        # MainWindow = UiMainWindow()
        # MainWindow.show()
        # Start_Window.close(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Start_Window()
    MainWindow.show()
    sys.exit(app.exec())
