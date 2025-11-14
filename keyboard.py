import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

# Список кнопок
keyboard_buttons = [
    # --- 1 ряд (функциональные) ---
    ('Esc', 0, 0, 50, 50, 'white'),
    ('F1', 60, 0, 50, 50, 'white'),
    ('F2', 120, 0, 50, 50, 'white'),
    ('F3', 180, 0, 50, 50, 'white'),
    ('F4', 240, 0, 50, 50, 'white'),
    ('F5', 300, 0, 50, 50, 'white'),
    ('F6', 360, 0, 50, 50, 'white'),
    ('F7', 420, 0, 50, 50, 'white'),
    ('F8', 480, 0, 50, 50, 'white'),
    ('F9', 540, 0, 50, 50, 'white'),
    ('F10', 600, 0, 50, 50, 'white'),
    ('F11', 660, 0, 50, 50, 'white'),
    ('F12', 720, 0, 50, 50, 'white'),

    # --- 2 ряд (цифры) ---
    ('ё', 0, 60, 50, 50, 'gray'),
    ('1', 60, 60, 50, 50, 'pink'),
    ('2', 120, 60, 50, 50, 'pink'),
    ('3', 180, 60, 50, 50, 'yellow'),
    ('4', 240, 60, 50, 50, 'green'),
    ('5', 300, 60, 50, 50, 'blue'),
    ('6', 360, 60, 50, 50, 'blue'),
    ('7', 420, 60, 50, 50, 'purple'),
    ('8', 480, 60, 50, 50, 'green'),
    ('9', 540, 60, 50, 50, 'yellow'),
    ('0', 600, 60, 50, 50, 'pink'),
    ('-', 660, 60, 50, 50, 'pink'),
    ('=', 720, 60, 50, 50, 'gray'),
    ('Backspace', 780, 60, 90, 50, 'gray'),

    # --- 3 ряд (ЙЦУКЕН) ---
    ('Tab', 0, 120, 70, 50, 'gray'),
    ('Й', 80, 120, 50, 50, 'pink'),
    ('Ц', 140, 120, 50, 50, 'yellow'),
    ('У', 200, 120, 50, 50, 'green'),
    ('К', 260, 120, 50, 50, 'blue'),
    ('Е', 320, 120, 50, 50, 'blue'),
    ('Н', 380, 120, 50, 50, 'purple'),
    ('Г', 440, 120, 50, 50, 'purple'),
    ('Ш', 500, 120, 50, 50, 'green'),
    ('Щ', 560, 120, 50, 50, 'yellow'),
    ('З', 620, 120, 50, 50, 'pink'),
    ('Х', 680, 120, 50, 50, 'pink'),
    ('Ъ', 740, 120, 50, 50, 'pink'),
    ('\\', 800, 120, 70, 50, 'gray'),

    # --- 4 ряд (ФЫВАП) ---
    ('Caps lock', 0, 180, 90, 50, 'gray'),
    ('Ф', 100, 180, 50, 50, 'pink'),
    ('Ы', 160, 180, 50, 50, 'yellow'),
    ('В', 220, 180, 50, 50, 'green'),
    ('А', 280, 180, 50, 50, 'blue'),
    ('П', 340, 180, 50, 50, 'blue'),
    ('Р', 400, 180, 50, 50, 'purple'),
    ('О', 460, 180, 50, 50, 'purple'),
    ('Л', 520, 180, 50, 50, 'green'),
    ('Д', 580, 180, 50, 50, 'yellow'),
    ('Ж', 640, 180, 50, 50, 'pink'),
    ('Э', 700, 180, 50, 50, 'pink'),
    ('Enter', 760, 180, 110, 50, 'gray'),

    # --- 5 ряд (ЯЧСМИ) ---
    ('Shift_L', 0, 240, 110, 50, 'gray'),
    ('Я', 120, 240, 50, 50, 'pink'),
    ('Ч', 180, 240, 50, 50, 'yellow'),
    ('С', 240, 240, 50, 50, 'green'),
    ('М', 300, 240, 50, 50, 'blue'),
    ('И', 360, 240, 50, 50, 'blue'),
    ('Т', 420, 240, 50, 50, 'purple'),
    ('Ь', 480, 240, 50, 50, 'purple'),
    ('Б', 540, 240, 50, 50, 'green'),
    ('Ю', 600, 240, 50, 50, 'yellow'),
    ('.', 660, 240, 50, 50, 'pink'),
    ('Shift_R', 720, 240, 150, 50, 'gray'),

    # --- 6 ряд (Bottom row) ---
    ('Ctrl_L', 0, 300, 70, 50, 'gray'),
    ('Win_L', 80, 300, 70, 50, 'gray'),
    ('Alt_L', 160, 300, 70, 50, 'gray'),
    ('Space', 240, 300, 280, 50, 'orange'),
    ('Alt_R', 530, 300, 70, 50, 'gray'),
    ('Win_R', 610, 300, 70, 50, 'gray'),
    ('Menu', 690, 300, 70, 50, 'gray'),
    ('Ctrl_R', 770, 300, 70, 50, 'gray'),
]

class KeyboardArea(QWidget):
    """Отдельная область клавиатуры"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Клавиатура")
        self.setFixedSize(870, 350)  # увеличил высоту для 6 рядов
        self.buttons = {}
        self.init_ui()

    def init_ui(self):
        for key, x, y, w, h, color in keyboard_buttons:
            btn = QPushButton(key, self)
            btn.setGeometry(x, y, w, h)
            btn.setStyleSheet(f"background-color: {color}; font-weight: bold;")
            btn.clicked.connect(lambda checked, k=key: print(f"Нажата клавиша: {k}"))
            self.buttons[key] = btn

if __name__ == "__main__":
    app = QApplication(sys.argv)
    keyboard_window = KeyboardArea()
    keyboard_window.show()
    sys.exit(app.exec())
