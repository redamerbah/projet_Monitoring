
#! /bin/bash

for file in `ls /home/reda/MiniProjet/Logs`
do
if [ $((( $(date +%s) - $(date +%s -r /home/reda/MiniProjet/Logs/$file)) / 86400)) -ge 30 ]
then
echo "DAZ"
rm /home/reda/MiniProjet/Logs/$file
fi
done
#86400
