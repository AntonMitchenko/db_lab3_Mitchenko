import json
import psycopg2



username = 'postgres'
password = '111'
database = 'oliksiy'
host = 'localhost'
port = '5432'

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

data = {}
with conn:
    cur = conn.cursor()

    for table in ('wonder_in_internet','wonder_of_world', 'locations'):
        cur.execute('SELECT * FROM ' + table)
        rows = []
        fields = [x[0] for x in cur.description]

        for row in cur:
            rows.append(dict(zip(fields, row)))

        data[table] = rows

with open('all_data_lab_3.json', 'w') as outf:
    json.dump(data, outf, default=str)