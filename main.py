import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from start import MyApp

application = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(application.exec())
