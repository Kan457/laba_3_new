import sys
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QLabel, QPushButton, QMessageBox
from PyQt6.QtGui import QTextCharFormat, QColor, QTextCursor, QFont, QPixmap, QKeyEvent
from PyQt6.QtCore import Qt, QTimer, QTime, QSettings

# Пример keyboard_buttons
from keyboard import keyboard_buttons  


class KeyboardWidget(QWidget):
    def __init__(self, parent, input_field):
        super().__init__(parent)
        self.input_field = input_field
        self.buttons = {}
        self.key_ids = []
        self.create_keyboard()

    def create_keyboard(self):
        font = QFont("Segoe Script", 12)

        for idx, (name, x, y, w, h, color) in enumerate(keyboard_buttons):
            btn = QPushButton(name, self)
            btn.setFont(font)
            btn.base_color = color
            btn.setStyleSheet(f"background-color: {color}; border-radius: 5px; font-weight: bold;")
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.clicked.connect(lambda checked, key=name: self.insert_key(key))
            key_id = f"{name}_{idx}"
            self.buttons[key_id] = btn
            self.key_ids.append(key_id)

    def highlight_key(self, key):
        for idx, (name, *_rest) in enumerate(keyboard_buttons):
            btn = self.buttons[self.key_ids[idx]]
            btn.setStyleSheet(f"background-color: {btn.base_color}; border-radius:5px; font-weight:bold;")

        key_lower = key.lower()
        for idx, (name, *_rest) in enumerate(keyboard_buttons):
            if name.lower() == key_lower:
                btn = self.buttons[self.key_ids[idx]]
                btn.setStyleSheet("background-color:red; border-radius:5px; font-weight:bold;")
                break

    def insert_key(self, key):
        cursor = self.input_field.textCursor()
        k_lower = key.lower()

        if k_lower == "backspace":
            cursor.deletePreviousChar()
        elif k_lower == "enter":
            cursor.insertText("\n")
        elif k_lower == "space":
            cursor.insertText(" ")
        else:
            cursor.insertText(key.lower())

        self.input_field.setTextCursor(cursor)
        parent = self.input_field.parent()

        if hasattr(parent, 'update_display'):
            parent.update_display()
            parent.update_caret_and_keyboard()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = self.width(), self.height()

        base_w, base_h = 870, 350
        for idx, (name, x, y, bw, bh, color) in enumerate(keyboard_buttons):
            btn = self.buttons[self.key_ids[idx]]

            new_x = int(x / base_w * w)
            new_y = int(y / base_h * h)
            new_w = max(int(bw / base_w * w), 30)
            new_h = max(int(bh / base_h * h), 30)

            btn.setGeometry(new_x, new_y, new_w, new_h)


