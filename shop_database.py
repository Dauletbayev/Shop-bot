import sqlite3

# Подключение к БД
connection = sqlite3.connect("shop.db", check_same_thread=False)
# Python + SQL
sql = connection.cursor()


## Создание таблиц ##
# Таблица пользователей
sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(id INTEGER, name TEXT, number TEXT, location TEXT);')
# Таблица продуктов
sql.execute('CREATE TABLE IF NOT EXISTS products '
            '(id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT,'
            'pr_des TEXT, pr_count INTEGER, pr_photo TEXT, pr_price REAL);')
# Таблица корзины
sql.execute('CREATE TABLE IF NOT EXISTS cart '
            '(user_id INTEGER, user_product TEXT, pr_amount INTEGER, total REAL);')


## Методы для пользователя ##
# Регистрация
def register(id, name, number, location):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (id, name, number, location))
    # Фиксируем изменения
    connection.commit()


# Проверка на наличие пользователя в БД
def checker(id):
    check = sql.execute('SELECT id FROM users WHERE id=?;', (id,))

    if check.fetchone():
        return True
    else:
        return False


## Методы для продуктов ##
# Вывод инфы о конкретном товаре
def get_pr(id):
    result = sql.execute('SELECT pr_name, pr_des, pr_count, pr_photo, pr_price FROM products WHERE id=?;',
                         (id,))
    return result.fetchone()

# Метод для отображения продуктов в кнопках
def get_pr_but():
    return sql.execute('SELECT id, pr_name, pr_count FROM products;').fetchall()


# Метод для добавления продукта в БД
def add_pr(name, des, count, photo, price):
    sql.execute('INSERT INTO products(pr_name, pr_des, pr_count, pr_photo, pr_price) '
                'VALUES(?, ?, ?, ?, ?);', (name, des, count, photo, price))
    # Фиксируем изменения
    connection.commit()

# Метод для удаления
def del_pr(id):
    sql.execute('DELETE FROM products WHERE id=?;', (id,))
    # Фиксируем изменения
    connection.commit()

# Метод для изменения количества
def change_pr_count(id, new_count):
    # Текущее кол-во товара
    now_count = sql.execute('SELECT pr_count FROM products WHERE id=?;', (id,)).fetchone()
    # Приход товара
    plus_count = now_count[0] + new_count
    sql.execute('UPDATE products SET pr_count=? WHERE id=?;', (plus_count, id))
    # Фиксируем изменения
    connection.commit()


# Метод для получения id товаров
def get_pr_name_id():
    prods = sql.execute('SELECT id, pr_count FROM products;').fetchall()
    all_prods = [i[0] for i in prods if i[1] > 0]
    return all_prods


# Метод для проверки наличия продуктов в базе
def check_pr():
    if sql.execute('SELECT * FROM products;').fetchall():
        return True
    else:
        return False


# Метод для проверки наличия продукта по id
def check_pr_id(id):
    if sql.execute('SELECT id FROM products WHERE id=?;', (id,)).fetchone():
        return True
    else:
        return False


## Методы корзины ##
# Добавление в корзину
def add_pr_to_cart(user_id, user_product, pr_amount, total):
    sql.execute('INSERT INTO cart VALUES(?, ?, ?, ?);', (user_id, user_product, pr_amount, total))
    # Фиксируем изменения
    connection.commit()


# Очистка корзины
def clear_cart(user_id):
    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id,))
    # Фиксируем изменения
    connection.commit()


# Оформление заказа
def make_order(user_id):
    pr_name = sql.execute('SELECT user_product FROM cart WHERE user_id=?;', (user_id,)).fetchone()
    amount = sql.execute('SELECT pr_amount FROM cart WHERE user_id=?;', (user_id,)).fetchone()
    pr_quantity = sql.execute('SELECT pr_count FROM products WHERE pr_name=?;', (pr_name[0],)).fetchone()
    new_quantity = pr_quantity[0] - amount[0]
    sql.execute('UPDATE products SET pr_count=? WHERE pr_name=?;', (new_quantity, pr_name[0]))
    info = sql.execute('SELECT * FROM cart WHERE user_id=?;', (user_id,)).fetchone()
    address = sql.execute('SELECT location FROM users WHERE id=?;', (user_id,)).fetchone()
    # Фиксируем изменения
    connection.commit()
    return info, address


# Отображение корзины
def show_cart(user_id):
    return sql.execute('SELECT user_product, pr_amount, total FROM cart WHERE user_id=?;', (user_id,)).fetchone()

all_users = sql.execute('SELECT * FROM users').fetchall()
for user in all_users:
    print(f'Пользователь: {user}')

all_products = sql.execute('SELECT * FROM products').fetchall()
for product in all_products:
    print(f'Продукт: {product}')
