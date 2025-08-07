import sqlite3

def main():

    conn = sqlite3.connect("/financial_tracker/fi.db")
    cursor = conn.cursor()


    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Таблицы в базе:", tables)


    try:
        cursor.execute("SELECT * FROM user;")
        rows = cursor.fetchall()
        print("Данные из таблицы user:")
        for row in rows:
            print(row)
    except Exception as e:
        print("Ошибка при запросе:", e)


    conn.close()

if __name__ == "__main__":
    main()
