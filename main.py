import psycopg2
import matplotlib.pyplot as plt


username = 'postgres'
password = '111'
database = 'oliksiy'

query_1 = '''
SELECT trim(country),count(country) from locations GROUP by country 
'''

query_2 = '''
SELECT trim(type_of_wonder),count(type_of_wonder) from wonder_of_world GROUP by type_of_wonder'''

query_3 = '''
SELECT name_of_wonder,build_in_year from wonder_of_world 
'''

conn = psycopg2.connect(user = username, password = password, dbname = database)

with conn:
    print("Database opened successfully")
    cur = conn.cursor()
    figure, (bar_ax, pie_ax, graph_ax) = plt.subplots(1, 3)
    print('1.\n')
    cur.execute(query_1)
    contry=[]
    count=[]
    for row in cur:
        contry.append(row[0])
        count.append(row[1])
    print(count)
    x_range = range(len(contry))
    bar_ax.bar(x_range, count, label='Count')
    bar_ax.set_title('Кількість чудес світу')
    bar_ax.set_xlabel('Чудеса світу')
    bar_ax.set_ylabel('Кількість')
    bar_ax.set_xticks(x_range)
    bar_ax.set_xticklabels(contry, rotation=45, ha='right')

    print('2.\n')
    type=[]
    count=[]
    cur.execute(query_2)
    for row in cur:
        type.append(row[0])
        count.append(row[1])
    pie_ax.pie(count, labels=type, autopct='%1.1f%%')
    pie_ax.set_title('відсоток кожного тику чудеса світу')
    print('3.\n')
    cur.execute(query_3)
    res = []
    res2 = []
    for row in cur:
        min = ['-']
        max = []
        res.append(row[0])
        if row[1].strip()=='':
            res2.append(0)
        elif "B"  in list(row[1].strip()):
            for i in range(0,row[1].strip().index("B")):
                if list(row[1])!=' ':
                    min.append(list(row[1].strip())[i])
            res2.append(int("".join(min).strip()))
        elif "A" in list(row[1].strip()):
            for i in range(0, row[1].strip().index("A")):
                if list(row[1]) != ' ':
                    max.append(list(row[1].strip())[i])
            res2.append(int("".join(max).strip()))
        else:
            for i in range(0, 6):
                if list(row[1])[i] != ' ':
                    max.append(list(row[1].strip())[i])
                else:
                    break
            res2.append(int("".join(max).strip()))
    for i in range(len(res)-1):
        print(res[i],res2[i])
    graph_ax.plot(res, res2, marker='o')
    graph_ax.set_xlabel('назва будівлі')
    graph_ax.set_ylabel('рік будування')
    graph_ax.set_title('Графік залежності будівлі, від року будуванння ')

mng = plt.get_current_fig_manager()
mng.resize(1500, 600)

plt.show()