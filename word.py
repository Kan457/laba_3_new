import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt6.QtGui import QColor, QFont


class WordTrainer(QWidget):
    def __init__(self):
        super().__init__()
        self.words = []
        self.current_index = 0
        self.error_count = 0
        self.load_words()
        self.init_ui()
        self.show_next_word()

    def load_words(self):
        """Считывает слова из text.txt"""
        try:
            with open("word.txt", "r", encoding="utf-8") as f:
                text = f.read()
            self.words = text.split()
        except FileNotFoundError:
            self.words = ["Файл", "word.txt", "не", "найден"]

    def init_ui(self):
        layout = QVBoxLayout()

        self.word_label = QLabel("")
        self.word_label.setFont(QFont("Arial", 24))
        self.word_label.setStyleSheet("color: black;")

        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Arial", 18))
        self.input_field.returnPressed.connect(self.check_word)
        self.input_field.textEdited.connect(self.check_live_typing)

        self.feedback_label = QLabel("")
        self.feedback_label.setFont(QFont("Arial", 16))

        self.error_label = QLabel("Ошибок: 0")
        self.error_label.setFont(QFont("Arial", 14))

        layout.addWidget(QLabel("Введите слово:"))
        layout.addWidget(self.word_label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.feedback_label)
        layout.addWidget(self.error_label)

        self.setLayout(layout)
        self.setWindowTitle("Тренажёр набора слов")

    def show_next_word(self):
        """Показывает следующее слово"""
        if self.current_index < len(self.words):
            self.word_label.setText(self.words[self.current_index])
            self.feedback_label.setText("")
            self.input_field.clear()
            self.input_field.setStyleSheet("color: black;")
        else:
            self.word_label.setText("✅ Тренировка завершена")
            self.input_field.setDisabled(True)
            self.feedback_label.setText(f"Ошибок всего: {self.error_count}")

    def check_live_typing(self):
        """Подсветка зелёным/красным во время набора"""
        current_word = self.words[self.current_index]
        typed = self.input_field.text()

        if typed == current_word[:len(typed)]:
            self.input_field.setStyleSheet("color: green;")
        else:
            self.input_field.setStyleSheet("color: red;")

    def check_word(self):
        """Проверяет введённое слово при нажатии Enter"""
        current_word = self.words[self.current_index]
        typed = self.input_field.text().strip()

        if typed == current_word:
            self.feedback_label.setText("✅ Верно!")
            self.feedback_label.setStyleSheet("color: green;")
            self.current_index += 1
            self.show_next_word()
        else:
            self.feedback_label.setText("❌ Ошибка!")
            self.feedback_label.setStyleSheet("color: red;")
            self.error_count += 1
            self.error_label.setText(f"Ошибок: {self.error_count}")
            self.input_field.selectAll()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WordTrainer()
    window.resize(500, 300)
    window.show()
    sys.exit(app.exec())
