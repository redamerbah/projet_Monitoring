#! /bin/bash

#template1=$(head -n $(grep -n '<!-- debut -->' template.html | cut -d ":" -f 1) template.html)
#template2=$(tail -n+$(grep -n '<!-- fin -->' template.html | cut -d ":" -f 1) template.html)
#msg="<p><strong style=\"color: crimson\">$1</strong> a dépassé son quota d'utilisation $3<br>Voici le graphe d'utilisation :</p>"
#graph="<object data=\"/home/reda/MiniProjet/graphs/$2$1.html\" type=\"text/html\" height=\"40%\" width=\"90%\"></object>"

#body="$template1 $msg $graph $template2"
dateAuj=$(date '+%d-%m-%Y à %H:%M')

cd /home/reda/MiniProjet/graphs

if [ -f /home/reda/MiniProjet/graphs/historiquegraph_$2$1.html  ]; then
    echo "$1 a dépassé son quota d'utilisation $3 ci contre la graphe de son utilisation dans les dernieres 24 heures :" | mail -s "Alerte $1-$2-$dateAuj" \
    -A historiquegraph_$2$1.html \
    redamerbah1999@gmail.com \

    
else
    echo "$1 a dépassé son quota d'utilisation $3!" | mail -s "Alerte $1-$2-$dateAuj" \
    redamerbah1999@gmail.com \

fi
