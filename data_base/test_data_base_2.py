import psycopg2

# connect to database
with psycopg2.connect(
    host='localhost',
    database='test',
    user='postgres',
    password='Herbalife1'
) as conn:
    with conn.cursor() as cur:
        name = ['Dima', 'Victor', 'Tom']
        date = ['1982-01-09', '1971-12-12', '1956-09-27']
        sex = ['M', 'M', 'M']
        cur.execute("""SELECT * 
        FROM  patients 
        where oms_num = (select max(oms_num) from patients);""")
        last_oms = cur.fetchall()[0][-1]
        list_ = []
        for x in range(len(name)):
            last_oms += 1
            list_.append((name[x], sex[x], date[x], last_oms))
        cur.executemany(
            f"INSERT INTO patients VALUES (%s, %s, %s, %s);", list_)
        cur.execute("SELECT * FROM patients")
        rows = cur.fetchall()
    conn.close()
