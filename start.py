import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton,QMessageBox,QVBoxLayout, QLineEdit
from PyQt6.QtCore import Qt, QObject, QEvent
from button import keyboard_buttons

class KeyFilter(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            key = event.text().upper()
            if key in self.parent.buttons:
                self.parent.buttons[key].setStyleSheet("background-color: red;")
            return False  # чтобы событие продолжало распространяться
        elif event.type() == QEvent.Type.KeyRelease:
            key = event.text().upper()
            if key in self.parent.buttons:
                for n, x, y, x0, y0, color in keyboard_buttons:
                    if n.upper() == key:
                        self.parent.buttons[key].setStyleSheet(f"background-color: {color};")
                        break
            return False
        return False
    

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно приложения")
        self.resize(900, 650)
        self.buttons = {}  # словарь для хранения кнопок
        self.create_button()
        
        # чтобы получать события клавиатуры
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Устанавливаем фильтр событий для перехвата клавиш
        self.key_filter = KeyFilter(self)
        self.installEventFilter(self.key_filter)

        # Кнопка для чтения файла
        self.read_button = QPushButton("Читать файл", self)
        self.read_button.setGeometry(20, 160, 120, 40)
        #self.read_button.clicked.connect(self.read_file)

        # Чтобы окно могло получать фокус
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
                # Создаем виджет строки ввода
        self.line_edit = QLineEdit(self)
        self.line_edit.setGeometry(20, 205, 850, 40)  

        # Можно подключить событие изменения текста
        self.line_edit.textChanged.connect(self.on_text_changed)
        # Можно подключить событие на Enter
        self.line_edit.returnPressed.connect(self.on_return_pressed)

        # Размещаем строку ввода в окне
        layout = QVBoxLayout()
        layout.addWidget(self.line_edit)
        

    def on_text_changed(self, text):
        print("Текст изменился:", text)

    def on_return_pressed(self):
        print("Нажат Enter. Текущий текст:", self.line_edit.text())

    def create_button(self):
        for name, x, y, x0, y0, color in keyboard_buttons:
            button = QPushButton(name, self)
            button.setGeometry(x, y, x0, y0)
            button.setStyleSheet(f"background-color: {color};")
            self.buttons[name.upper()] = button
    '''
        def read_file(self):
    try:
        with open("example.txt", "r", encoding="utf-8") as f:
            self.file_lines = f.readlines()
        self.current_line_index = 0
        self.timer.start(500)  # каждые 500 мс выводим новую строку
    except FileNotFoundError:
        self.line_edit.setText("Файл example.txt не найден!")

    def update_text_from_file(self):
        if self.current_line_index < len(self.file_lines):
            line = self.file_lines[self.current_line_index].strip()
            self.line_edit.setText(line)
            self.current_line_index += 1
        else:
            self.timer.stop()  # останавливаем таймер после конца файла
    '''

    def on_button_click(self):
        QMessageBox.information(self, "Сообщение", "Ты нажал кнопку!")

if __name__=='__main__': 
    pass #все равно не воспринимает нжатие с калавиатуры