
#!/bin/bash

# usercount pour récuper le nombre des utilisateurs 
# cpu récuper le nombre des coeurs matériels de processeur  
usrscount=$(ls /home | wc -l)

actualDate=$(date +'+%s')

cpu=$(lscpu | tail -n+5 | head -n+1 | cut -d ":" -f 2 | awk '{print substr($0, length($0))}')

sqlite3 /home/reda/MiniProjet/monitor.db "CREATE TABLE resources(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, storage INTEGER, ram REAL, cpu REAL, date INTEGER)"

for i in `seq 1 $usrscount`
do

cd /home

usr=$(ls /home | head -n$i | tail -n1)

storage=$(python3 /home/reda/MiniProjet/storage.py $usr)

if [ $(ls /home | grep "$usr") == $(who | cut -d " " -f 1 | grep "$usr") ];
then
	if test -e /home/reda/MiniProjet/ram$usr.txt
	then
		rm /home/reda/MiniProjet/ram$usr.txt
	fi
	echo "$(top -u $usr -b -n 1 | tail -n+8 | cut -c57-60)" >> /home/reda/MiniProjet/ram$usr.txt

	ram=$(python3 /home/reda/MiniProjet/monitor.py /home/reda/MiniProjet/ram$usr.txt)
	Result=`echo "$ram > 30.0" | bc`
	if [ $Result -eq 1 ]; then
		python3 /home/reda/MiniProjet/graphs.py $usr "Ram"
		bash /home/reda/MiniProjet/mail.sh $usr "ram" "(ram : $ram%)"
	fi
	rm /home/reda/MiniProjet/ram$usr.txt
	if test -e /home/reda/MiniProjet/cpu$usr.txt
	then
		rm /home/reda/MiniProjet/cpu$usr.txt
	fi
	echo "$(top -u $usr -b -n 1 | tail -n+8 | cut -c49-54)" >> /home/reda/MiniProjet/cpu$usr.txt
	#echo $(cat /home/reda/MiniProjet/cpu$usr.txt)
	cpuval=$(python3 /home/reda/MiniProjet/CPU.py /home/reda/MiniProjet/cpu$usr.txt $cpu)
	#echo $cpuval
	
	Result=`echo "$cpu > 10.0" | bc`
	if [  $Result -eq 1 ]; then
		python3 /home/reda/MiniProjet/graphs.py $usr "CPU"
		bash /home/reda/MiniProjet/mail.sh $usr "cpu" "(cpu : $cpuval%)"
	fi
	rm /home/reda/MiniProjet/cpu$usr.txt
	#file=$(date '+/home/reda/MiniProjet/Logs/log-%d-%m-%y-%H-%M.csv')

	sqlite3 /home/reda/MiniProjet/monitor.db "INSERT INTO resources(username, storage, ram, cpu, date) VALUES('$usr', $storage, $ram, $cpuval, $actualDate)"

else
# si l'utilisateur est n'est pas connecter :
	sqlite3 /home/reda/MiniProjet/monitor.db "INSERT INTO resources(username, storage, ram, cpu, date) VALUES('$usr', $storage, 0.0, 0.0, $actualDate)"
fi
done

bash /home/reda/MiniProjet/historique.sh

#sqlite3 /home/reda/MiniProjet/monitor.db -cmd ".headers on" ".mode csv" ".once $file" "SELECT * FROM resources"
#sqlite3 /home/reda/MiniProjet/monitor.db "DROP TABLE resources"

#chown -R $USER:$USER $file
