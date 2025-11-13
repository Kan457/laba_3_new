import sys
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QLabel, QPushButton, QMessageBox
from PyQt6.QtGui import QTextCharFormat, QColor, QTextCursor, QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer, QTime, QSettings

# импортируем клавиатуру из отдельного файла
from keyboard import keyboard_buttons  # <-- здесь твой список клавиш

class KeyboardWidget(QWidget):
    """Клавиатура для ввода текста"""
    def __init__(self, parent, input_field):
        super().__init__(parent)
        self.input_field = input_field
        self.buttons = {}
        self.create_keyboard()

    def create_keyboard(self):
        for name, x, y, w, h, color in keyboard_buttons:
            btn = QPushButton(name, self)
            btn.setStyleSheet(f"""
                background-color: {color};
                border-radius: 5px;
                font-weight: bold;
            """)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.clicked.connect(lambda checked, key=name: self.insert_key(key))
            self.buttons[name.upper()] = btn

    def insert_key(self, key):
        cursor = self.input_field.textCursor()
        if key == "Backspace":
            cursor.deletePreviousChar()
        elif key == "Enter":
            cursor.insertText("\n")
        elif key == "Space":
            cursor.insertText(" ")
        else:
            cursor.insertText(key)
        self.input_field.setTextCursor(cursor)
        # обновляем подсветку текста, если есть метод
        if hasattr(self.input_field.parent(), 'update_display'):
            self.input_field.parent().update_display()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = self.width(), self.height()
        base_w, base_h = 900, 250  # базовые размеры для масштабирования
        for name, x, y, bw, bh, color in keyboard_buttons:
            btn = self.buttons[name.upper()]
            new_x = int(x / base_w * w)
            new_y = int(y / base_h * h)
            new_w = max(int(bw / base_w * w), 30)
            new_h = max(int(bh / base_h * h), 30)
            btn.setGeometry(new_x, new_y, new_w, new_h)


class TypingTrainer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Тренажёр набора текста")
        self.resize(900, 650)
        self.setMinimumSize(600, 400)

        self.original_text = ""
        self.error_count = 0
        self.timer_running = False
        self.time = QTime(0, 0, 0)
        self.best_time = None

        self.settings = QSettings("TypingTrainerCompany", "TypingTrainerApp")

        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("w.jpg"))
        self.background_label.setScaledContents(True)
        self.background_label.lower()

        self.init_ui()
        self.load_text_from_file()
        self.load_record()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        # Клавиатура
        self.keyboard_widget = KeyboardWidget(self, self.user_input)

    def init_ui(self):
        base_font = QFont("Segoe Script", 14)

        self.original_display = QTextEdit(self)
        self.original_display.setReadOnly(True)
        self.original_display.setFont(base_font)

        self.user_input = QTextEdit(self)
        self.user_input.setFont(base_font)
        self.user_input.textChanged.connect(self.update_display)

        self.error_label = QLabel("Ошибок: 0", self)
        self.error_label.setFont(base_font)
        self.timer_label = QLabel("Время: 00:00", self)
        self.timer_label.setFont(base_font)
        self.best_time_label = QLabel("Рекорд: —", self)
        self.best_time_label.setFont(base_font)
        self.best_time_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.exit_button = QPushButton("Выйти", self)
        self.exit_button.setStyleSheet("""
            background-color: black;
            color: white;
            font-weight: bold;
            border-radius: 5px;
        """)
        self.exit_button.clicked.connect(self.close)

    # ---------------- Методы для текста и таймера ----------------
    def load_text_from_file(self):
        try:
            with open("text.txt", "r", encoding="utf-8") as f:
                self.original_text = f.read()
        except FileNotFoundError:
            self.original_text = "Файл text.txt не найден."
        self.original_display.setPlainText(self.original_text)

    def update_display(self):
        user_text = self.user_input.toPlainText()
        if len(user_text) == 1 and not self.timer_running:
            self.start_timer()

        if len(user_text) >= len(self.original_text):
            self.stop_timer()
            msg = QMessageBox(self)
            msg.setWindowTitle("Тест завершён")
            msg.setText(
                f"Вы завершили тест!\n"
                f"Время: {self.time.toString('mm:ss')}\n\n"
                f"Рекорд: {self.best_time.toString('mm:ss') if self.best_time else '—'}"
            )
            msg.exec()
            self.close()

        self.error_count = 0
        fmt_correct = QTextCharFormat()
        fmt_correct.setForeground(QColor("green"))
        fmt_error = QTextCharFormat()
        fmt_error.setForeground(QColor("red"))
        fmt_future = QTextCharFormat()
        fmt_future.setForeground(QColor("gray"))

        cursor = self.original_display.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.setCharFormat(QTextCharFormat())

        for i, char in enumerate(user_text):
            cursor.setPosition(i)
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)
            if i < len(self.original_text) and char == self.original_text[i]:
                cursor.setCharFormat(fmt_correct)
            else:
                cursor.setCharFormat(fmt_error)
                self.error_count += 1

        if len(user_text) < len(self.original_text):
            cursor.setPosition(len(user_text))
            cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
            cursor.setCharFormat(fmt_future)

        self.error_label.setText(f"Ошибок: {self.error_count}")

    def start_timer(self):
        if not self.timer_running:
            self.time = QTime(0, 0, 0)
            self.timer.start(1000)
            self.timer_running = True

    def update_timer(self):
        self.time = self.time.addSecs(1)
        self.timer_label.setText(f"Время: {self.time.toString('mm:ss')}")

    def stop_timer(self):
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False
            self.check_record()

    def load_record(self):
        record_str = self.settings.value("best_time", "")
        if record_str:
            self.best_time = QTime.fromString(record_str, "mm:ss")
        else:
            self.best_time = None
        if self.best_time:
            self.best_time_label.setText(f"Рекорд: {self.best_time.toString('mm:ss')}")

    def save_record(self):
        if self.best_time:
            self.settings.setValue("best_time", self.best_time.toString("mm:ss"))

    def check_record(self):
        if self.error_count > 0:
            return
        if not self.best_time or self.time < self.best_time:
            self.best_time = self.time
            self.save_record()
            self.best_time_label.setText(f"Рекорд: {self.best_time.toString('mm:ss')}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = self.width(), self.height()
        self.background_label.setGeometry(0, 0, w, h)

        top_height = h // 3
        self.original_display.setGeometry(10, 10, w - 20, top_height)
        input_height = h // 12
        self.user_input.setGeometry(10, 20 + top_height, w - 20, input_height)

        label_y = 30 + top_height + input_height
        self.error_label.setGeometry(10, label_y, w // 4, 30)
        self.timer_label.setGeometry(w // 4, label_y, w // 4, 30)
        self.best_time_label.setGeometry(w // 2, label_y, w // 2 - 20, 30)
        self.exit_button.setGeometry(w - 110, label_y, 100, 30)

        keyboard_top = label_y + 50
        keyboard_height = h - keyboard_top - 10
        self.keyboard_widget.setGeometry(0, keyboard_top, w, keyboard_height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingTrainer()
    window.show()
    sys.exit(app.exec())
