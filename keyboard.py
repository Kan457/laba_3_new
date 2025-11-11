from PyQt6.QtWidgets import QWidget, QPushButton,QMessageBox
from button import keyboard_buttons

class Mykeyboard(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = {}  # словарь для хранения кнопок
        self.create_button()

    def create_button(self):
        for name, x, y, x0, y0, color in keyboard_buttons:
            button = QPushButton(name, self)
            button.setGeometry(x, y, x0, y0)
            button.setStyleSheet(f"background-color: {color};")
            self.buttons[name.upper()] = button
   

    def on_button_click(self):
        QMessageBox.information(self, "Сообщение", "Ты нажал кнопку!")

if __name__=='__main__': 
    pass 