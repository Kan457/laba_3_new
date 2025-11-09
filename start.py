import sys
from PyQt6.QtWidgets import QApplication, QWidget , QPushButton, QMessageBox
from button import keyboard_buttons

class MyApp(QWidget):
    def __init__(self):
        super().__init__()# инициализация QWidget

        self.setWindowTitle("Окно приложения")
        self.resize(900, 600)
        self.create_button()

        # подключаем событие
        #self.button.clicked.connect(self.on_button_click)

    def create_button(self):
        for name,x,y,x0,y0 in keyboard_buttons:
            button = QPushButton(name,self)
            button.setGeometry(x,y,x0,y0)

    def on_button_click(self):
        QMessageBox.information(self, "Сообщение", "Ты нажал кнопку!")

application = QApplication(sys.argv)#создание приложени
#sys.argv — список аргументов, переданных при запуске программы
window = MyApp()
window.show()
sys.exit(application.exec())#слушает нажатия клавиш, клики мыши, обновления интерфейса,“держит” окно открытым


if __name__=='__main__':
    pass