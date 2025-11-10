from PyQt6.QtWidgets import QWidget, QPushButton,QMessageBox
from button import keyboard_buttons

class Mykeyboard(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = {}  # словарь для хранения кнопок
        self.create_button()

                # Создаем виджет строки ввода
        #self.line_edit = QLineEdit(self)
        #self.line_edit.setGeometry(20, 205, 850, 40)  

        # Можно подключить событие изменения текста
        #self.line_edit.textChanged.connect(self.on_text_changed)
        # Можно подключить событие на Enter
        #self.line_edit.returnPressed.connect(self.on_return_pressed)

        # Размещаем строку ввода в окне
        #layout = QVBoxLayout()
        #layout.addWidget(self.line_edit)
        

    #def on_text_changed(self, text):
        #print("Текст изменился:", text)

    #def on_return_pressed(self):

    def create_button(self):
        for name, x, y, x0, y0, color in keyboard_buttons:
            button = QPushButton(name, self)
            button.setGeometry(x, y, x0, y0)
            button.setStyleSheet(f"background-color: {color};")
            self.buttons[name.upper()] = button
   

    def on_button_click(self):
        QMessageBox.information(self, "Сообщение", "Ты нажал кнопку!")

if __name__=='__main__': 
    pass #все равно не воспринимает нжатие с калавиатуры