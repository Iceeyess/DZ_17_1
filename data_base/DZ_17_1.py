# Исходные данные для заполнения таблиц
import csv

with open('customers_data.csv', newline='') as file:
    customers_data = [row for row in csv.reader(file) if 'customer_id' not in row]

with open('employees_data.csv', newline='') as file:
    employees_data = [row for row in csv.reader(file) if 'first_name' not in row]

with open('orders_data.csv', newline='') as file:
    orders_data = [row for row in csv.reader(file) if 'order_id' not in row]

# Импортируйте библиотеку psycopg2
import psycopg2

# Создайте подключение к базе данных
params = dict(host='sql_db', port=5432, database='analysis', user='simple', password='qweasd963')
conn = psycopg2.connect(**params)

# Открытие курсора
cur = conn.cursor()

# Не меняйте и не удаляйте эти строки - они нужны для проверки
cur.execute("create schema if not exists itresume3270;")
cur.execute("DROP TABLE IF EXISTS itresume3270.orders")
cur.execute("DROP TABLE IF EXISTS itresume3270.customers")
cur.execute("DROP TABLE IF EXISTS itresume3270.employees")

# Ниже напишите код запросов для создания таблиц
cur.execute("""
    CREATE TABLE itresume3270.customers(
    customer_id CHAR(5) NOT NULL UNIQUE, company_name VARCHAR(100), contact_name VARCHAR(100), PRIMARY KEY(customer_id)
    );
    """)
cur.execute("""CREATE TABLE itresume3270.employees(
    employee_id SERIAL, first_name VARCHAR(25) NOT NULL, last_name VARCHAR(35) NOT NULL,
    title VARCHAR(100) NOT NULL, birth_date DATE NOT NULL, notes TEXT, 
    PRIMARY KEY(employee_id));
    """)
cur.execute("""CREATE TABLE itresume3270.orders(
    order_id INT NOT NULL, customer_id CHAR(5) NOT NULL, employee_id INT NOT NULL, order_date DATE NOT NULL, ship_city VARCHAR(100),
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id), FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
    );
    """)

# Зафиксируйте изменения в базе данных
conn.commit()

# Теперь приступаем к операциям вставок данных
# Запустите цикл по списку customers_data и выполните запрос формата
# INSERT INTO table (column1, column2, ...) VALUES (%s, %s, ...) returning *", data)
# В конце каждого INSERT-запроса обязательно должен быть оператор returning *
cur.executemany("INSERT INTO itresume3270.customers VALUES(%s, %s, %s) returning *;", customers_data)
# Не меняйте и не удаляйте эти строки - они нужны для проверки
conn.commit()
cur.execute('SELECT * FROM itresume3270.customers')
res_customers = [cur.fetchall()[-1],]

# Запустите цикл по списку employees_data и выполните запрос формата
# INSERT INTO itresume3270.table (column1, column2, ...) VALUES (%s, %s, ...) returning *", data)
# В конце каждого INSERT-запроса обязательно должен быть оператор returning *
cur.executemany(
    "INSERT INTO itresume3270.employees (first_name, last_name, title, birth_date, notes) VALUES(%s, %s, %s, %s, %s) returning *;",
    employees_data)

# Не меняйте и не удаляйте эти строки - они нужны для проверки
conn.commit()
cur.execute('SELECT * FROM itresume3270.employees')
res_employees = [cur.fetchall()[-1],]

# Запустите цикл по списку orders_data и выполните запрос формата
# INSERT INTO itresume3270.table (column1, column2, ...) VALUES (%s, %s, ...) returning *", data)
# В конце каждого INSERT-запроса обязательно должен быть оператор returning *
cur.executemany("INSERT INTO itresume3270.orders VALUES(%s, %s, %s, %s, %s) returning *;", orders_data)

# Не меняйте и не удаляйте эти строки - они нужны для проверки
conn.commit()
cur.execute('SELECT * FROM itresume3270.orders')
res_orders = [cur.fetchall()[-1],]

# Закрытие курсора
cur.close()

# Закрытие соединения
conn.close()
