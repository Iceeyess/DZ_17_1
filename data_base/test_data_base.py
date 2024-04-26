import psycopg2

# connect to database
conn = psycopg2.connect(
    host='localhost',
    database='test',
    user='postgres',
    password='Herbalife1'
)

# creation cursor
cur = conn.cursor()
# cur.execute("SELECT * FROM patients")

# cur.execute('SELECT * FROM patients;')
# rows = cur.fetchall()

# for row in rows:
#     print(row)
#execute query
cur.execute("SELECT * FROM patients")
rows = cur.fetchall()
conn.commit()
name = ['Dima', 'Victor', 'Tom']
date = ['1982-01-09', '1971-12-12', '1956-09-27']
sex = ['M', 'M', 'M']
cur.execute("""SELECT * 
FROM  patients 
where oms_num = (select max(oms_num) from patients);""")
last_oms = cur.fetchall()[0][-1]

for x in range(len(name)):
    last_oms += 1
    cur.execute(
        f"INSERT INTO patients VALUES (%s, %s, %s, %s);", (name[x], sex[x], date[x], last_oms)
        )

conn.commit()
cur.execute("SELECT * FROM patients")
rows = cur.fetchall()
cur.close()
conn.close()

