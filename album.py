import sys
import time
from datetime import datetime
import os

from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, QInputDialog, QMessageBox, QLineEdit)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, QSettings

from db import add_user, check_password, check_user, create_table

class PhotoAlbum(QMainWindow):
    def __init__(self):
        super().__init__()

        self.lasttime = QLabel()

        self.currTimeLabel = QLabel(datetime.now().strftime("%D %H:%M:%S"))
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeUpdate)
        self.timer.start(1000)

        self.settings = QSettings('Album', "Vadim_Killer", self)
        self.loadSettings()

        self.setWindowTitle('Мой фотоальбом')

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(400, 400)
        self.image_label.setStyleSheet("background-color: #f0f0f0;")

        self.dir_button = QPushButton('Загрузить папку', self)
        self.dir_button.clicked.connect(self.seeAllAlbum)
        self.dir_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 25px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px;")


        self.upload_button = QPushButton('Загрузить фото', self)
        self.upload_button.clicked.connect(self.upload_photo)
        self.upload_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 25px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px;")

        self.login_button = QPushButton('Войти', self)
        self.login_button.clicked.connect(self.login)
        self.signup_button = QPushButton('Зарегистрироваться', self)
        self.signup_button.clicked.connect(self.signup)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.upload_button)
        main_layout.addWidget(self.dir_button)
        main_layout.addWidget(self.login_button)
        main_layout.addWidget(self.signup_button)
        main_layout.addWidget(self.currTimeLabel)
        main_layout.addWidget(self.lasttime)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def upload_photo(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter('Images (*.png *.jpg *.jpeg *.bmp)')
        file_dialog.setViewMode(QFileDialog.Detail)

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            image = QPixmap(file_path)
            self.image_label.setPixmap(image)

    def signup(self):
        username, ok = QInputDialog.getText(self, 'Регистрация', 'Введите имя пользователя:')
        if ok:
            password, ok = QInputDialog.getText(self, 'Регистрация', 'Введите пароль:', QLineEdit.Password)
            if ok:
                create_table()
                add_user(username, password)

    def login(self):
        username, ok = QInputDialog.getText(self, 'Вход', 'Введите имя пользователя:')
        if ok:
            password, ok = QInputDialog.getText(self, 'Вход', 'Введите пароль:', QLineEdit.Password)
            if ok:
                if check_user(username):
                    if check_password(username, password):
                        QMessageBox.information(self, 'Успешный вход', 'Добро пожаловать!')
                    else:
                        QMessageBox.warning(self, 'Ошибка', 'Неверный пароль')
                else:
                    QMessageBox.warning(self, 'Ошибка', 'Пользователь не найден')
    def timeUpdate(self): #Обновление часов
        self.currTimeLabel.setText(datetime.now().strftime("%D %H:%M:%S"))

    def saveSettings(self): #Сохраняет настройки в реестре
        self.settings.setValue('LastTime', int(datetime.timestamp(datetime.now())))

    def loadSettings(self): #Загружает настройки из реестра
        id = self.settings.value('LastTime', 1, type=int)
        self.lasttime.setText(f'Последнее использование:{str(datetime.fromtimestamp(id).strftime("%D %H:%M:%S"))}')

    def closeEvent(self, event): #При закрытии приложения сохраняются настройки
        self.saveSettings()
        event.accept()

    def seeAllAlbum(self):
        img = QFileDialog.getOpenFileNames(self, '1', '2', filter='Images (*.png *.jpg *.jpeg *.bmp)')[0]
        self.timerimg = QTimer()
        self.timerimg.timeout.connect(lambda: self.changeimg(img))
        self.timerimg.start(1000)
        self.index = 0

    def changeimg(self, img):
        image = QPixmap(img[self.index])
        self.index += 1
        self.image_label.setPixmap(image)
        self.index %= len(img)

def show_album():
    app = QApplication(sys.argv)

    authorization_widget = PhotoAlbum()
    authorization_widget.show()

    sys.exit(app.exec_())

show_album()