class TypingTrainer(QWidget):
    def __init__(self, parent_app=None):
        super().__init__()
        self.parent_app = parent_app

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
        try:
            self.background_label.setPixmap(QPixmap("u.png"))
            self.background_label.setScaledContents(True)
            self.background_label.lower()
        except:
            pass

        self.init_ui()
        self.load_text_from_file()
        self.load_record()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.keyboard_widget = KeyboardWidget(self, self.user_input)
        QTimer.singleShot(100, self.update_caret_and_keyboard)

    def init_ui(self):
        font14 = QFont("Segoe Script", 14)
        font12 = QFont("Segoe Script", 12)

        self.original_display = QTextEdit(self)
        self.original_display.setReadOnly(True)
        self.original_display.setFont(font14)

        self.user_input = QTextEdit(self)
        self.user_input.setFont(font14)
        self.user_input.textChanged.connect(self.update_display)

        self.error_label = QLabel("Ошибок: 0", self)
        self.error_label.setFont(font14)

        self.timer_label = QLabel("Время: 00:00", self)
        self.timer_label.setFont(font14)

        self.best_time_label = QLabel("Рекорд: —", self)
        self.best_time_label.setFont(font14)
        self.best_time_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.exit_button = QPushButton("Выйти", self)
        self.exit_button.setFont(font12)
        self.exit_button.setStyleSheet("background-color:black; color:white; font-weight:bold; border-radius:5px;")
        self.exit_button.clicked.connect(self.go_to_main)

    # =============== Каретка + виртуальная клавиатура ===============
    def update_caret_and_keyboard(self):
        pos = len(self.user_input.toPlainText())
        if pos >= len(self.original_text):
            return

        next_char = self.original_text[pos]

        if next_char == " ":
            self.keyboard_widget.highlight_key("Space")
        elif next_char == "\n":
            self.keyboard_widget.highlight_key("Enter")
        else:
            self.keyboard_widget.highlight_key(next_char.lower())

        cursor = self.original_display.textCursor()
        cursor.setPosition(pos)

        fmt = QTextCharFormat()
        fmt.setForeground(QColor("green"))
        fmt.setFontUnderline(True)

        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)
        cursor.setCharFormat(fmt)

    # =================== Физическая клавиатура ====================
    def keyPressEvent(self, event: QKeyEvent):
        pos = len(self.user_input.toPlainText())
        if pos >= len(self.original_text):
            return

        expected = self.original_text[pos]
        key = event.key()
        text = event.text().lower()

        if key == Qt.Key.Key_Space:
            pressed = " "
            virt = "Space"

        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            pressed = "\n"
            virt = "Enter"

        elif key == Qt.Key.Key_Backspace:
            self.user_input.textCursor().deletePreviousChar()
            self.keyboard_widget.highlight_key("Backspace")
            return

        else:
            pressed = text
            virt = text

        if pressed == expected:
            self.user_input.insertPlainText(pressed)
            self.update_display()
        else:
            self.error_count += 1
            self.error_label.setText(f"Ошибок: {self.error_count}")

        self.keyboard_widget.highlight_key(virt)

    def keyReleaseEvent(self, event):
        self.update_caret_and_keyboard()

    # =================== Основная логика ==========================
    def load_text_from_file(self):
        try:
            with open("text.txt", "r", encoding="utf-8") as f:
                self.original_text = f.read()
        except:
            self.original_text = "Файл text.txt не найден."

        self.original_display.setPlainText(self.original_text)

    def update_display(self):
        user_text = self.user_input.toPlainText()

        if len(user_text) == 1 and not self.timer_running:
            self.start_timer()

        if len(user_text) >= len(self.original_text) and len(self.original_text) > 0:
            self.stop_timer()
            self.check_record()

            QMessageBox.information(
                self,
                "Тест завершён",
                f"Вы завершили тест!\nВремя: {self.time.toString('mm:ss')}"
            )

            self.go_to_main()
            return

        fmt_correct = QTextCharFormat(); fmt_correct.setForeground(QColor("green"))
        fmt_error   = QTextCharFormat(); fmt_error.setForeground(QColor("red"))
        fmt_future  = QTextCharFormat(); fmt_future.setForeground(QColor("gray"))

        cursor = self.original_display.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.setCharFormat(QTextCharFormat())

        self.error_count = 0

        for i, char in enumerate(user_text):
            if i >= len(self.original_text):
                self.error_count += 1
                continue

            cursor.setPosition(i)
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)

            if char == self.original_text[i]:
                cursor.setCharFormat(fmt_correct)
            else:
                cursor.setCharFormat(fmt_error)
                self.error_count += 1

        cursor.setPosition(len(user_text))
        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
        cursor.setCharFormat(fmt_future)

        self.error_label.setText(f"Ошибок: {self.error_count}")
        self.update_caret_and_keyboard()

    # ================= Таймер ==================
    def start_timer(self):
        self.time = QTime(0, 0, 0)
        self.timer.start(1000)
        self.timer_running = True

    def update_timer(self):
        self.time = self.time.addSecs(1)
        self.timer_label.setText(f"Время: {self.time.toString('mm:ss')}")

    def stop_timer(self):
        self.timer.stop()
        self.timer_running = False

    # ================= Рекорды =================
    def load_record(self):
        record = self.settings.value("best_time", "")
        if record:
            t = QTime.fromString(record, "mm:ss")
            if t.isValid():
                self.best_time = t

        self.best_time_label.setText(
            f"Рекорд: {self.best_time.toString('mm:ss') if self.best_time else '—'}"
        )

    def save_record(self):
        if self.best_time:
            self.settings.setValue("best_time", self.best_time.toString("mm:ss"))

    def check_record(self):
        if self.error_count > 0:
            return

        if not self.best_time or self.time < self.best_time:
            self.best_time = QTime(self.time.hour(), self.time.minute(), self.time.second())
            self.save_record()

    # ================= Выход ===================
    def go_to_main(self):
        self.close()
        if self.parent_app:
            self.parent_app.show()

    # ================= Разметка ==================
    def resizeEvent(self, event):
        super().resizeEvent(event)

        w, h = self.width(), self.height()

        self.background_label.setGeometry(0, 0, w, h)

        top_height = h // 3
        self.original_display.setGeometry(10, 10, w - 20, top_height)

        input_height = h // 12
        self.user_input.setGeometry(10, 20 + top_height, w - 20, input_height)

        label_y = 30 + top_height + input_height

        self.error_label.setGeometry(20, label_y, 200, 40)
        self.timer_label.setGeometry(230, label_y, 200, 40)
        self.best_time_label.setGeometry(430, label_y, 200, 40)
        self.exit_button.setGeometry(w - 130, label_y, 110, 35)

        keyboard_top = label_y + 60
        keyboard_height = h - keyboard_top - 10
        self.keyboard_widget.setGeometry(0, keyboard_top, w, keyboard_height)


# ============= Запуск ============
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingTrainer()
    window.show()
    sys.exit(app.exec())
