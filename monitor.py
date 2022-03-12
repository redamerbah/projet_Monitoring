import locale
import sys

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
sum = 0.0
filename = sys.argv[1] 
memfile=open(filename,"r")
mem = memfile.readlines()
for line in mem:
	try :
		sum = sum + float(locale.atof(line[:-1]))
		#print (locale.atof(line[:-1]))
	except :
		print("Erreur de conversion")
memfile.close()
print(str(sum))
