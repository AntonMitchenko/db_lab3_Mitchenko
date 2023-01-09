import csv
import psycopg2

username = 'postgres'
password = '111'
database = 'oliksiy'

INPUT_CSV_FILE = 'wonders_of_world.csv'

delete_all = '''
DELETE FROM wonder_in_internet;
DELETE FROM wonder_of_world;
DELETE FROM locations;
'''

query_world = '''
INSERT INTO wonder_of_world (name_of_wonder, type_of_wonder ,build_in_year)  VALUES (%s, %s, %s)
'''

query_internet = '''
INSERT INTO wonder_in_internet(name_of_wonder, type_wonder, wikipedia_link,picture_link) VALUES (%s, %s,%s, %s)
'''

query_locations = '''
INSERT INTO locations (name_of_wonder,city, country, latitude, longtitude ) VALUES (%s, %s, %s, %s,%s)
'''
query_locations_null = '''
INSERT INTO locations (name_of_wonder,city, country, latitude, longtitude ) VALUES (%s, NULL ,%s, %s, %s)
'''


conn = psycopg2.connect(user=username, password=password, dbname=database)

def find_count(s):
    word_list = s.split()
    for i in word_list:
        if i.isnumeric():
            return i
    return 0


def insert_world(name, type, year, local_cur,globals):
    if globals.count(name.strip()) == 1:
        local_cur.execute(query_world, (name, type, year))

def insert_internet(name,type, wiki, picture,local_cur,globals):
    if globals.count(name.strip()) == 1:
        local_cur.execute(query_internet, (name,type, wiki, picture))


def locations_insert(name, country, latitude,longtitude,local_cur,globals):
    local_contry = country.split(',')
    if globals.count(name.strip()) == 1:
        if len(local_contry)!=1:
            local_cur.execute(query_locations, (name, local_contry[0],local_contry[-1], latitude,longtitude))
        else:
            local_cur.execute(query_locations, (name, "unknown".strip(), local_contry[-1].strip(), latitude, longtitude))

with conn:
    cur = conn.cursor()
    cur.execute(delete_all)
    with open(INPUT_CSV_FILE, 'r',encoding="UTF-8") as ret:
        reader = csv.DictReader(ret)
        globals=[]
        i=0
        for idx, row in enumerate(reader):
            if globals.count(row['Name'].strip()) == 0:
                globals.append(row['Name'].strip())
                locations_insert(row['Name'], row['Location'], row['Latitude'], row["Longitude"], cur,globals)
                insert_world(row['Name'], row['Type'], row['Build in year'], cur,globals)
                insert_internet(row['Name'],row['Type'], row['Wikipedia link'], row['Picture link'], cur,globals)
                i+=1
        print("Succesful!!", i )
    conn.commit()