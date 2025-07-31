import sqlite3

def main():
    # Подключаемся к базе (укажи правильный путь к файлу fi.db)
    conn = sqlite3.connect("C:/Users/User/PycharmProjects/21.07/fi.db")
    cursor = conn.cursor()

    # Пример запроса — получить список таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Таблицы в базе:", tables)

    # Пример: выбрать все записи из таблицы user
    try:
        cursor.execute("SELECT * FROM user;")
        rows = cursor.fetchall()
        print("Данные из таблицы user:")
        for row in rows:
            print(row)
    except Exception as e:
        print("Ошибка при запросе:", e)

    # Закрываем соединение
    conn.close()

if __name__ == "__main__":
    main()
