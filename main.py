import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from start_file import MyApp
from PyQt6.QtGui import QPixmap



application = QApplication(sys.argv)
window = MyApp()
window.resize(900, 650)
window.show()
sys.exit(application.exec())