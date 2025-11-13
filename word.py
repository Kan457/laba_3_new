import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QSpacerItem, QSizePolicy, QPushButton
)
from PyQt6.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt
from button import keyboard_buttons  # [(текст, x, y, w, h, color), ...]

class WordTrainer(QWidget):
    def __init__(self):
        super().__init__()
        self.words = []
        self.current_index = 0
        self.error_count = 0
        self.buttons = {}

        self.load_words()
        self.init_ui()
        self.create_keyboard()
        self.show_next_word()
        self.create_exit_button()  # кнопка выхода

    def load_words(self):
        """Считывает слова из word.txt"""
        try:
            with open("word.txt", "r", encoding="utf-8") as f:
                self.words = f.read().split()
        except FileNotFoundError:
            self.words = ["Файл", "word.txt", "не", "найден"]

    def init_ui(self):
        """Создаёт интерфейс"""
        layout = QVBoxLayout()

        # Верхние элементы
        self.word_label = QLabel("")
        self.word_label.setFont(QFont("Arial", 36))
        self.word_label.setStyleSheet("color: black;")
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.prompt_label = QLabel("Введите слово:")
        self.prompt_label.setFont(QFont("Arial", 20))
        self.prompt_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Arial", 22))
        self.input_field.setFixedHeight(40)  # уменьшено
        self.input_field.setFixedWidth(450)  # половина ширины окна
        self.input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_field.returnPressed.connect(self.check_word)
        self.input_field.textEdited.connect(self.check_live_typing)

        self.feedback_label = QLabel("")
        self.feedback_label.setFont(QFont("Arial", 20))
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.error_label = QLabel("Ошибок: 0")
        self.error_label.setFont(QFont("Arial", 18))
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Располагаем выше центра
        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        layout.addWidget(self.word_label)
        layout.addWidget(self.prompt_label)
        layout.addWidget(self.input_field, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feedback_label)
        layout.addWidget(self.error_label)
        layout.addSpacerItem(QSpacerItem(20, 180, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout)
        self.setWindowTitle("Тренажёр набора слов")
        self.setGeometry(100, 100, 900, 700)

        # Фон окна через QPalette
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(QPixmap("j.jpg")))
        self.setPalette(palette)

    def create_keyboard(self):
        """Создаёт виртуальную клавиатуру и располагает её внизу"""
        max_y = max(y + h for _, x, y, w, h, color in keyboard_buttons)
        offset = self.height() - max_y - 40

        for name, x, y, w, h, color in keyboard_buttons:
            btn = QPushButton(name, self)
            btn.setGeometry(x, y + offset, w, h)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: black;
                    border-radius: 5px;
                    font-size: 16px;
                }}
                QPushButton:pressed {{
                    background-color: #444;
                }}
            """)
            self.buttons[name.upper()] = btn

    def create_exit_button(self):
        """Кнопка выхода в главное окно в правом верхнем углу"""
        self.exit_button = QPushButton("Выйти", self)
        self.exit_button.setGeometry(self.width() - 110, 10, 100, 40)
        self.exit_button.setStyleSheet("""
            background-color: black;
            color: white;
            font-weight: bold;
            border-radius: 5px;
        """)
        self.exit_button.clicked.connect(self.go_to_main_app)
        self.exit_button.raise_()  # поверх всех виджетов

    def go_to_main_app(self):
        # Импортируем здесь, чтобы избежать циклического импорта
        from start_file import MyApp
        self.main_window = MyApp()
        self.main_window.show()
        self.close()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.create_keyboard()
        # обновляем положение кнопки выхода при изменении размера
        self.exit_button.setGeometry(self.width() - 110, 10, 100, 40)

    def show_next_word(self):
        if self.current_index < len(self.words):
            self.word_label.setText(self.words[self.current_index])
            self.feedback_label.setText("")
            self.input_field.clear()
            self.input_field.setStyleSheet("color: black;")
        else:
            self.word_label.setText("Тренировка завершена")
            self.input_field.setDisabled(True)
            self.feedback_label.setText(f"Ошибок всего: {self.error_count}")

    def check_live_typing(self):
        current_word = self.words[self.current_index]
        typed = self.input_field.text()
        if typed == current_word[:len(typed)]:
            self.input_field.setStyleSheet("color: green;")
        else:
            self.input_field.setStyleSheet("color: red;")

    def check_word(self):
        current_word = self.words[self.current_index]
        typed = self.input_field.text().strip()
        if typed == current_word:
            self.feedback_label.setText("Верно!")
            self.feedback_label.setStyleSheet("color: green;")
            self.current_index += 1
            self.show_next_word()
        else:
            self.feedback_label.setText("Ошибка!")
            self.feedback_label.setStyleSheet("color: red;")
            self.error_count += 1
            self.error_label.setText(f"Ошибок: {self.error_count}")
            self.input_field.selectAll()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WordTrainer()
    window.show()
    sys.exit(app.exec())
