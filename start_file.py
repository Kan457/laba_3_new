import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QMovie, QFont, QPixmap
from PyQt6.QtCore import Qt
from test import TypingTrainer
from word import WordTrainer


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Клавиатурный тренажёр")
        
        # Размер окна
        self.resize(800, 400)
        self.setMinimumSize(600, 300)

        # === ФОН ===
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("f.jpg"))
        self.background_label.setScaledContents(True)
        self.background_label.lower()

        # === GIF слева и справа от заголовка ===
        self.gif_left = QLabel(self)
        self.movie_left = QMovie("g.gif")
        self.gif_left.setMovie(self.movie_left)
        self.gif_left.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.movie_left.start()

        self.gif_right = QLabel(self)
        self.movie_right = QMovie("g.gif")
        self.gif_right.setMovie(self.movie_right)
        self.gif_right.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.movie_right.start()

        # === Заголовок ===
        self.title_label = QLabel("Клавиатурный тренажёр", self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: black; font-weight: bold;")

        # === Кнопки по центру окна ===
        self.button_train = QPushButton("Пройти обучение", self)
        self.button_train.clicked.connect(self.open_word_trainer)
        self.button_train.setStyleSheet("background-color: rgba(255,255,255,180); font-weight: bold;")

        self.button_test = QPushButton("Пройти тест", self)
        self.button_test.clicked.connect(self.open_typing_trainer)
        self.button_test.setStyleSheet("background-color: rgba(255,255,255,180); font-weight: bold;")

        # Первичная расстановка
        self.resizeEvent(None)

    # === Адаптивное позиционирование ===
    def resizeEvent(self, event):
        w = self.width()
        h = self.height()

        # Фон
        self.background_label.setGeometry(0, 0, w, h)

        # Динамический размер шрифта
        title_font_size = max(16, h // 15)
        button_font_size = max(12, h // 20)

        self.title_label.setFont(QFont("Segoe Script", title_font_size, QFont.Weight.Bold))
        self.button_train.setFont(QFont("Segoe Script", button_font_size, QFont.Weight.Bold))
        self.button_test.setFont(QFont("Segoe Script", button_font_size, QFont.Weight.Bold))

        # Размер GIF
        gif_width = int(w * 0.08)
        gif_height = int(h * 0.15)

        self.gif_left.setGeometry(20, 20, gif_width, gif_height)
        self.movie_left.setScaledSize(self.gif_left.size())

        self.gif_right.setGeometry(w - gif_width - 20, 20, gif_width, gif_height)
        self.movie_right.setScaledSize(self.gif_right.size())

        # Заголовок между GIF
        title_x = 20 + gif_width + 10
        title_width = w - 2*(gif_width + 20 + 10)
        title_height = gif_height
        self.title_label.setGeometry(title_x, 20, title_width, title_height)

        # Кнопки по центру окна под заголовком
        button_width = int(w * 0.5)
        button_height = int(h * 0.20)
        space_between = int(h * 0.05)
        total_buttons_height = 2 * button_height + space_between
        y_start = title_height + 40  # чуть ниже заголовка
        x_center = (w - button_width) // 2

        self.button_train.setGeometry(x_center, y_start, button_width, button_height)
        self.button_test.setGeometry(x_center, y_start + button_height + space_between, button_width, button_height)

    # Методы открытия окон
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
