import sys  # Импорт системного модуля для работы с аргументами командной строки и выхода из приложения
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QLabel, QMessageBox  # Импорт нужных классов из PyQt6
from PyQt6.QtGui import QTextCharFormat, QColor, QTextCursor, QFont  # Импорт классов для форматирования текста
from PyQt6.QtCore import Qt, QTimer, QTime  # Импорт классов для таймера и времени


class TypingTrainer(QWidget):  # Класс тренажёра, наследуется от QWidget
    def __init__(self):
        super().__init__()  # Инициализация базового класса QWidget
        self.original_text = ""  # Исходный текст для набора
        self.error_count = 0  # Счётчик ошибок

        # ---------- Таймер и отсчёт времени ----------
        self.timer = QTimer()  # Создаём объект таймера
        self.time = QTime(0, 0, 0)  # Устанавливаем начальное время (00:00)
        self.timer.timeout.connect(self.update_timer)  # Подключаем сигнал таймера к методу обновления
        self.timer_running = False  # Флаг — идёт ли сейчас таймер

        # ---------- Рекорд времени ----------
        self.best_time = None  # Переменная для хранения лучшего результата (тип QTime)
        self.record_file = "record.txt"  # Имя файла для сохранения рекорда
        self.load_record()  # Загружаем рекорд из файла (если есть)

        # ---------- Интерфейс ----------
        self.init_ui()  # Создаём элементы интерфейса
        self.load_text_from_file()  # Загружаем текст для тренировки

    def init_ui(self):
        layout = QVBoxLayout()  # Основной вертикальный layout для расположения элементов

        base_font = QFont("Arial", 14)  # Базовый шрифт для всех текстовых элементов

        self.original_display = QTextEdit()  # Поле с оригинальным текстом
        self.original_display.setReadOnly(True)  # Делаем поле только для чтения
        self.original_display.setFixedHeight(100)  # Устанавливаем высоту
        self.original_display.setFont(base_font)  # Устанавливаем шрифт

        self.user_input = QTextEdit()  # Поле для пользовательского ввода
        self.user_input.setFixedHeight(100)  # Устанавливаем высоту
        self.user_input.setFont(base_font)  # Устанавливаем шрифт
        self.user_input.textChanged.connect(self.update_display)  # Обновляем подсветку при изменении текста

        self.error_label = QLabel("Ошибок: 0")  # Метка для отображения количества ошибок
        self.error_label.setFont(base_font)  # Шрифт метки

        self.timer_label = QLabel("Время: 00:00")  # Метка таймера
        self.timer_label.setFont(base_font)  # Шрифт метки

        self.record_label = QLabel(self.get_record_text())  # Метка для вывода рекорда
        self.record_label.setFont(base_font)  # Шрифт метки

        # Добавляем все элементы на layout
        layout.addWidget(QLabel("Оригинальный текст:", font=base_font))
        layout.addWidget(self.original_display)
        layout.addWidget(QLabel("Ваш ввод:", font=base_font))
        layout.addWidget(self.user_input)
        layout.addWidget(self.error_label)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.record_label)

        self.setLayout(layout)  # Применяем layout к окну
        self.setWindowTitle("Тренажёр набора текста (PyQt6)")  # Заголовок окна

    # ---------- Работа с рекордом ----------
    def load_record(self):
        """Загружает рекорд из файла record.txt."""
        try:
            with open(self.record_file, "r", encoding="utf-8") as f:  # Пытаемся открыть файл
                record_str = f.read().strip()  # Считываем строку
                if record_str:  # Если файл не пустой
                    self.best_time = QTime.fromString(record_str, "mm:ss")  # Преобразуем строку в QTime
        except FileNotFoundError:
            self.best_time = None  # Если файл не найден — рекорда нет

    def save_record(self):
        """Сохраняет рекорд в файл record.txt."""
        if self.best_time:  # Проверяем, есть ли рекорд
            with open(self.record_file, "w", encoding="utf-8") as f:  # Открываем файл для записи
                f.write(self.best_time.toString("mm:ss"))  # Сохраняем рекорд как строку

    def get_record_text(self):
        """Возвращает строку для отображения рекорда."""
        if self.best_time:
            return f"Рекорд: {self.best_time.toString('mm:ss')}"  # Если рекорд есть — возвращаем время
        return "Рекорд: —"  # Если нет рекорда

    # ---------- Таймер ----------
    def start_timer(self):
        """Запускает таймер при начале ввода."""
        if not self.timer_running:  # Проверяем, не запущен ли уже таймер
            self.time = QTime(0, 0, 0)  # Обнуляем время
            self.timer.start(1000)  # Запускаем таймер с шагом 1 секунда
            self.timer_running = True  # Меняем флаг состояния

    def stop_timer(self):
        """Останавливает таймер и проверяет рекорд."""
        if self.timer_running:  # Проверяем, запущен ли таймер
            self.timer.stop()  # Останавливаем
            self.timer_running = False  # Меняем флаг
            self.check_record()  # Проверяем, побит ли рекорд

    def update_timer(self):
        """Обновляет таймер каждую секунду."""
        self.time = self.time.addSecs(1)  # Добавляем 1 секунду к времени
        self.timer_label.setText(f"Время: {self.time.toString('mm:ss')}")  # Обновляем надпись на экране

    # ---------- Работа с текстом ----------
    def load_text_from_file(self):
        """Загружает текст из файла text.txt."""
        try:
            with open("text.txt", "r", encoding="utf-8") as f:  # Открываем файл с текстом
                self.original_text = " ".join(f.read().split())  # Убираем лишние пробелы и переносы
            self.original_display.setPlainText(self.original_text)  # Показываем текст на экране
        except FileNotFoundError:
            self.original_display.setPlainText("Файл text.txt не найден.")  # Если файла нет — сообщение
            self.original_text = ""  # Пустой текст

    def update_display(self):
        """Подсвечивает правильные и неправильные символы и считает ошибки."""
        user_text = self.user_input.toPlainText()  # Получаем текст, введённый пользователем

        # Запускаем таймер при вводе первого символа
        if len(user_text) == 1 and not self.timer_running:
            self.start_timer()

        # Останавливаем таймер, если весь текст введён
        if len(user_text) >= len(self.original_text) and self.timer_running:
            self.stop_timer()

        self.error_count = 0  # Обнуляем счётчик ошибок

        fmt_correct = QTextCharFormat()  # Формат для правильных символов
        fmt_correct.setForeground(QColor("green"))  # Цвет — зелёный

        fmt_error = QTextCharFormat()  # Формат для ошибок
        fmt_error.setForeground(QColor("red"))  # Цвет — красный

        text_cursor = self.original_display.textCursor()  # Получаем курсор редактирования текста
        text_cursor.select(QTextCursor.SelectionType.Document)  # Выбираем весь текст
        text_cursor.setCharFormat(QTextCharFormat())  # Сбрасываем формат (убираем старую подсветку)

        # Подсветка символов
        for i, char in enumerate(user_text):  # Перебираем символы, которые ввёл пользователь
            text_cursor.setPosition(i)  # Ставим курсор на позицию символа
            text_cursor.movePosition(QTextCursor.MoveOperation.Right,
                                     QTextCursor.MoveMode.KeepAnchor, 1)  # Выделяем символ
            if i < len(self.original_text) and char == self.original_text[i]:  # Проверяем совпадение с оригиналом
                text_cursor.setCharFormat(fmt_correct)  # Если совпадает — зелёный
            else:
                text_cursor.setCharFormat(fmt_error)  # Если ошибка — красный
                self.error_count += 1  # Увеличиваем счётчик ошибок

        # Подсвечиваем оставшийся текст серым
        fmt_future = QTextCharFormat()
        fmt_future.setForeground(QColor("gray"))  # Цвет для ещё не введённого текста
        if len(user_text) < len(self.original_text):  # Если пользователь не дописал до конца
            text_cursor.setPosition(len(user_text))  # Ставим курсор на текущую позицию
            text_cursor.movePosition(QTextCursor.MoveOperation.End,
                                     QTextCursor.MoveMode.KeepAnchor)  # Выделяем оставшийся текст
            text_cursor.setCharFormat(fmt_future)  # Применяем серый цвет

        # Обновляем счётчик ошибок на экране
        self.error_label.setText(f"Ошибок: {self.error_count}")

        # Прокручиваем оригинальный текст, чтобы текущая позиция всегда была видна
        self.scroll_to_position(len(user_text))

    def scroll_to_position(self, pos):
        """Прокручивает текст, чтобы текущая позиция была видна."""
        cursor = self.original_display.textCursor()  # Получаем курсор текста
        cursor.setPosition(pos)  # Устанавливаем позицию курсора
        self.original_display.setTextCursor(cursor)  # Применяем курсор
        self.original_display.ensureCursorVisible()  # Прокручиваем, чтобы курсор был виден

    # ---------- Проверка рекорда ----------
    def check_record(self):
        """Сравнивает текущее время с рекордом и обновляет его, если побит."""
        if self.error_count > 0:  # Если есть ошибки
            QMessageBox.information(self, "Результат",
                                    f"Вы закончили с ошибками ({self.error_count}). Время: {self.time.toString('mm:ss')}")
            return  # Не обновляем рекорд при ошибках

        # Если рекорда нет или текущее время лучше
        if not self.best_time or self.time < self.best_time:
            self.best_time = self.time  # Сохраняем новый рекорд
            self.save_record()  # Пишем рекорд в файл
            self.record_label.setText(self.get_record_text())  # Обновляем метку рекорда
            QMessageBox.information(self, "Новый рекорд!",
                                    f"Поздравляем! Новый рекорд: {self.best_time.toString('mm:ss')}")
        else:
            # Просто показываем текущее время, если рекорд не побит
            QMessageBox.information(self, "Результат",
                                    f"Ваше время: {self.time.toString('mm:ss')}\nРекорд: {self.best_time.toString('mm:ss')}")


# ---------- Точка входа ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаём приложение
    window = TypingTrainer()  # Создаём окно тренажёра
    window.resize(800, 400)  # Устанавливаем размер окна
    window.show()  # Показываем окно
    sys.exit(app.exec())  # Запускаем главный цикл приложения
