#! /bin/bash

dateOfToday=$(date '+log-%d-%m-%y-')

cd /home/reda/MiniProjet/Logs

files=$(find -name "$dateOfToday*")

zip $(date '+/home/reda/MiniProjet/Logs/archive-%d-%m-%y.zip') $files

rm $files

chown -R $USER:$USER $(date '+/home/reda/MiniProjet/Logs/archive-%d-%m-%y.zip')
