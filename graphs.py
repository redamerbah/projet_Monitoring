import pygal
import os
import sys
from array import *
import sqlite3
from datetime import datetime


user = sys.argv[1]
about = sys.argv[2]


#Conexion à la base de données
db = sqlite3.connect('/home/reda/MiniProjet/monitor.db')
cur = db.cursor()

#Stockage de la date d'aujourd'hui en calculant le nombre de secondes passées depuis 1-1-1970 à ce jour ci (UNIX TIMESTAMP)
now = datetime.now()
time = datetime.timestamp(now)

#Traitements des données agées de 24 heures

T_cpu = []
T_ram = []
T_dates = []

if about == "CPU":
	temp = []
	for row in cur.execute('select cpu from resources where username="'+user+'" and (('+str(time)+' - date)/3600) < 1;'):
	    temp.append(float(row[0]))
	TEMP = [user, temp]
	T_cpu.append(TEMP)
	TEMP = []

elif about == "Ram":
	temp = []
	for row in cur.execute('select ram from resources where username="'+user+'" and (('+str(time)+' - date)/3600) < 1;'):
		temp.append(float(row[0]))
	TEMP = [user, temp]
	T_ram.append(TEMP)
	TEMP = []

else :
    print('error')

temp = []
for row in cur.execute('select distinct date from resources where (('+str(time)+' - date)/3600) < 1;'):
	temp.append(int(row[0]))

for time in temp:
	T_dates.append(datetime.fromtimestamp(int(time)).strftime("%H:%M"))


########## Ram
if about == "Ram":
    line_chart_ram=pygal.Line()
    line_chart_ram.title='Ram Use (%)'
    line_chart_ram.x_labels=map(str,T_dates)
    for entry in T_ram:
    	line_chart_ram.add(entry[0], entry[1])
    line_chart_ram.render_to_file('/home/reda/MiniProjet/graphs/historiquegraph_ram'+user+'.html')

########## CPU

elif about == "CPU":
    line_chart_cpu=pygal.Line()
    line_chart_cpu.title='CPU Use (%)'
    line_chart_cpu.x_labels=map(str,T_dates)
    for entry in T_cpu:
	    line_chart_cpu.add(entry[0], entry[1])
    line_chart_ram.render_to_file('/home/reda/MiniProjet/graphs/historiquegraph_cpu'+user+'.html')

else:
    print('error')
