from employee import employees_data
from customers import customers_data
from orders import orders_data

import psycopg2

params = dict(host='localhost', port=5432, database='test', user='postgres', password='Herbalife1')
conn = psycopg2.connect(**params)

# Открытие курсора
cur = conn.cursor()

# Не меняйте и не удаляйте эти строки - они нужны для проверки
cur.execute("DROP TABLE IF EXISTS orders")
cur.execute("DROP TABLE IF EXISTS customers")
cur.execute("DROP TABLE IF EXISTS employees")

# Ниже напишите код запросов для создания таблиц
cur.execute("""
    CREATE TABLE customers(
    customer_id CHAR(5) NOT NULL UNIQUE, company_name VARCHAR(100), contact_name VARCHAR(100), PRIMARY KEY(customer_id)
    );
    """)
cur.execute("""CREATE TABLE employees(
    employee_id SERIAL, first_name VARCHAR(25) NOT NULL, last_name VARCHAR(35) NOT NULL,
    title VARCHAR(100) NOT NULL, birth_date DATE NOT NULL, notes TEXT, 
    PRIMARY KEY(employee_id));
    """)
cur.execute("""CREATE TABLE orders(
    order_id INT NOT NULL, customer_id CHAR(5) NOT NULL, employee_id INT NOT NULL, order_date DATE NOT NULL, ship_city VARCHAR(100),
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id), FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
    );
    """)
# Зафиксируйте изменения в базе данных
conn.commit()

#Теперь приступаем к операциям вставок данных
# Запустите цикл по списку customers_data и выполните запрос формата
# INSERT INTO table (column1, column2, ...) VALUES (%s, %s, ...) returning *", data)
# В конце каждого INSERT-запроса обязательно должен быть оператор returning *
cur.executemany("INSERT INTO customers VALUES(%s, %s, %s) returning *;", customers_data)
# Не меняйте и не удаляйте эти строки - они нужны для проверки
conn.commit()
cur.execute('SELECT * FROM customers;')
res_customers = cur.fetchall()

# Запустите цикл по списку employees_data и выполните запрос формата
# INSERT INTO itresume3270.table (column1, column2, ...) VALUES (%s, %s, ...) returning *", data)
# В конце каждого INSERT-запроса обязательно должен быть оператор returning *
cur.executemany("INSERT INTO employees (first_name, last_name, title, birth_date, notes) VALUES(%s, %s, %s, %s, %s) returning *;", employees_data)

# Не меняйте и не удаляйте эти строки - они нужны для проверки
conn.commit()
cur.execute("SELECT * FROM employees;")
res_employees = cur.fetchall()


# Запустите цикл по списку orders_data и выполните запрос формата
# INSERT INTO itresume3270.table (column1, column2, ...) VALUES (%s, %s, ...) returning *", data)
# В конце каждого INSERT-запроса обязательно должен быть оператор returning *
cur.executemany("INSERT INTO orders VALUES(%s, %s, %s, %s, %s) returning *;", orders_data)


# Не меняйте и не удаляйте эти строки - они нужны для проверки
conn.commit()
cur.execute("SELECT * FROM employees;")
res_orders = cur.fetchall()

# Закрытие курсора
cur.close()

# Закрытие соединения
