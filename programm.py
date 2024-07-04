import cv2

from PyQt5 import uic
from PyQt5.Qt import *


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_design.ui', self)
        self.pushButton.clicked.connect(self.choose)
        self.pushButton_2.clicked.connect(self.webcam)
        self.pushButton_3.clicked.connect(self.average)
        self.pushButton_4.clicked.connect(self.draw)
        self.pushButton_5.clicked.connect(self.gray)
        self.pushButton_6.clicked.connect(self.save)

        self.radioButton.clicked.connect(self.change_channel)
        self.radioButton_2.clicked.connect(self.change_channel)
        self.radioButton_3.clicked.connect(self.change_channel)
        self.radioButton_4.clicked.connect(self.change_channel)

        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_video_stream)

        self.current_image = None
        self.original_image = None
        self.channel = 'all'

    def choose(self):
        try:
            file_dialog = QFileDialog(self)
            filename, _ = file_dialog.getOpenFileName(self, "Выбрать изображение", "", "Изображения (*.png *.jpg)")
            if filename:
                self.current_image = cv2.imread(filename)
                self.original_image = self.current_image.copy()
                self.display_image(self.current_image)
        except:
            self.statusbar.showMessage('Ошибка! В пути к файлу присутствуют русские буквы!')

    def webcam(self):
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)
        self.pushButton_6.setEnabled(True)

    def display_video_stream(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_image = frame
            self.display_image(frame)

    def save(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_image = frame
            self.original_image = self.current_image.copy()
            self.display_image(frame)
            self.timer.stop()
            self.cap.release()
            self.pushButton_6.setEnabled(False)

    def display_image(self, image):
        if image is not None:
            if self.channel == 'red':
                image = image.copy()
                image[:, :, 0] = 0
                image[:, :, 1] = 0
            elif self.channel == 'green':
                image = image.copy()
                image[:, :, 0] = 0
                image[:, :, 2] = 0
            elif self.channel == 'blue':
                image = image.copy()
                image[:, :, 1] = 0
                image[:, :, 2] = 0

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.imager.setPixmap(pixmap.scaled(self.imager.size(), Qt.KeepAspectRatio))

    def average(self):
        self.statusbar.showMessage('')
        width = self.lineEdit.text()
        height = self.lineEdit_2.text()
        if height == '' or width == '':
            self.statusbar.showMessage('Ошибка! В какой-то из строчек пусто!')
        else:
            try:
                height = int(height)
                width = int(width)
                if height <= 0 or width <= 0:
                    self.statusbar.showMessage('Ошибка! Размер получаемой картинки должен быть больше 0!')
                else:
                    if self.current_image is not None:
                        resized_image = cv2.resize(self.current_image, (width, height))
                        self.display_image(resized_image)
                    else:
                        self.statusbar.showMessage('Ошибка! Картинка не задана!')
            except ValueError:
                self.statusbar.showMessage('Ошибка! Введены некорректные данные!')

    def draw(self):
        x1 = self.lineEdit_3.text()
        y1 = self.lineEdit_4.text()
        x2 = self.lineEdit_5.text()
        y2 = self.lineEdit_6.text()
        if x1 == '' or x2 == '' or y1 == '' or y2 == '':
            self.statusbar.showMessage('Ошибка! Какие-то координаты не заданы!')
        else:
            try:
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)
                if x1 <= 0 or y1 <= 0 or x2 <= 0 or y2 <= 0:
                    self.statusbar.showMessage('Ошибка! Координаты не могут быть отрицательными или равными 0!')
                else:
                    if self.current_image is not None:
                        image = self.current_image.copy()
                        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        self.display_image(image)
                    else:
                        self.statusbar.showMessage('Ошибка! Картинка не задана!')
            except ValueError:
                self.statusbar.showMessage('Ошибка! Введены некорректные данные!')

    def gray(self):
        if self.current_image is not None:
            gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
            self.display_image(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB))
        else:
            self.statusbar.showMessage('Ошибка! Картинка не задана!')

    def change_channel(self):
        if self.radioButton.isChecked():
            self.channel = 'all'
        elif self.radioButton_2.isChecked():
            self.channel = 'red'
        elif self.radioButton_3.isChecked():
            self.channel = 'green'
        elif self.radioButton_4.isChecked():
            self.channel = 'blue'
        if self.current_image is not None:
            self.display_image(self.current_image)

