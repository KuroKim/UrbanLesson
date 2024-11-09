# Задача "Средний баланс пользователя":
# Для решения этой задачи вам понадобится решение предыдущей.
# Для решения необходимо дополнить существующий код:
# Удалите из базы данных not_telegram.db запись с id = 6.
# Подсчитать общее количество записей.
# Посчитать сумму всех балансов.
# Вывести в консоль средний баланс всех пользователей.


import sqlite3

conn = sqlite3.connect('not_telegram.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
    )
''')

users = [
    ('User1', 'example1@gmail.com', 10, 1000),
    ('User2', 'example2@gmail.com', 20, 1000),
    ('User3', 'example3@gmail.com', 30, 1000),
    ('User4', 'example4@gmail.com', 40, 1000),
    ('User5', 'example5@gmail.com', 50, 1000),
    ('User6', 'example6@gmail.com', 60, 1000),
    ('User7', 'example7@gmail.com', 70, 1000),
    ('User8', 'example8@gmail.com', 80, 1000),
    ('User9', 'example9@gmail.com', 90, 1000),
    ('User10', 'example10@gmail.com', 100, 1000)
]

cursor.executemany('''
    INSERT INTO Users (username, email, age, balance)
    VALUES (?, ?, ?, ?)
''', users)
conn.commit()

cursor.execute('''
    UPDATE Users
    SET balance = 500
    WHERE id % 2 = 1
''')
conn.commit()

cursor.execute('''
    DELETE FROM Users
    WHERE id IN (SELECT id FROM Users WHERE (rowid - 1) % 3 = 0)
''')
conn.commit()

cursor.execute('''
    DELETE FROM Users
    WHERE id = 6
''')
conn.commit()

cursor.execute('''
    SELECT username, email, age, balance
    FROM Users
    WHERE age != 60
''')

users = cursor.fetchall()

for user in users:
    print(f'Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}')

total_users = cursor.execute('''
    SELECT COUNT(*)
    FROM Users
''').fetchone()[0]

total_balance = cursor.execute('''
    SELECT SUM(balance)
    FROM Users
''').fetchone()[0]


average_balance = total_balance / total_users

print(f'Общее количество пользователей: {total_users}')
print(f'Сумма всех балансов: {total_balance}')
print(f'Средний баланс всех пользователей: {average_balance}')


conn.close()
