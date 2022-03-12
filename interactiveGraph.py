import pygal
import os
import sys
from array import *
import sqlite3
from datetime import datetime

#Reception de la liste des utilisateurs
users = sys.argv[1:]

#Conexion à la base de données
db = sqlite3.connect('/home/reda/MiniProjet/monitor.db')
cur = db.cursor()

#Stockage de la date d'aujourd'hui en calculant le nombre de secondes passées depuis 1-1-1970 à ce jour ci (UNIX TIMESTAMP)
now = datetime.now()
time = datetime.timestamp(now)

#Traitements des données agées de 24 heures


def histo(hours, users, time):
	T_cpu = []
	T_ram = []
	T_storage = []
	T_dates = []

	for user in users:
		temp = []
		for row in cur.execute('select cpu from resources where username="'+user+'" and (('+str(time)+' - date)/3600) < '+str(hours)+';'):
			temp.append(float(row[0]))
		TEMP = [user, temp]
		T_cpu.append(TEMP)
		TEMP = []

	for user in users:
		temp = []
		for row in cur.execute('select ram from resources where username="'+user+'" and (('+str(time)+' - date)/3600) < '+str(hours)+';'):
			temp.append(float(row[0]))
		TEMP = [user, temp]
		T_ram.append(TEMP)
		TEMP = []

	for user in users:
		temp = []
		for row in cur.execute('select storage from resources where username="'+user+'" and (('+str(time)+' - date)/3600) < '+str(hours)+';'):
			temp.append(float(row[0]))
		TEMP = [user, temp]
		T_storage.append(TEMP)
		TEMP = []

	temp = []
	for row in cur.execute('select distinct date from resources where (('+str(time)+' - date)/3600) < '+str(hours)+';'):
		temp.append(int(row[0]))

	for time in temp:
		T_dates.append(datetime.fromtimestamp(int(time)).strftime("%d/%m/%Y %H:%M"))


	########## Ram

	line_chart_ram=pygal.Line()
	line_chart_ram.title='Ram Use (%)'
	line_chart_ram.x_labels=map(str,T_dates)
	for entry in T_ram:
		line_chart_ram.add(entry[0], entry[1])
	line_chart_ram.render_to_file('/home/reda/MiniProjet/graphs/temp'+str(hours)+'/historiquegraph_ram.html')

	########## CPU

	line_chart_cpu=pygal.Line()
	line_chart_cpu.title='CPU Use (%)'
	line_chart_cpu.x_labels=map(str,T_dates)
	for entry in T_cpu:
		line_chart_cpu.add(entry[0], entry[1])
	line_chart_cpu.render_to_file('/home/reda/MiniProjet/graphs/temp'+str(hours)+'/historiquegraph_cpu.html')

	########## Storage

	line_chart_store=pygal.Line()
	line_chart_store.title='Storage Use (KB)'
	line_chart_store.x_labels=map(str,T_dates)
	for entry in T_storage:
		line_chart_store.add(entry[0], entry[1])
	line_chart_store.render_to_file('/home/reda/MiniProjet/graphs/temp'+str(hours)+'/historiquegraph_storage.html')

histo(24, users, time)
histo(12, users, time)
histo(6, users, time)
histo(1, users, time)
