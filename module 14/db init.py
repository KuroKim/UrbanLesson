from crud_functions import *


def populate_products():
    products = [
        ('Товар 1', 'Описание товара 1', 100),
        ('Товар 2', 'Описание товара 2', 200),
        ('Товар 3', 'Описание товара 3', 300),
        ('Товар 4', 'Описание товара 4', 400)
    ]
    cursor.executemany('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', products)
    conn.commit()
