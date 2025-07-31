import sqlite3

# Подключаемся к базе данных, которая лежит в той же папке
conn = sqlite3.connect("fi.db")
cursor = conn.cursor()

# Список таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Список таблиц:", tables)

# Пример: показать все записи из таблицы user
try:
    cursor.execute("SELECT * FROM user;")
    rows = cursor.fetchall()
    print("Содержимое таблицы user:")
    for row in rows:
        print(row)
except Exception as e:
    print("Ошибка при запросе:", e)

conn.close()
