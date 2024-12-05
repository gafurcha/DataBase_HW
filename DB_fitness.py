import sqlite3

# Подключение к базе данных (создаст файл, если его нет)
connection = sqlite3.connect('fitness_club.db')

# Создание объекта курсора
cursor = connection.cursor()

# Создание таблиц
cursor.execute("""
CREATE TABLE IF NOT EXISTS Клиенты (
    Код_клиента INTEGER PRIMARY KEY AUTOINCREMENT,
    Фамилия TEXT NOT NULL,
    Имя TEXT NOT NULL,
    Отчество TEXT,
    Адрес TEXT,
    Телефон TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Абонементы (
    Код_абонемента INTEGER PRIMARY KEY AUTOINCREMENT,
    Название TEXT NOT NULL,
    Цена REAL NOT NULL,
    Количество_посещений_в_день INTEGER NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Продажа_абонементов (
    Номер_карты INTEGER PRIMARY KEY AUTOINCREMENT,
    Код_клиента INTEGER NOT NULL,
    Абонемент INTEGER NOT NULL,
    Дата_начала DATE NOT NULL,
    Дата_окончания DATE NOT NULL,
    FOREIGN KEY (Код_клиента) REFERENCES Клиенты(Код_клиента),
    FOREIGN KEY (Абонемент) REFERENCES Абонементы(Код_абонемента)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Учет_посещений (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Номер_карты INTEGER NOT NULL,
    Услуга INTEGER NOT NULL,
    FOREIGN KEY (Номер_карты) REFERENCES Продажа_абонементов(Номер_карты)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Услуги (
    Код_услуги INTEGER PRIMARY KEY,
    Наименование_услуги TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Помещения (
    Код_помещения INTEGER PRIMARY KEY,
    Название TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Список_сотрудников (
    Номер_сотрудника INTEGER PRIMARY KEY AUTOINCREMENT,
    Фамилия TEXT NOT NULL,
    Имя TEXT NOT NULL,
    Отчество TEXT,
    Адрес TEXT,
    Дата_рождения DATE,
    Оклад REAL NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Расписание (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Дата DATE NOT NULL,
    Время_начала TIME NOT NULL,
    Время_окончания TIME NOT NULL,
    Помещение INTEGER NOT NULL,
    Сотрудник INTEGER NOT NULL,
    Примечание TEXT,
    FOREIGN KEY (Помещение) REFERENCES Помещения(Код_помещения),
    FOREIGN KEY (Сотрудник) REFERENCES Список_сотрудников(Номер_сотрудника)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Специализация_сотрудников (
    Номер_сотрудника INTEGER NOT NULL,
    Услуга INTEGER NOT NULL,
    PRIMARY KEY (Номер_сотрудника, Услуга),
    FOREIGN KEY (Номер_сотрудника) REFERENCES Список_сотрудников(Номер_сотрудника),
    FOREIGN KEY (Услуга) REFERENCES Услуги(Код_услуги)
);
""")

# Очистка таблиц перед добавлением данных
tables = ["Клиенты", "Абонементы", "Продажа_абонементов", "Учет_посещений", "Услуги", "Помещения", "Список_сотрудников", "Расписание", "Специализация_сотрудников"]
for table in tables:
    cursor.execute(f"DELETE FROM {table};")

# Добавление тестовых данных в таблицы

# Клиенты
cursor.executemany("""
INSERT INTO Клиенты (Фамилия, Имя, Отчество, Адрес, Телефон) 
VALUES (?, ?, ?, ?, ?);
""", [
    ("Иванов", "Иван", "Иванович", "Москва, ул. Ленина, 1", "+7-999-123-45-67"),
    ("Петров", "Петр", "Петрович", "СПб, ул. Гагарина, 5", "+7-911-222-33-44"),
    ("Сидоров", "Сергей", "Александрович", "Москва, ул. Мира, 10", "+7-495-000-00-01"),
    ("Кузнецова", "Мария", "Ивановна", "Казань, ул. Баумана, 18", "+7-843-555-66-77"),
    ("Белова", "Анна", "Викторовна", "СПб, пр. Невский, 24", "+7-812-333-44-55"),
    ("Максимов", "Николай", "Степанович", "Москва, пр. Вернадского, 78", "+7-925-100-20-30"),
    ("Романов", "Алексей", "Олегович", "Самара, ул. Молодежная, 56", "+7-846-777-88-99")
])

# Абонементы
cursor.executemany("""
INSERT INTO Абонементы (Название, Цена, Количество_посещений_в_день) 
VALUES (?, ?, ?);
""", [
    ("Полный доступ", 3000.00, 1),
    ("Йога", 1500.00, 2),
    ("Кардио-зал", 1800.00, 2),
    ("Персональная тренировка", 5000.00, 1),
    ("Детский клуб", 2000.00, 3),
    ("Реабилитация", 4500.00, 1),

    ("Сауна и бассейн", 2500.00, 2)
])

# Услуги
cursor.executemany("""
INSERT INTO Услуги (Код_услуги, Наименование_услуги) 
VALUES (?, ?);
""", [
    (1, "Тренажерный зал"),
    (2, "Йога"),
    (3, "Массаж"),
    (4, "Сауна"),
    (5, "Персональная тренировка"),
    (6, "Плавательный бассейн"),
    (7, "Реабилитация после травм")
])

# Помещения
cursor.executemany("""
INSERT INTO Помещения (Код_помещения, Название) 
VALUES (?, ?);
""", [
    (1, "Основной зал"),
    (2, "Зал йоги"),
    (3, "Кардио-зал"),
    (4, "Раздевалка"),
    (5, "Сауна"),
    (6, "Бассейн"),
    (7, "Массажная комната")
])

# Список сотрудников
cursor.executemany("""
INSERT INTO Список_сотрудников (Фамилия, Имя, Отчество, Адрес, Дата_рождения, Оклад) 
VALUES (?, ?, ?, ?, ?, ?);
""", [
    ("Петров", "Петр", "Иванович", "Москва, ул. Гагарина, 12", "1980-05-15", 50000.00),
    ("Сидорова", "Ольга", "Николаевна", "СПб, ул. Ленина, 8", "1990-04-20", 55000.00),
    ("Васильев", "Александр", "Юрьевич", "Москва, ул. Мира, 45", "1985-03-10", 60000.00),
    ("Кузнецов", "Максим", "Андреевич", "Казань, ул. Баумана, 18", "1995-08-18", 48000.00),
    ("Белоусова", "Татьяна", "Викторовна", "СПб, ул. Пролетарская, 7", "1987-06-15", 52000.00),
    ("Григорьев", "Иван", "Степанович", "Москва, ул. Ломоносова, 33", "1979-12-12", 62000.00),
    ("Федорова", "Екатерина", "Сергеевна", "СПб, ул. Балканская, 3", "1992-11-11", 47000.00)
])

# Сохранение изменений
connection.commit()

# Проверка содержимого базы данных
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Список таблиц в базе данных:", cursor.fetchall())

# Проверка содержимого таблиц
cursor.execute("SELECT * FROM Клиенты;")
print("\nДанные из таблицы 'Клиенты':", cursor.fetchall())

cursor.execute("SELECT * FROM Абонементы;")
print("\nДанные из таблицы 'Абонементы':", cursor.fetchall())

cursor.execute("SELECT * FROM Услуги;")
print("\nДанные из таблицы 'Услуги':", cursor.fetchall())

# Закрытие соединения
connection.close()

