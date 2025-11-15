import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QDialog
)
from PyQt6.QtGui import QFont, QPixmap, QPainter
from PyQt6.QtCore import Qt, QTimer, QEvent

from keyboard import keyboard_buttons  # файл с раскладкой клавиатуры


BASE_W = 900
BASE_H = 700
BASE_KB_H = 350
BASE_KB_W = 870


class KeyboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons = {}
        self.norm_map = {}
        self.alias = {
            " ": "space",
            "\n": "enter",
            "\t": "tab",
            "\b": "backspace",
            "enter": "enter"
        }
        self.make_buttons()

    def make_buttons(self):
        for name, x, y, w, h, color in keyboard_buttons:
            btn = QPushButton(name, self)
            btn.base_color = color
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setFont(QFont("Segoe Script", 12))
            btn.setStyleSheet(f"background-color:{color}; border-radius:5px;")
            btn.clicked.connect(lambda c, n=name: self.click(n))
            self.buttons[name] = btn
            self.norm_map[name.lower()] = name

    def click(self, name):
        parent = self.parent()
        if not parent:
            return

        if name.lower() == "backspace":
            txt = parent.input.text()
            parent.input.setText(txt[:-1])
            parent.check_live()
            return

        if name.lower() == "enter":
            parent.check_word()
            return

        if name.lower() == "space":
            parent.insert_char(" ")
            return

        ch = name[0].lower()
        parent.insert_char(ch)

    def highlight(self, key):
        for btn in self.buttons.values():
            btn.setStyleSheet(f"background-color:{btn.base_color}; border-radius:5px;")

        if key is None:
            return

        if key in self.alias:
            key = self.alias[key]

        key = str(key).lower()
        target = None
        if key in self.norm_map:
            target = self.norm_map[key]
        else:
            for k in self.buttons.keys():
                if k.lower() == key:
                    target = k

        if target:
            self.buttons[target].setStyleSheet("background-color:red; border-radius:5px;")

    def resize_keyboard(self, W, H):
        scale_x = W / BASE_KB_W
        scale_y = H / BASE_KB_H
        s = min(scale_x, scale_y)

        for name, x, y, w, h, color in keyboard_buttons:
            btn = self.buttons[name]
            btn.setGeometry(int(x * s), int(y * s), int(w * s), int(h * s))
            btn.setFont(QFont("Segoe Script", max(8, int(12 * s))))

        self.setFixedSize(int(BASE_KB_W * s), int(BASE_KB_H * s))


