import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QPushButton
from PyQt6.QtGui import QMovie, QFont
from PyQt6.QtCore import Qt
from test import TypingTrainer
from word import WordTrainer

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно приложения")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: white;")

        window_width = 400
        window_height = 300
        gif_height = 150

        # === ТЕКСТ ВВЕРХУ ===
        self.title_label = QLabel("Клавиатурный тренажёр", self)
        self.title_label.setFont(QFont("Segoe Script", 16, QFont.Weight.Bold))
        self.title_label.setGeometry(0, 10, window_width, 30)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # === КНОПКИ ПОД ТЕКСТОМ ===
        button_width = 180
        button_height = 30
        space_between = 20
        y_buttons = 10 + 30 + 25

        button_font = QFont("Segoe Script", 12, QFont.Weight.Bold)  # Шрифт для кнопок

        # Левая кнопка: "Пройти обучение"
        x_left = (window_width - (2 * button_width + space_between)) // 2
        self.button_train = QPushButton("Пройти обучение", self)
        self.button_train.setGeometry(x_left, y_buttons, button_width, button_height)
        self.button_train.setFont(button_font)
        self.button_train.clicked.connect(self.open_word_trainer)

        # Правая кнопка: "Пройти тест"
        x_right = x_left + button_width + space_between
        self.button_test = QPushButton("Пройти тест", self)
        self.button_test.setGeometry(x_right, y_buttons, button_width, button_height)
        self.button_test.setFont(button_font)
        self.button_test.clicked.connect(self.open_typing_trainer)

        # === GIF СНИЗУ ===
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, window_height - gif_height, window_width, gif_height)
        self.movie = QMovie("cat_code.gif")
        self.movie.setScaledSize(self.image_label.size())
        self.image_label.setMovie(self.movie)
        self.movie.start()
        self.image_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Чтобы окно принимало клавиши
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    # === Обработка клавиш ===
    def keyPressEvent(self, event):
        key = event.text()
        print(f"Нажата клавиша: {key}")
        if key == " ":
            QMessageBox.information(self, "Пробел", "Ты нажал пробел!")

    # === Методы открытия окон ===
    def open_word_trainer(self):
        self.trainer_window = WordTrainer()
        self.trainer_window.show()
        self.close()

    def open_typing_trainer(self):
        self.test_window = TypingTrainer()
        self.test_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
