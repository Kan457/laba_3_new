
from PyQt6.QtWidgets import QWidget, QPushButton,QMessageBox
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно приложения клавиатурный тренажер")

if __name__=='__main__': 
    pass #все равно не воспринимает нжатие с калавиатуры