class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Помощь")
        self.setFixedSize(800, 600)

        lay = QVBoxLayout(self)
        lbl = QLabel()
        px = QPixmap("k.jpg")
        if not px.isNull():
            lbl.setPixmap(px.scaled(760, 520, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            lbl.setText("Нет изображения")

        lay.addWidget(lbl)

        btn = QPushButton("Закрыть")
        btn.setFont(QFont("Segoe Script", 14))
        btn.clicked.connect(self.close)
        lay.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)


class WordTrainer(QWidget):
    def __init__(self, parent_app=None):
        super().__init__()
        self.parent_app = parent_app
        self.setWindowTitle("Тренажёр слов")
        self.setMinimumSize(650, 500)

        # === ФОН ===
        self.bg = QPixmap("r.jpg")

        self.words = self.load_words()
        self.index = 0
        self.errors = 0

        # === СООБЩЕНИЕ ОБ ОШИБКЕ ===
        self.error_msg = QLabel("")
        self.error_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_msg.setFont(QFont("Segoe Script", 16, QFont.Weight.Bold))
        self.error_msg.setStyleSheet("color: red;")
        self.error_msg.hide()

        self.word_label = QLabel("")
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_label.setFont(QFont("Segoe Script", 24))

        self.input = QLineEdit()
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input.setFont(QFont("Segoe Script", 18))
        self.input.returnPressed.connect(self.check_word)
        self.input.textEdited.connect(self.check_live)

        self.error_label = QLabel("Ошибок: 0")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setFont(QFont("Segoe Script", 18))

        self.help_btn = QPushButton("Помощь")
        self.help_btn.clicked.connect(lambda: HelpDialog().exec())
        self.help_btn.setFont(QFont("Segoe Script", 18))
        self.help_btn.setStyleSheet("background-color: red; color: white; border-radius: 5px;")

        self.exit_btn = QPushButton("Выйти")
        self.exit_btn.clicked.connect(self.go_to_main)
        self.exit_btn.setFont(QFont("Segoe Script", 18))
        self.exit_btn.setStyleSheet("background-color: black; color: white; border-radius: 5px;")

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.exit_btn)
        top_bar.addStretch(1)
        top_bar.addWidget(self.help_btn)

        self.main_area = QVBoxLayout()
        self.main_area.addLayout(top_bar)
        self.main_area.addStretch(1)
        self.main_area.addWidget(self.error_msg)   # ← ВСТАВЛЕНО
        self.main_area.addWidget(self.word_label)
        self.main_area.addWidget(self.input, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_area.addWidget(self.error_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_area.addStretch(1)

        self.keyboard = KeyboardWidget(self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addLayout(self.main_area)
        layout.addWidget(self.keyboard, alignment=Qt.AlignmentFlag.AlignCenter)

        self.show_word()
        self.highlight_expected()
        self.input.installEventFilter(self)

        QTimer.singleShot(100, self.resize_all)

    def go_to_main(self):
        self.close()
        if self.parent_app:
            self.parent_app.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.bg.isNull():
            painter.drawPixmap(self.rect(), self.bg)

    def load_words(self):
        try:
            with open("word.txt", "r", encoding="utf-8") as f:
                return f.read().split()
        except:
            return ["пример", "слово", "текст"]

    def show_word(self):
        if self.index < len(self.words):
            self.word_label.setText(self.words[self.index])
            self.input.setText("")
            self.input.setStyleSheet("color:black;")
        else:
            self.word_label.setText("Готово!")
            self.input.setDisabled(True)

        self.highlight_expected()

    # === ФУНКЦИЯ СООБЩЕНИЯ ОБ ОШИБКЕ ===
    def show_error_message(self):
        self.error_msg.setText("Ошибка")
        self.error_msg.show()
        QTimer.singleShot(700, lambda: self.error_msg.hide())

    def insert_char(self, ch):
        self.input.insert(ch)
        self.check_live()

    def check_live(self):
        word = self.words[self.index]
        typed = self.input.text()

        if typed == word[:len(typed)]:
            self.input.setStyleSheet("color:green;")
        else:
            self.input.setStyleSheet("color:red;")
            self.show_error_message()

    def check_word(self):
        word = self.words[self.index]
        typed = self.input.text()

        if typed == word:
            self.index += 1
            self.show_word()
        else:
            self.errors += 1
            self.error_label.setText(f"Ошибок: {self.errors}")
            self.input.selectAll()
            self.show_error_message()

    def resize_all(self):
        W = self.width()
        H = self.height()
        kb_h = H * 0.50
        kb_w = W - 40
        self.keyboard.resize_keyboard(kb_w, kb_h)

        scale = W / BASE_W

        self.word_label.setFont(QFont("Segoe Script", max(18, int(40 * scale))))
        self.input.setFont(QFont("Segoe Script", max(14, int(22 * scale))))
        self.error_label.setFont(QFont("Segoe Script", max(12, int(18 * scale))))
        self.error_msg.setFont(QFont("Segoe Script", max(14, int(16 * scale)), QFont.Weight.Bold))

        self.help_btn.setFont(QFont("Segoe Script", max(10, int(14 * scale))))
        self.exit_btn.setFont(QFont("Segoe Script", max(10, int(14 * scale))))

        self.input.setFixedWidth(int(W * 0.5))
        self.input.setFixedHeight(int(45 * scale))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_all()

    def eventFilter(self, obj, event):
        if obj is self.input:
            if event.type() == QEvent.Type.KeyPress:
                key = event.key()
                ch = event.text()

                if key == Qt.Key.Key_Space:
                    self.keyboard.highlight("space")
                elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                    self.keyboard.highlight("enter")
                elif key == Qt.Key.Key_Backspace:
                    self.keyboard.highlight("backspace")
                elif ch:
                    self.keyboard.highlight(ch.lower())
                else:
                    self.keyboard.highlight(None)

            elif event.type() == QEvent.Type.KeyRelease:
                QTimer.singleShot(30, self.highlight_expected)

        return super().eventFilter(obj, event)

    def highlight_expected(self):
        if self.index < len(self.words):
            w = self.words[self.index]
            pos = len(self.input.text())

            if pos < len(w):
                self.keyboard.highlight(w[pos])
            else:
                self.keyboard.highlight("enter")
        else:
            self.keyboard.highlight(None)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WordTrainer()
    win.show()
    sys.exit(app.exec())
