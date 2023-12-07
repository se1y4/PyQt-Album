import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap

class InteractiveAlbum(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Интерактивный альбом")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.image_label = QLabel()
        self.image_label.setFixedSize(300, 300)
        self.layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        self.btn_layout = QHBoxLayout()
        self.prev_button = QPushButton("Предыдущее")
        self.prev_button.clicked.connect(self.show_prev_image)
        self.btn_layout.addWidget(self.prev_button)
        self.next_button = QPushButton("Следующее")
        self.next_button.clicked.connect(self.show_next_image)
        self.btn_layout.addWidget(self.next_button)
        self.layout.addLayout(self.btn_layout)

        self.images = ["image1.jpg", "image2.jpg", "image3.jpg"]  # Список изображений
        self.current_image_index = 0
        self.show_image()

    def show_image(self):
        pixmap = QPixmap(self.images[self.current_image_index])
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def show_prev_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.images)
        self.show_image()

    def show_next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.show_image()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InteractiveAlbum()
    window.show()
    sys.exit(app.exec())