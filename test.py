# Импорт системного модуля для работы с аргументами и завершением программы
import sys

# Импорт нужных классов из PyQt6 для создания интерфейса
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QLabel, QPushButton, QVBoxLayout , QHBoxLayout , QGridLayout , QMessageBox
from PyQt6.QtGui import QTextCharFormat, QColor, QTextCursor, QFont , QPixmap  # Работа с цветом, текстом, шрифтами
from PyQt6.QtCore import Qt, QTimer, QTime                             # Работа с временем и сигналами
from button import keyboard_buttons  # Импортируем список кнопок (координаты и цвета клавиш)

# Класс основного окна приложения
class TypingTrainer(QWidget):
    def __init__(self):
        super().__init__()  # Инициализация родительского класса QWidget

        self.setWindowTitle("Тренажёр набора текста")  # Заголовок окна
        self.setFixedSize(900, 650)                    # Фиксированный размер окна

        # === Основные переменные ===
        self.original_text = ""        # Текст для набора
        self.error_count = 0           # Количество ошибок пользователя
        self.timer_running = False     # Флаг, запущен ли таймер
        self.time = QTime(0,0,0)       # Объект времени (начальное значение 00:00)
        self.best_time = None          # Лучшее время (рекорд)
        self.record_file = "record.txt" # Файл для сохранения рекорда

        self.buttons = {}              # Словарь для хранения кнопок клавиатуры

        # === Вызовы методов инициализации ===
        self.init_ui()                 # Создание интерфейса
        self.create_keyboard()         # Создание виртуальной клавиатуры
        self.load_text_from_file()     # Загрузка текста из файла
        self.load_record()             # Загрузка рекорда из файла

        # === Настройка таймера ===
        self.timer = QTimer()                        # Создаём таймер
        self.timer.timeout.connect(self.update_timer) # При каждом срабатывании вызывается update_timer

    # === Создание элементов интерфейса ===
    def init_ui(self):
        self.layout = QVBoxLayout()      # Вертикальный макет (элементы располагаются сверху вниз)
        base_font = QFont("Segoe Script", 14)   # Базовый шрифт для всех элементов
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("i.jpg"))  # путь к картинке
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, 900, 650)
        self.background_label.lower()  # Отправляем на задний план

        # Поле для отображения оригинального текста
        self.original_display = QTextEdit(self)
        self.original_display.setReadOnly(True)
        self.original_display.setFont(base_font)
        self.original_display.setGeometry(10, 10, 880, 180)  # x, y, width, height

        # Поле для ввода текста пользователем
        self.user_input = QTextEdit(self)
        self.user_input.setFont(base_font)
        self.user_input.setGeometry(10, 210, 880, 50)  # x, y, width, height
        self.user_input.textChanged.connect(self.update_display)

        # Метка ошибок
        self.error_label = QLabel("Ошибок: 0", self)
        self.error_label.setFont(base_font)
        self.error_label.setGeometry(10, 260, 200, 30)  # x, y, width, height

        # Метка таймера
        self.timer_label = QLabel("Время: 00:00", self)
        self.timer_label.setFont(base_font)
        self.timer_label.setGeometry(350, 260, 200, 30)  # x, y, width, height

    # === Создание экранной клавиатуры ===
    def create_keyboard(self):
        """Создание кнопок клавиатуры из списка keyboard_buttons"""
        for name, x, y, x0, y0, color in keyboard_buttons:
            button = QPushButton(name, self)
            button.setGeometry(x, y, x0, y0)
            button.setStyleSheet(f"background-color: {color};")
            self.buttons[name.upper()] = button
   
        '''
        keyboard_layout = QGridLayout()  # создаём сетку для клавиш
        keyboard_layout.setSpacing(5)    # расстояние между клавишами

        row = 0
        col = 0
        max_cols = 14  # можно подстроить под ширину клавиатуры

        for key, x, y, w, h, color in keyboard_buttons:
            btn = QPushButton(str(key))  # создаём кнопку
            btn.setFixedSize(w, h)       # задаём размеры
            btn.setStyleSheet(f"background-color: {color}; font-size: 14px;")
            btn.clicked.connect(lambda checked, k=str(key): self.insert_key(k))
            keyboard_layout.addWidget(btn, row, col)  # добавляем кнопку в сетку
            self.buttons[str(key).upper()] = btn

            col += 1
            if col >= max_cols:  # перенос на новую строку
                col = 0
                row += 1

        self.layout.addLayout(keyboard_layout)  # добавляем клавиатуру в основной layout
        '''

    # === Вставка символа в поле ввода ===
    def insert_key(self, key):
        cursor = self.user_input.textCursor()   # Получаем курсор в поле ввода
        cursor.insertText(key)                  # Вставляем символ
        self.user_input.setTextCursor(cursor)   # Обновляем положение курсора

    # === Запуск таймера ===
    def start_timer(self):
        if not self.timer_running:      # Если таймер не запущен
            self.time = QTime(0,0,0)    # Обнуляем время
            self.timer.start(1000)      # Запускаем таймер (раз в 1 секунду)
            self.timer_running = True   # Устанавливаем флаг

    # === Обновление времени ===
    def update_timer(self):
        self.time = self.time.addSecs(1) # Добавляем 1 секунду
        self.timer_label.setText(f"Время: {self.time.toString('mm:ss')}") # Обновляем текст метки

    # === Остановка таймера ===
    def stop_timer(self):
        if self.timer_running:          # Если таймер запущен
            self.timer.stop()           # Останавливаем его
            self.timer_running = False  # Меняем флаг
            self.check_record()         # Проверяем, побит ли рекорд

    # === Загрузка текста из файла ===
    def load_text_from_file(self):
        try:
            with open("text.txt", "r", encoding="utf-8") as f:   # Открываем файл с текстом
                self.original_text = " ".join(f.read().split())  # Читаем текст и удаляем лишние пробелы
            self.original_display.setPlainText(self.original_text) # Отображаем текст в поле
        except FileNotFoundError:                               # Если файл не найден
            self.original_display.setPlainText("Файл text.txt не найден.")
            self.original_text = ""

    # === Проверка правильности ввода ===
    def update_display(self):
        user_text = self.user_input.toPlainText()   # Получаем текст, введённый пользователем

        # Запуск таймера при первом вводе
        if len(user_text) == 1 and not self.timer_running:
            self.start_timer()

        if len(user_text) >= len(self.original_text):
            self.stop_timer()
            # Сохраняем текущий результат
            self.save_result()
            previous = self.load_previous_results()

            # Показать сообщение с результатами
            msg = QMessageBox(self)
            msg.setWindowTitle("Тест завершён")
            msg.setText(f"Вы завершили тест!\nВремя: {self.time.toString('mm:ss')}\n\nПредыдущие результаты:\n{previous}")
            msg.exec()
            
            # Можно закрывать окно, если нужно
            self.close()
        # Обнуляем ошибки
        self.error_count = 0

        # Настраиваем форматы цвета
        fmt_correct = QTextCharFormat()
        fmt_correct.setForeground(QColor("green"))  # Зелёный для правильных символов
        fmt_error = QTextCharFormat()
        fmt_error.setForeground(QColor("red"))      # Красный для ошибок
        fmt_future = QTextCharFormat()
        fmt_future.setForeground(QColor("gray"))    # Серый для ещё не введённого текста

        # Получаем курсор для редактирования форматирования текста
        cursor = self.original_display.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)  # Выделяем весь текст
        cursor.setCharFormat(QTextCharFormat())            # Сбрасываем предыдущее форматирование

        # Проходим по каждому введённому символу
        for i, char in enumerate(user_text):
            cursor.setPosition(i)   # Переходим к символу
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1) # Захватываем его
            if i < len(self.original_text) and char == self.original_text[i]: # Если символ совпадает
                cursor.setCharFormat(fmt_correct)  # Зелёный
            else:
                cursor.setCharFormat(fmt_error)    # Красный
                self.error_count += 1              # Увеличиваем счётчик ошибок

        # Подсветка ещё не введённого текста
        if len(user_text) < len(self.original_text):
            cursor.setPosition(len(user_text))
            cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
            cursor.setCharFormat(fmt_future)

        # Обновляем метку ошибок
        self.error_label.setText(f"Ошибок: {self.error_count}")
        self.scroll_to_position(len(user_text))  # Прокручиваем текст, если он длинный

    # === Прокрутка текста ===
    def scroll_to_position(self, pos):
        cursor = self.original_display.textCursor()
        cursor.setPosition(pos)
        self.original_display.setTextCursor(cursor)
        self.original_display.ensureCursorVisible()

    # === Загрузка рекорда ===
    def load_record(self):
        try:
            with open(self.record_file, "r", encoding="utf-8") as f:
                record_str = f.read().strip()  # Читаем строку
                if record_str:
                    self.best_time = QTime.fromString(record_str, "mm:ss")  # Преобразуем строку во время
        except FileNotFoundError:
            self.best_time = None  # Если файла нет — рекорд отсутствует

    # === Сохранение рекорда ===
    def save_record(self):
        if self.best_time:
            with open(self.record_file, "w", encoding="utf-8") as f:
                f.write(self.best_time.toString("mm:ss"))  # Записываем рекорд в файл

    # === Проверка нового рекорда ===
    def check_record(self):
        if self.error_count > 0:  # Если есть ошибки — не засчитываем
            return
        if not self.best_time or self.time < self.best_time:  # Если нет рекорда или текущее время лучше
            self.best_time = self.time  # Сохраняем новый рекорд
            self.save_record()          # Записываем в файл


# ---------- Запуск приложения ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаём приложение Qt
    window = TypingTrainer()      # Создаём объект главного окна
    window.show()                 # Показываем окно
    sys.exit(app.exec())          # Запускаем цикл событий и выходим при закрытии
