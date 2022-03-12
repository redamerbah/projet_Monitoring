from flask import Flask, render_template
import pygal
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route("/")
@app.route('/dashboard')
def dashboard():
    # Conexion à la base de données
    db = sqlite3.connect('/home/reda/MiniProjet/monitor.db')
    cur = db.cursor()

    users = []

    for row in cur.execute('select distinct username from resources'):
        users.append(str(row[0]))

    # Stockage de la date d'aujourd'hui en calculant le nombre de secondes passées depuis 1-1-1970 à ce jour ci (UNIX TIMESTAMP)
    now = datetime.now()
    time = datetime.timestamp(now)

    T_cpu = []
    T_ram = []
    T_storage = []
    T_dates = []

    allTabs = []

    storage = []
    sumStorage = int(0)
    multiples = ['KiB', 'MiB', 'GiB', 'TiB']
    x = 0
    for row in cur.execute('select storage, username from resources order by id desc limit(' + str(len(users)) + ');'):
        storage.append(
            [
                str(row[1]),
                int(row[0])
            ]
        )
    sum = 0
    for store in storage:
        sum += store[1]
    kbStorage = sum
    while sum >= 1024 and x <= 3:
        sum /= 1024
        x += 1

    for user in users:
        temp = []
        for row in cur.execute(
                'select cpu from resources where username="' + user + '" and ((' + str(time) + ' - date)/3600) < 6;'):
            temp.append(float(row[0]))
        TEMP = [user, temp]
        T_cpu.append(TEMP)
        TEMP = []

    for user in users:
        temp = []
        for row in cur.execute(
                'select ram from resources where username="' + user + '" and ((' + str(time) + ' - date)/3600) < 6;'):
            temp.append(float(row[0]))
        TEMP = [user, temp]
        T_ram.append(TEMP)
        TEMP = []

    for user in users:
        temp = []
        for row in cur.execute('select storage from resources where username="' + user + '" and ((' + str(
                time) + ' - date)/3600) < 6;'):
            temp.append(float(row[0]))
        TEMP = [user, temp]
        T_storage.append(TEMP)
        TEMP = []

    temp = []
    for row in cur.execute('select distinct date from resources where ((' + str(time) + ' - date)/3600) < 6;'):
        temp.append(int(row[0]))

    for time in temp:
        T_dates.append(datetime.fromtimestamp(int(time)).strftime("%d/%m/%Y %H:%M"))

    ########## Ram

    line_chart_ram = pygal.Line()
    line_chart_ram.title = 'Ram Use (%)'
    line_chart_ram.x_labels = map(str, T_dates)
    for entry in T_ram:
        line_chart_ram.add(entry[0], entry[1])
    line_chart_ram = line_chart_ram.render_data_uri()

    allTabs.append(line_chart_ram)

    ########## CPU

    line_chart_cpu = pygal.Line()
    line_chart_cpu.title = 'CPU Use (%)'
    line_chart_cpu.x_labels = map(str, T_dates)
    for entry in T_cpu:
        line_chart_cpu.add(entry[0], entry[1])
    line_chart_cpu = line_chart_cpu.render_data_uri()

    allTabs.append(line_chart_cpu)

    ########## Storage

    line_chart_store = pygal.Line()
    line_chart_store.title = 'Storage Use (KB)'
    line_chart_store.x_labels = map(str, T_dates)
    for entry in T_storage:
        line_chart_store.add(entry[0], entry[1])
    line_chart_store = line_chart_store.render_data_uri()

    allTabs.append(line_chart_store)

    pie_chart = pygal.Pie(inner_radius=.60)
    pie_chart.title = "Utilisation Stockage (" + str(format(sum, '.2f')) + " " + str(multiples[x]) + ")"
    for userstorage in storage:
        pie_chart.add(userstorage[0], float(float(userstorage[1]) / float(kbStorage)) * 100)
    pie_chart = pie_chart.render_data_uri()

    return render_template('charts.html', charts=allTabs, storagePie=pie_chart)


@app.route('/userdetails')
def userDetails():
    # Conexion à la base de données
    db = sqlite3.connect('/home/reda/MiniProjet/monitor.db')
    cur = db.cursor()

    users = []

    for row in cur.execute('select distinct username from resources'):
        users.append(str(row[0]))

    userInfos = []

    def humanReadable(storage):
        multiples = ['KiB', 'MiB', 'GiB', 'TiB']
        x = 0
        while storage >= 1024 and x <= 3:
            storage /= 1024
            x += 1
        return [format(storage, '.2f'), multiples[x]]

    for row in cur.execute(
            'select username, storage, ram, cpu from resources order by id desc limit(' + str(len(users)) + ');'):
        userInfos.append(
            [
                str(row[0]),
                humanReadable(int(row[1])),
                format(float(row[2]), '.2f'),
                format(float(row[3]), '.2f')
            ]
        )

    return render_template('userdetail.html', infos=userInfos)


if __name__ == '__main__':
    app.run(debug=True)
