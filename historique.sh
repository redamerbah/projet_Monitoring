#! /bin/bash

usrscount=$(ls /home | wc -l)

declare -a arrUser

for i in `seq 1 $usrscount`
do
	arrUser+=($(ls /home | head -n$i | tail -n1))
done 

python3 /home/reda/MiniProjet/interactiveGraph.py ${arrUser[@]}
